# vsix_downloader

This work builds on top of Taylor Jones work available here <https://gist.github.com/taylor-jones/78d4db0163bb0ae94131f58c75f425fe>

- Adds option to use a file instead of installed extensions using `argparse`;
- Updates use of module `os` with `subprocess`.

## What it does

The script downloads the latest versions of set extensions, regardless of your VSCode installation. VSCode might therefore need to be updated so that all extensions work properly.

## Usage

```sh
usage: vsix_download.py [-h] [-f FILE] [-i]

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File containing extensions
  -i, --install         Allows to auto intall each vsix as they are downloaded
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
