#!/usr/bin/python

# July-28-2016
# jsonparse.py: Script to search through any json document using the dict created with json module

import json
import argparse
import os
import sys
import jsclean
from collections import OrderedDict
# should probably have class with the search method, so then a search for key or value can be called/imported/etc
# this isn't as useful because part of the point is searching through a database


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", help="If included, input is a directory.", action='store_true')
    group.add_argument("-f", "--file", help="If included, input is a file.", action='store_true')
    parser.add_argument("-i", "--input", help="JSON file or directory to process. Use absolute path for directory.",
                        required=True)
    args = parser.parse_args()

    input_files = []
    directory = args.directory
    args_file = args.file
    json_input = args.input

    if directory:
        if not os.path.exists(json_input):
            print "Input directory does not exist. Please try again."
            sys.exit()

        input_files = jsclean.directory_walk(json_input)
        # print "input files:", input_files

    elif args_file:
        if jsclean.valid_json_file(json_input, "input"):
            input_files.append(args.input)

    # search_dict(input_files)
    for i in range(len(input_files)):
        f = open(os.path.abspath(input_files[i]), 'r+')
        new = JSONDict(f)
        print "keys", new.keys
        print "values", new.values


class JSONDict:
    def __init__(self, file_object):
        self.data = json.load(file_object)
        self.keys = self.data.keys()
        self.values = self.data.values()

    def search(self):
        if self.keys.hasattr("strip"):
            print


def file_check(f_input):
    json_list = []
    f = open(os.path.abspath(f_input), 'r+')
    for line in f.readlines():
        file_line = line.strip()
        json_list.append(file_line)
    string_file = "".join(json_list)
    f.seek(0)
    check_file = json.dumps(json.load(f, object_pairs_hook=OrderedDict), separators=(',', ': '))
    if string_file == check_file:
        print "true"
        return True
    return False


if __name__ == "__main__":
    main()
