# vsix_downloader

This work builds on top of Taylor Jones work available here <https://gist.github.com/taylor-jones/78d4db0163bb0ae94131f58c75f425fe>

- Adds option to use a file instead of installed extensions using `argparse`;
- Updates use of module `os` with `subprocess`.
- Install the downloaded extentions

## What it does

The script downloads the latest versions of set extensions, unless a version is specified next to the extension name in extension@version format

## Usage

```sh
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
```

## Launch

Two options

- with file :

```sh
python3 vsix_download.py --file extensions.txt
```

- with installed vscode extensions

```sh
python3 vsix_download.py
```

Find `.vsix` in the extensions folder.
