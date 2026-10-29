#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download VS Code extensions as VSIX files using cURL.

Default:
    Download the latest version of every installed extension.

Options:
    -f, --file       Read extension IDs and optional versions from a file.
    -i, --install    Install each downloaded VSIX.
    -o, --output-dir Choose the output directory.
    --installed-versions
                     Download the exact versions currently installed.

Extension file format (one per line):
    ms-python.python
    esbenp.prettier-vscode
    ms-vscode.cpptools@1.20.5
"""

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path

CURL_CMD = "curl.exe" if platform.system() == "Windows" else "curl"


def parse_extension(spec: str) -> tuple[str, str]:
    """
    Parse publisher.package[@version].

    If no version is provided, use 'latest'.
    """
    extension_id, separator, version = spec.strip().partition("@")
    parts = extension_id.split(".", 1)

    if len(parts) != 2 or not all(parts):
        raise ValueError(
            f"Invalid extension ID: {spec!r}. " "Expected publisher.package[@version]."
        )

    if separator and not version.strip():
        raise ValueError(f"Missing version in extension specification: {spec!r}")

    return extension_id, version.strip() if separator else "latest"


def vsix_url(extension: str, version: str = "latest") -> str:
    """Build the VSIX download URL for a publisher.package extension."""
    extension_id, _ = parse_extension(extension)
    publisher, package = extension_id.split(".", 1)

    return (
        f"https://{publisher}.gallery.vsassets.io/"
        f"_apis/public/gallery/publisher/{publisher}/"
        f"extension/{package}/{version}/"
        "assetbyname/Microsoft.VisualStudio.Services.VSIXPackage"
    )


def get_extensions(
    file_path: Path | None,
    installed_versions: bool = False,
) -> list[str]:
    """Read extension specifications from a file or the VS Code CLI."""

    if file_path:
        if not file_path.is_file():
            raise FileNotFoundError(f"Extension list not found: {file_path}")

        lines = file_path.read_text(encoding="utf-8-sig").splitlines()

    else:
        command = ["code", "--list-extensions"]

        if installed_versions:
            command.append("--show-versions")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        lines = result.stdout.splitlines()

    # Ignore blank lines and comments; remove duplicates while preserving order.
    extensions = list(
        dict.fromkeys(
            line.strip()
            for line in lines
            if line.strip() and not line.lstrip().startswith("#")
        )
    )

    if not extensions:
        raise ValueError("No extensions found.")

    return extensions


def download_extension(
    spec: str,
    output_dir: Path,
) -> Path:
    """Download one extension VSIX and return its path."""

    extension_id, version = parse_extension(spec)
    output_file = output_dir / f"{extension_id}.vsix"
    url = vsix_url(extension_id, version)

    command = [
        CURL_CMD,
        "--fail",
        "--location",
        "--retry",
        "3",
        "--retry-delay",
        "1",
        "--output",
        str(output_file),
        url,
    ]

    print(f"Downloading {extension_id} ({version})...")

    try:
        subprocess.run(command, check=True)

        if not output_file.is_file() or output_file.stat().st_size == 0:
            raise RuntimeError("Download produced an empty file.")

    except (subprocess.CalledProcessError, OSError, RuntimeError):
        output_file.unlink(missing_ok=True)
        raise

    print(f"Saved: {output_file}")
    return output_file


def main() -> int:
    """main function

    Returns:
        int: err code
    """
    parser = argparse.ArgumentParser(
        description="Download VS Code extensions as VSIX files."
    )

    parser.add_argument(
        "-f",
        "--file",
        type=Path,
        help="File containing extension IDs, optionally with @version.",
    )
    parser.add_argument(
        "-i",
        "--install",
        action="store_true",
        help="Install each VSIX after downloading.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("./extensions"),
        help="Output directory (default: ./extensions).",
    )
    parser.add_argument(
        "--installed-versions",
        action="store_true",
        help=(
            "Download the exact versions currently installed. "
            "Used when no extension file is supplied."
        ),
    )

    args = parser.parse_args()

    if shutil.which(CURL_CMD) is None:
        parser.error(f"Could not find cURL executable: {CURL_CMD}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    try:
        extensions = get_extensions(
            args.file,
            installed_versions=args.installed_versions and args.file is None,
        )

        failures = []

        for spec in extensions:
            try:
                vsix_path = download_extension(spec, args.output_dir)

                if args.install:
                    subprocess.run(
                        ["code", "--install-extension", str(vsix_path)],
                        check=True,
                    )
                    print(f"Installed: {spec}")

            except (
                OSError,
                ValueError,
                RuntimeError,
                subprocess.CalledProcessError,
            ) as exc:
                print(f"ERROR: {spec}: {exc}", file=sys.stderr)
                failures.append(spec)

        succeeded = len(extensions) - len(failures)
        print(f"\nFinished: {succeeded} succeeded, " f"{len(failures)} failed.")

        if failures:
            print("Failed extensions:", ", ".join(failures))
            return 1

        return 0

    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
