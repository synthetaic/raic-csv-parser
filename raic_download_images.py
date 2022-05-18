import argparse
import asyncio
import csv
import json
import os
import subprocess
from itertools import repeat
from pathlib import Path, PurePath
from typing import Any, Dict, List, Tuple
from uuid import uuid4

import pandas as pd
import requests
from aiohttp import ClientSession


async def http_get_with_aiohttp(
    session: ClientSession,
    url: str,
    sas: str,
    headers: Dict = {},
    proxy: str = None,
    timeout: int = 10,
) -> bytes:

    response = await session.get(
        url=url + sas, headers=headers, proxy=proxy, timeout=timeout
    )
    content = None
    try:
        content = await response.read()
    except:
        pass
    return content


async def http_get_with_aiohttp_parallel(
    session: ClientSession,
    list_of_urls: List[str],
    sas: str,
    headers: Dict = {},
    proxy: str = None,
    timeout: int = 10,
) -> List[bytes]:

    results = await asyncio.gather(
        *[
            http_get_with_aiohttp(session, url, sas, headers, proxy, timeout)
            for url in list_of_urls
        ]
    )
    return results


def getSAASkey(csvFile: str) -> str:
    with open(csvFile, newline="") as f:
        reader = csv.reader(f)
        SaaSkey = next(reader)[1]
    return SaaSkey


def main(args) -> None:
    csvFile = args.input
    outDir = args.outdir
    isImagery = args.image

    SASkey = getSAASkey(csvFile)
    df = pd.read_csv(csvFile, skiprows=1)






    for index, row in df.iterrows():
        try:
            file_path = os.path.join(outDir, str(row["category"]))
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            full_link = '"' + row["url"] + SASkey + '"'
            processcmd = "azcopy cp " + full_link + " " + file_path
            transfer = subprocess.call(processcmd, stderr=subprocess.STDOUT)
            downloadedName = str(row["url"]).split("/")[
                len(str(row["url"]).split("/")) - 1
            ]
            newName = "image_" + str(i) + ".jpg"
            os.rename(
                os.path.join(file_path, downloadedName),
                os.path.join(file_path, newName),
            )
        except EOFError as error:
            print("Error with SAS")
        except Exception as e:
            print(str(e) + "Unknown error has occured")
        i += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input", required=True, help="CSV file downloaded from RAIC portal"
    )
    parser.add_argument(
        "-o", "--outdir", required=True, help="output directory for downlaoded images"
    )
    parser.add_argument(
        "--image-or-video",
        action="store_false",
        help="include this flag if the exported CSV contains data from image or video datasets (not geospatial).",
    )

    args = parser.parse_args()

    main(args)
