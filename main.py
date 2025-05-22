import argparse
from utils.jobnetmm import JobNetScraper
from utils.jobdbsg import JobsDBScraper
from utils.jobsdbth import JobsDBThScraper
from utils.jobstreetmalay import JobStreetMalaysia
from utils.founditSG import FounditScraper
from utils.data_normalizer import JobDataNormalizer
import os


def extract_founditsg():
    raw = FounditScraper(headless=True).extract_jobs()
    df = JobDataNormalizer().founditsg(raw)
    df.to_csv("output/foundit.csv", index=False, encoding='utf-8-sig')
    return df


def main(source):
    dispatch = {
        "founditsg": extract_founditsg,
    }
    if source not in dispatch:
        raise ValueError(f"Unknown source: {source}")
    
    df = dispatch[source]()
    print(f"Data extraction for {source} completed.")
    print(df.head())
    print(f"Data extraction for {source} completed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    args = parser.parse_args()
    main(args.source)