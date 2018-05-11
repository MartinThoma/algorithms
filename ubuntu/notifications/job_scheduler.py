#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""How to receive the last-modified header."""

import csv
import logging
import os
import requests
import subprocess
import sys
import time
from multiprocessing import Process


logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.DEBUG,
                    stream=sys.stdout)


def sendmessage(summary, body):
    subprocess.Popen(['notify-send', summary, body])
    return


def read_jobs(csv_filepath):
    with open(csv_filepath, 'r') as fp:
        reader = csv.DictReader(fp, delimiter=';', quotechar='"')
        data_read = [row for row in reader]
    return data_read


def get_last_modified(url):
    """Get the Last-Modified header of an URL."""
    header = requests.head(url).headers
    if 'Last-Modified' in header:
                return header['Last-Modified']
    else:
        return None


def create_new_process(csv_filepath, line_nr):
    assert line_nr >= 0, "line_nr={line_nr}".format(line_nr)
    jobs = read_jobs(csv_filepath)
    logging.info("Start job for '{name}'".format(name=jobs[line_nr]['name']))
    p = Process(target=job_runner,
                args=(csv_filepath, line_nr, jobs))
    p.start()
    return p


def job_runner(csv_filepath, line_nr, jobs):
    name = jobs[line_nr]['name']
    url = jobs[line_nr]['url']
    intervall = int(jobs[line_nr]['intervall'])
    last_modified_seen = jobs[line_nr]['url']
    print("Run line_nr={}".format(line_nr))
    while True:
        print 'process id:', os.getpid()
        # Get websites last modified
        last_modified_website = get_last_modified(url)
        if last_modified_website != last_modified_seen:
            # Update file
            update_file(csv_filepath,
                        line_nr,
                        last_modified_website,
                        os.getpid())
            last_modified_seen = last_modified_website
            # notify
            sendmessage("Change detector",
                        "Change detected on <a href='{url}'>{name}</a>"
                        .format(url=url, name=name))
        # wait
        time.sleep(intervall)

        # See if the process should kill itself
        jobs = read_jobs(csv_filepath)
        if jobs[line_nr]['pid'] == 'commit_suicide':
            return


def update_file(csv_filepath, line_nr, last_modified_website, pid):
    # Race conditions!
    jobs = read_jobs(csv_filepath)
    print(jobs)
    jobs[line_nr]['last-modified'] = last_modified_website
    jobs[line_nr]['pid'] = pid
    with open(csv_filepath, 'w') as fp:
        writer = csv.writer(fp, delimiter=';')
        writer.writerow(["intervall", "name", "url", "last-modified", "pid"])
        for job in jobs:
            writer.writerow([job['intervall'],
                             job['name'],
                             job['url'],
                             job['last-modified'],
                             job['pid']])


def main():
    csv_filepath = "jobs.csv"
    jobs = read_jobs(csv_filepath)
    for line_nr, job in enumerate(jobs):
        process_runs = os.path.exists("/proc/{}".format(job['pid']))
        if job['pid'] == 'stopped' or not process_runs:
            create_new_process(csv_filepath, line_nr)
            time.sleep(1)
    while True:
        time.sleep(1)


if __name__ == '__main__':
    main()
