# raic_download_images.py
#
# Author: Brian D Goodwin; brian@synthetaic.com
# Date: 2022-05-18
#
# Purpose: facilitate image downloads from data labels built via RAIC.
#
# Output: all files deposited in desired output folder and a reference
#   dataframe saved as a CSV file, which ties the local filenames back
#   to the original URL.

import os
import argparse
import asyncio
import csv
from pathlib import Path, PurePath
from typing import List
from uuid import uuid4

import pandas as pd
from aiohttp import ClientSession


async def http_get(
    session: ClientSession,
    url: str,
    outfilename: str,
    sas: str,
    headers: dict = {},
    proxy: str = None,
    timeout: int = 5*60,
) -> bytes:

    response = await session.get(
        url=url + sas, headers=headers, proxy=proxy, timeout=timeout
    )
    content = None

    out = {"url": url, "filename": None}

    try:
        content = await response.read()
        with open(outfilename, "wb") as f:
            f.write(content)
        out["filename"] = outfilename
    except:
        pass

    return out


async def http_get_parallel(
    session: ClientSession,
    indf: pd.DataFrame,
    sas: str,
    headers: dict = {},
    proxy: str = None,
    timeout: int = 5*60,
) -> List[dict]:

    results = await asyncio.gather(
        *[
            http_get(session, row.url, row.outfile, sas, headers, proxy, timeout)
            for k, row in indf.iterrows()
        ]
    )
    return results


def getSASkey(csvFile: str) -> str:
    with open(csvFile, newline="") as f:
        reader = csv.reader(f)
        SASkey = next(reader)[1]
    return SASkey


async def main(args: argparse.Namespace) -> int:
    csvFile = args.input
    outDir = args.outdir
    isImagery = args.image_or_video

    SASkey = getSASkey(csvFile)
    df = pd.read_csv(csvFile, skiprows=1)
    df["outfile"] = df["url"].apply(
        lambda x: PurePath(
            outDir,
            *list(
                Path(x).parts[-4:] if not isImagery else [str(uuid4()) + Path(x).suffix]
            ),
        )
    )

    df["outfile"].apply(lambda x: os.makedirs(Path(x).parent, exist_ok=True))

    sess = ClientSession()
    res = await http_get_parallel(sess, df, SASkey)
    saved_csv = str(PurePath(outDir, "ref_" + Path(csvFile).stem + ".csv"))
    await sess.close()

    try:
        pd.DataFrame(res).to_csv(saved_csv)
        print(f"Successfully saved csv to:\n{saved_csv}")
    except:
        print("Failed to save reference CSV... ignoring...")
        return 1
    
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input", required=True, help="CSV file exported from RAIC portal"
    )
    parser.add_argument(
        "-o", "--outdir", required=True, help="output directory for downlaoded images"
    )
    parser.add_argument(
        "--image-or-video",
        action="store_true",
        help="include this flag if the exported CSV contains data from image or video datasets (not geospatial).",
    )

    args = parser.parse_args()

    asyncio.run(main(args))
