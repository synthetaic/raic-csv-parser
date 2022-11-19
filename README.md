# Purpose

The script to download imagery from RAIC using a CSV export is provided in this repo, __raic_download_images.py__. 

```sh
python raic_download_images.py -i <RAIC csv file name> -o <output directory>
```

`-i` the file path to the exported CSV from RAIC.

`-o` the output directory path in which all downloaded data will be deposited.

`--geospatial-data` flag, if present, indicates that the CSV was exported from the Maps RAIC module.

`--crops-only` flag, if present, indicates that only the detected crops should be downloaded.

## Deps

This script was tested using python3.8.

Your python invironment requires that the packages in `requirements.txt` be installed (e.g., `pip install -r ./requirements.txt`).

## Example usage

```sh
python raic_download_images.py --input ./data/4f3e7f32-4aba-449d-a277-e23fab876a0f_categories_18-11-22.csv --outdir /local/folder/crops --crops-only
```
