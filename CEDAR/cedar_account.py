# CEDAR class imports
import json
from pymongo import MongoClient
# import _tkinter
# import Tkinter
from cedar_request import Post, Search, Delete, Get, valid_resource


class CedarAccount:
    def __init__(self, api_key, host_name, sort):
        self.api_key = api_key
        self.host_name = host_name
        self.sort = sort

    def main_loop(self):
        raise NotImplementedError

    def update(self, new_file, folder):
        raise NotImplementedError

    def convert_cde_to_field(self):
        raise NotImplementedError


class CedarDirect(CedarAccount):
    def __init__(self, auth, site, sort, user=None):
        CedarAccount.__init__(self, auth, site, sort)
        self.user = user

    def main_loop(self):
        print self.user
        while True:
            print "Options:"
            print "1:\tSearch"
            print "2:\tPost"
            print "3:\tGet"
            print "4:\tDelete"
            print "5:\tQuit"
            choice = valid_input("Choice (#): ", ["1", "2", "3", "4", "5"], [Search, Post, Get, Delete, exit])
            if choice is "Quit":
                exit()
            if choice is Search:
                search_phrase = raw_input("search with: ")
                if search_phrase is "":
                    search_phrase = "*"
                Search(self.host_name, self.api_key, search_phrase, self.sort)

            if choice is Post:
                folder = raw_input("Folder id to post resource to: ")
                post_file = open(raw_input("JSON file to post: "), 'r+')
                text = post_file.read()
                json_text = json.loads(text)
                resource = get_resource_type(json_text)
                Post(self.host_name, self.api_key, folder, resource, text)
                post_file.close()

            if choice is Get:
                Get(self.host_name, self.api_key)

            if choice is Delete:
                print "If resource id is not known, search resource first!"
                print "Read id from local copy of resource, or enter id directly?"
                print "1:\tID from local copy"
                print "2:\tEnter ID directly"
                choice = valid_input("Choices (1 or 2: ", ["1", "2"], ["1,", "2"])
                if choice == 1:
                    delete_file = open(raw_input("Copy of the file to delete: "), 'r+')
                    text = delete_file.read()
                    json_text = json.loads(text)
                    resource = get_resource_type(json_text)
                    res_id = json_text["@id"]
                else:
                    res_id = raw_input("ID of JSON file to delete: ")
                    resource = valid_resource(raw_input("Resource_type: "))

                Delete(self.host_name, self.api_key, resource, res_id)

    def update(self, new_file, folder):
        print self.api_key

    def convert_cde_to_field(self):
        print self.api_key


class CedarDB(CedarAccount):
    def __init__(self, auth, site, sort, user):
        CedarAccount.__init__(self, auth, site, sort)
        self.client = MongoClient()

        self.username = user
        db = self.client[self.username]

        # print db.name
        # print db.count()

        files = db.dataset

        # print files.name
        # print files.database
        # print db.get_collection("dataset")
        # print files.count()

        # cde_string = open("/Users/kcollins/Documents/scripts/example_target_json/CEDARDataElement0_output.json", 'r')
        # print "open"
        # cde_string = cde_string.read()
        # print "read"
        # cde = json.loads(cde_string)
        # print "loaded"

        # insert_id = db.dataset.insert_one({"key": "value"})  #
        # insert_id = files.insert_one(cde)
        # print insert_id
        file_list = self.get_user_files(self.host_name, self.api_key)
        result = files.insert_many(file_list)
        print result.inserted_ids
        # print "done"

        self.user_files = files

    def main_loop(self):
        print self.username

    def get_user_files(self, site, auth):
        # print self.user_files

        text = Search(site, auth)

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

        files = []
        for instance in ids:
            r = Search(self.host_name, self.api_key, instance, "name")  # create get command
            # resp = r.request
            if r.success:
                json_file = json.loads(r.text)
                files.append(json_file)
        return files

    def update(self, new_file, folder):
        json_text = json.loads(new_file)
        file_id = json_text['@id']
        resource = get_resource_type(json_text)
        r = Delete(self.host_name, self.api_key, resource, file_id)
        # resp = r.request
        if r.success:
            r_update = Post(self.host_name, self.api_key, folder, resource, json_text)
            # resp = r_update.http_request()
            if not r_update.success:
                print "Update failed"
                exit()
        else:
            print "Delete failed"
            exit()

    def convert_cde_to_field(self):
        print self.api_key


def get_resource_type(item):
    # resources = ['Template', 'TemplateElement']
    try:
        res_type = item['@type']
    except KeyError:
        return 'template-instances'

    if str(res_type).endswith('Element'):
        return 'template-elements'
    elif str(res_type).endswith('Template'):
        return 'templates'


def valid_input(prompt, choices, labels):
    valid_choice = False
    choice = ""
    while valid_choice is False:
        choice = raw_input(prompt).strip()
        if choice not in choices:
            print "Try again"
        else:
            choice = labels[int(choice) - 1]
            valid_choice = True
    return choice
