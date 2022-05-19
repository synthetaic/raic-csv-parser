# Purpose

The script to download imagery from RAIC using a CSV export is provided:

```sh
python raic_download_images.py -i <RAIC csv file name> -o <output directory> [--image-or-video]
```

`-i` the file path to the exported CSV from RAIC

`-o` the output directory path in which all downloaded data will be deposited

`--image-or-video` flag, if present indicates that the CSV was exported for either image or video datasets (i.e., _NOT_ geospatial imagery)

This script was tested using python3.8.

Your python invironment requires that the packages in `requirements.txt` be installed (e.g., `pip install -r ./requirements.txt`).

# Running the Script 

The main script can be run using a (provided) docker environment or your own python environment. All testing was carried out using the docker environment described below

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
    python /root/raic_download_images.py -i /root/input.csv -o /root/data [--image-or-video]
```

