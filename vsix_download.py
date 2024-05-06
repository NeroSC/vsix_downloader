#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Download the latest versions of all installed VSCode extensions with cURL.
TODO: Update to allow for specifying extension version (but default to latest version).
"""

import argparse
import platform
import subprocess
from pathlib import Path

match platform.system():
    case "Windows":
        CURL_CMD = "curl.exe"
    case "Linux":
        CURL_CMD = "curl"
    case _:
        CURL_CMD = "CUSTOM_CURL_CMD"


def vsix_url(extension: str):
    """
    Gets the URL for a .vsix VSCode extension, given the full name
    of the extension in the format of {publish}.{package}

    ex: ms-python.python

    Args:
        extension (str): name of vscode extension "publisher.package"

    Returns:
        str: Url to the extension download
    """
    publisher, package = extension.split('.')
    return f'https://{publisher}.gallery.vsassets.io/_apis/public/gallery/publisher/{publisher}/extension/{package}/latest/assetbyname/Microsoft.VisualStudio.Services.VSIXPackage'


def vsix_curl(extension: str, link: str, output_dir: str, curl_cmd: str = CURL_CMD):
    """Builds and returns the cURL command to download a vscode extension
    to a spexified directory and filename.

    Args:
        extension (str): name of extension "publisher.package"
        link (str): download link for the latest version of the extension
        output_dir (str): output directory where the new .vsix will be stored
        curl_cmd (str, optional): command to use for cURL, depends on OS. Defaults to CURL_CMD.

    Returns:
        str: Download command with curl
    """
    return f'{curl_cmd} {link} -o {output_dir}/{extension}.vsix'


if __name__ == "__main__":

    OUTPUT_DIR = './extensions'

    if Path(OUTPUT_DIR).is_dir():
        pass
    else:
        subprocess.run(['mkdir', OUTPUT_DIR], check=True)

    # adding -file argument
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str, help="File containing extensions")
    parser.add_argument("-i", "--install", action='store_true',
                        help="Allows to auto intall each vsix as they are downloaded")

    args = parser.parse_args()

    # Arguments checks
    INSTALL = args.install

    if args.file:
        with open("extensions.txt", "r", encoding="utf-8") as file:
            extensions = file.read().splitlines()
    else:
        # get a list of all installed extensions
        results = subprocess.run(
            ['code', '--list-extensions'], stdout=subprocess.PIPE, check=True, shell=True)
        extensions = results.stdout.decode("utf-8").splitlines()

    # download each of the extensions and place them in a specified directory.
    for ext in extensions:
        url = vsix_url(ext)
        cmd = vsix_curl(ext, url, OUTPUT_DIR)
        subprocess.run(cmd.split(), check=True, shell=True)
        if True is INSTALL:
            subprocess.run(["code", "--install-extension", f"{OUTPUT_DIR}/{ext}.vsix"], check=True)
