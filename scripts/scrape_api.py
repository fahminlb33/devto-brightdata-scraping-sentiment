import os
import json
import glob
import itertools
import argparse
from typing import Any

import tqdm

from magic.brightdata import BrightDataClient

CNN_PAGE_LENGTH_CONST = 10
ENGINE_DATASET_ID = {
    "cnn": "gd_lycz8783197ch4wvwg",  # discover by keyword
    "bbc": "gd_ly5lkfzd1h8c85feyh",  # discover by keyword
    "reuters": "gd_lyptx9h74wtlvpnfu",  # discover by keyword
}


def run_discover(args: dict[str, Any], client: BrightDataClient):
    # open output file
    with open(args["output_file"], "a+") as output_file:
        # get keywords
        keywords = [x.strip() for x in args["keywords"].split(",")]

        # create body
        body = []
        if args["engine"] == "cnn":
            # CNN
            max_pages = args["limit"] // CNN_PAGE_LENGTH_CONST
            body = [
                {
                    "url": f"https://edition.cnn.com/search?q={keyword}&from=0&size={CNN_PAGE_LENGTH_CONST}&page={page}&sort=newest&types=all"
                }
                for page, keyword in itertools.product(
                    range(1, max_pages + 1), keywords
                )
            ]
        elif args["engine"] == "bbc":
            # BBC
            body = [{"keyword": keyword} for keyword in keywords]
        else:
            # Reuters
            body = [{"keyword": keyword, "sort": "newest"} for keyword in keywords]

        # trigger scraping
        res = client.trigger_data_collection(
            ENGINE_DATASET_ID[args["engine"]],
            args["limit"],
            True,
            body,
            "discover_new",
            "search_url" if "url" in body[0] else "keyword",
        )

        # save to output
        job = {
            "snapshot_id": res["snapshot_id"],
            "engine": args["engine"],
            "keywords": keywords,
        }

        json.dump(job, output_file)
        output_file.write("\n")


def run_download(args: dict[str, Any], client: BrightDataClient):
    # make sure output directory is exists
    os.makedirs(args["output_path"], exist_ok=True)

    # glob downloaded files
    downloaded_files = glob.glob(os.path.join(args["output_path"], "*.jsonl"))

    # to store stats
    stats = {
        "downloaded": 0,
        "skipped": 0,
        "running": 0,
        "failed": 0,
    }

    # open input file
    with open(args["snapshots_file"], "r") as f:
        # process each job
        for line in tqdm.tqdm(f.readlines()):
            # parse job
            job = json.loads(line.strip())

            # check if this file is already downloaded
            if job["snapshot_id"] + ".jsonl" in downloaded_files:
                stats["skipped"] += 1
                continue

            # check status
            res = client.monitor_progress(job["snapshot_id"])

            # process response
            if res["status"] == "ready":
                stats["downloaded"] += 1

                # open save file
                with open(
                    os.path.join(args["output_path"], job["snapshot_id"] + ".jsonl"),
                    "w",
                ) as output_file:
                    # download the data
                    res = client.download(job["snapshot_id"])

                    # save to file
                    output_file.write(res)
            elif res["status"] == "running":
                stats["running"] += 1
            elif res["status"] == "failed":
                stats["failed"] += 1

    # print statistics
    print("Downloaded:", stats["downloaded"])
    print("Skipped:", stats["skipped"])
    print("Running:", stats["running"])
    print("Failed:", stats["failed"])


def main(args: dict[str, Any]):
    print(args)

    # create API client
    client = BrightDataClient(args["api_key"])

    # run
    if args["mode"] == "discover":
        run_discover(args, client)
    elif args["mode"] == "download":
        run_download(args, client)


if __name__ == "__main__":
    # --- create main argparser
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", type=str, required=True)

    # --- register subparsers
    subparsers = parser.add_subparsers(dest="mode")

    # trigger scraping by keyword
    discover = subparsers.add_parser("discover")
    discover.add_argument("--output-file", type=str, required=True)
    discover.add_argument("--keywords", type=str, required=True)
    discover.add_argument(
        "--engine", type=str, choices=["cnn", "bbc", "reuters"], required=True
    )
    discover.add_argument("--limit", type=int, default=50)

    # download snapshots
    download = subparsers.add_parser("download")
    download.add_argument("--snapshots-file", type=str, required=True)
    download.add_argument("--output-path", type=str, required=True)

    # run app
    main(vars(parser.parse_args()))
