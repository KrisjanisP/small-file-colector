Having a directory with millions of small uncompressed text files is an unnecessary burden for the operating system. `collect.py` collects these files or just their metadata and stores them in a `.zip` file.

## Prerequisites

`Python3` must be installed together with `tqdm`.

```bash
pip install tqdm
```

## Usage

```
python3 collect.py -in <input directory> -out <output file (.zip)>
```

TODO: add flag to also collect file content
