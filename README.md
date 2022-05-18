# THIS IS A PUBLIC REPOSITORY

# Use

The script to download imagery from RAIC using a CSV export is provided:

```sh
python raic_download_images.py -i <RAIC csv file name> -o <output directory>
```

This script was tested using python3.8 and requires [azcopy](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10) to be installed.

## Optional environment setup

This python script was tested using __python3.8__. Optionally, to setup an environment using docker, you could use the following steps.

First, pull the python3.8 image.

```sh
docker pull python:3.8
```

Then start a docker container user.

```sh
docker run --name raicdownload -dit -v /path/to/this/repo:/root/code python:3.8
```

Step into the container to run the script

```sh
docker exec -it raicdownload bash
```

Install `azcopy` (note that azcopy is at version 10.15.0 at the time of authorship and you may need to change the last line in the following block to match the version that was installed):

```sh
cd

wget https://aka.ms/downloadazcopy-v10-linux

tar -xzvf downloadazcopy-v10-linux

echo "export PATH=\$PATH:/root/azcopy_linux_amd64_10.15.0" >> /root/.bashrc
```

Then navigate to the `/root/code` directory and install the requirements from the _requirements.txt_ file:

```sh
cd /root/code

pip install -r requirements.txt
```

# Run the script

Using the optional environment setup as above, run the following command in a terminal from inside the repository folder (where the _raic\_download\_images.py_ file is located). The example below assumes that the exported CSV file is located in the `raic-csv-parser/data/` folder.

```sh
mkdir data/outputfiles

python raic_download_images.py -i ./data/<raic csv file name>.csv -o ./data/outputfiles/
```

