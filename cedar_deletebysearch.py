#!/usr/bin/python

# August-2-2016
# cedar_deletebysearch.py: Script to search CEDAR and delete resources by their IDs found

import os
import argparse
import requests
import os.path
import sys
import json
# import jsclean
import time
import urllib
# from pymongo import MongoClient
#   from datetime import datetime
#   import sqlite3
# from collections import OrderedDict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--apiKey", help="authorization for upload to CEDAR", required=True)
    parser.add_argument("-n", "--hostName", help="site host name")
    parser.add_argument("-d", "--directory", help="directory to write to", required=True)
    parser.add_argument("-o", "--order", help="order of results: name, recently created, or recently updated",
                        required=True)
    parser.add_argument("-s", "--search", help="name of search string in CEDAR", required=False)
    parser.add_argument("-u", "--interface", help="toggle user interface", action='store_true')

    args = parser.parse_args()
    api_key = args.apiKey
    host_name = args.hostName
    directory = args.directory
    order = args.order
    search = args.search
    # ui = args.interface

    if not os.path.exists(directory):
        print "Output directory does not exist. Please try again."
        sys.exit()

    # call cedar delete the first time: need a response to check count
    url, parameter, headers = create_search_command(api_key, host_name, search, order)

    text = cedar_search(url, parameter, headers, directory)

    json_text = json.loads(text)
    total_count = json_text['totalCount']
    # print "success", total_count
    ids = []

    try:
        resources = json_text['resources']
        for j in range(len(resources)):
            resource_id = resources[j]['@id']
            if resources[j]['type'] != "folder":
                ids.append(resource_id)

    except KeyError:
        print ids
        print len(ids)
        print total_count
        exit()
    print ids
    exit()
    # print ids
    i = 0
    for instance in ids:
        # print instance
        url, headers = create_delete_command(api_key, host_name, instance)
        # print url
        # print headers
        r = requests.delete(url, headers=headers)
        if (int(r.status_code) != 204) or (str(r.status_code) != "204"):
            print r.status_code
        # print r.reason
        # print r.url
        # print r.text
        i += 1
        if (i % 15) == 0:
            print i

    print "done"
    print len(ids)
    print total_count

    # add limit and offset to params, limit stays 1000 while offset iterates--new call to create_command every loop
    # store each one in list then iterate through again?
    # probably instead: for each r.text returned, check # of resources, iterate through and get @ids of each

    # later, will iterate through @ids with delete (for old files) or get (with search app)

    # NEXT
    # delete each of ids
    # some way of checking what you delete?
    # for now I just want all the old instances gone
    # then: start developing the bigger project


def cedar_search(url, parameter, headers, directory):
    log_file = os.path.join(directory, "log.txt")
    recent_log = os.path.join(directory, "recent_log.txt")
    with open(recent_log, 'w') as log_r:
        log_r.write("")

    start = time.time()
    r = requests.get(url, params=parameter, headers=headers)
    #  print r.status_code
    #  print r.url

    write_2_logs(r.headers, log_file, recent_log)
    write_2_logs(r.url, log_file, recent_log)
    write_2_logs(r.status_code, log_file, recent_log)
    write_2_logs(r.reason, log_file, recent_log)
    # write_2_logs(r.text, log_file, recent_log)
    #  print r.text

    end = time.time()
    elapsed = end - start
    elapsed_message = "\nElapsed time: " + str(elapsed) + "\n"
    write_2_logs(elapsed_message, log_file, recent_log)
    write_2_logs("", log_file, recent_log)
    return r.text


def write_2_logs(text, log_1, log_2):
    text = str(text)
    with open(log_1, 'a') as log:
        with open(log_2, 'a') as log_r:
            log.write(text)
            log.write("\n")
            log_r.write(text)
            log_r.write("\n")


def create_delete_command(api_key, host_name, resource_id):
    # resource_id = resource_id.encode('utf-8')
    resource_id = urllib.quote_plus(resource_id)
    # print resource_id
    url = "https://" + host_name + "/template-instances/" + resource_id
    api_header = 'apiKey ' + api_key
    headers = {'Authorization': api_header}
    return url, headers


def create_search_command(api_key, host_name, search, sort):
    parameter = {'q': search, 'sort': sort, 'limit': 200000}
    url = "https://" + host_name + "/search-deep"
    api_header = 'apiKey ' + api_key
    headers = {'Content-Type': 'application/json', 'Authorization': api_header}
    return url, parameter, headers


if __name__ == "__main__":
    main()
