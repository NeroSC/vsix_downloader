# vsix_downloader

This work builds on top of Taylor Jones work available here <https://gist.github.com/taylor-jones/78d4db0163bb0ae94131f58c75f425fe>

- Adds option to use a file instead of installed extensions using `argparse`;
- Updates use of module `os` with `subprocess`.

## What it does

The script downloads the latest versions of set extensions, regardless of your VSCode installation. VSCode might therefore need to be updated so that all extensions work properly.

## Launch

Two options

- with file :

```sh
python3 vsix_download.py -file extensions.txt
```

- with installed vscode extensions

```sh
python3 vsix_download.py
```

Find `.vsix` in the extensions folder.
