#!/usr/bin/env python3

"""Down load images from Zooniverse."""

import os
from os.path import join, exists
from datetime import datetime
import argparse
# from tqdm import tqdm
import requests
from panoptes_client import Panoptes, Workflow


def download_images(args):
    """Down load images from Zooniverse."""
    Panoptes.connect(username=args.username, password=args.password)
    workflow = Workflow.find(args.workflow)
    skips, downloads = 0, 0
    for j, subject_set in enumerate(workflow.links.subject_sets, 1):
        print(subject_set)
        for i, subject in enumerate(subject_set.subjects, 1):
            now = datetime.now().strftime('%Y-%M-%d %H:%M:%S')
            url = subject.locations[0]['image/jpeg']
            path = join(args.dir, f'{subject.id}.jpg')
            if exists(path):
                skips += 1
                print(f'{now} skipping {j} {i} {path}')
            else:
                downloads += 1
                print(f'{now} downloading {j} {i} {path}')
                response = requests.get(url, allow_redirects=True)
                open(path, 'wb').write(response.content)
    print(f'{now} Skipped {skips} Downloaded {downloads}'
          f' Total {skips + downloads}')


def parse_args():
    """Process command-line arguments."""
    parser = argparse.ArgumentParser(
        allow_abbrev=True,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Download images to the given directory.""")

    parser.add_argument(
        '--username', '-u', required=True,
        help="""Your Zooniverse user name.""")

    parser.add_argument(
        '--password', '-p', required=True,
        help="""Your Zooniverse password.""")

    parser.add_argument(
        '--workflow', '-w', required=True,
        help="""The ID of the workflow containing the images.""")

    parser.add_argument(
        '--dir', '-d', required=True,
        help="""Put the images in this directory.""")

    args = parser.parse_args()

    os.makedirs(args.dir, exist_ok=True)

    return args


if __name__ == "__main__":
    ARGS = parse_args()
    download_images(ARGS)
