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

import argparse
import asyncio
import csv
import os
from os.path import join as pjoin
from pathlib import Path, PurePath
from typing import List
from uuid import uuid4

import numpy as np
import pandas as pd
from aiohttp import ClientSession


async def http_get(
    session: ClientSession,
    url: str,
    outfilename: str,
    headers: dict = {},
    proxy: str = None,
    timeout: int = 5 * 60,
) -> dict:

    response = await session.get(
        url=url, headers=headers, proxy=proxy, timeout=timeout
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
    headers: dict = {},
    proxy: str = None,
    timeout: int = 5 * 60,
) -> List[dict]:

    results = await asyncio.gather(
        *[
            http_get(session, row.Url, row.outfile, headers, proxy, timeout)
            for k, row in indf.iterrows()
        ]
    )
    return results


async def main(args: argparse.Namespace) -> int:
    csvFile = args.input
    outDir = args.outdir
    isImagery = not args.geospatial_data
    colname = "Url" if args.crops_only else "OriginalImageUrl"

    df = pd.read_csv(csvFile)
    
    tmp = df[["FileName",colname]].astype(str)
    tmp = tmp.rename(columns={colname:"Url"})
    tmp = tmp.drop_duplicates()
    
    if args.crops_only:
        tmp["CropNum"] = tmp.groupby("FileName").cumcount().astype(str)
        tmp["outfile"] = tmp.apply(lambda x: (outDir / Path(x.FileName).with_suffix("") / (x.CropNum+".jpg")),axis=1).astype(str) # jpg is the default output from RAIC crops
        crop_dirs = np.unique(np.array([str(Path(k).parent) for k in tmp.outfile.tolist()]))
        _ = [os.makedirs(k, exist_ok=True) for k in crop_dirs]
    else:
        tmp["outfile"] = [str(outDir / Path(k)) for k in tmp["FileName"].tolist()]
        _ = [os.makedirs(Path(k).parent, exist_ok=True) for k in tmp["outfile"].tolist()]
    
    sess = ClientSession()
    res = await http_get_parallel(sess, tmp)
    saved_csv = str(PurePath(outDir, "ref_" + Path(csvFile).stem + ".csv"))
    await sess.close()

    try:
        pd.DataFrame(res).to_csv(saved_csv)
        print(f"Successfully saved reference dataframe CSV to:\n{saved_csv}")
        
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
        "--geospatial-data",
        action="store_true",
        help="include this flag if the exported CSV contains data from the Maps RAIC module.",
    )
    parser.add_argument(
        "--crops-only",
        action="store_true",
        help="Specifies that only the crops (instead of the whole images) from the detections should be downloaded. Otherwise, the whole image is downloaded. This flag is automatically set to false if `--geospatial-data` flag is present.",
    )

    args = parser.parse_args()
    
    print(args)

    asyncio.run(main(args))
