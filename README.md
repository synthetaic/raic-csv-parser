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

## Docker environment setup

Build the docker image:

```sh
docker build -t raiccsv:v1 .
```

The following command can be run right from the terminal. This command is setup such that your __input CSV file path__ and __output directory__ are `/full/path/to/categories_raic_csvfile.csv` and `/full/path/to/output/directory`, respectively. (The `--image-or-video` flag should be included if the exported CSV comes from either video data or imagery data; i.e., _not_ geospatial/map imagery.)

```sh
docker run \
    -v /full/path/to/categories_raic_csvfile.csv:/root/input.csv \
    -v /full/path/to/output/directory:/root/data \
    raiccsv:v1 \
    python /root/raic_download_images.py -i /root/input.csv -o /root/data 
```

