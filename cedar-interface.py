#!/usr/bin/python

import re
from CEDAR.cedar_account import CedarDirect, CedarDB, valid_input


class MainInterface:
    def __init__(self):
        self.host = site_name()
        self.account = account_type()
        self.user = None
        if self.account is CedarDB:
            self.user = username()
        self.key = user_api_key()
        self.sort_dir = sort()
        db = self.account(self.key, self.host, self.sort_dir, self.user)
        db.main_loop()

#   INTERFACE FUNCTIONS   ######################


def sort():
    print "What direction would you like any resources to be listed?"
    print "1:\tname"
    choice = "name" # valid_input("Choices (1): ", ["1"], "name")
    return choice


def user_api_key():
    valid_choice = False
    key = ""
    while valid_choice is False:
        key = "c0bfec41-23e9-433a-950e-1cbd1cf3080f" # raw_input("api key: ")
        reg = re.compile("\w{8}\-\w{4}\-\w{4}\-\w{4}\-\w{12}")
        if reg.match(key):
            valid_choice = True
        else:
            print "Try again"
    return key


def username():
    print "Please enter credentials for CEDAR account\n"
    user = "kcollins" # raw_input("username: ").replace(" ", "_").replace("\t", "").replace("\n", "")
    return user


def account_type():
    print "Would you like to interact make requests directly to your account, or download your account files to " \
          "interact with locally?"
    print "1:\tDirect access"
    print "2:\tLocal use"
    account = CedarDB # valid_input("Choice (1 or 2): ", ["1", "2"], [CedarDirect, CedarDB])

    return account


def site_name():
    print "Welcome to CEDAR \n"
    print "Which host name are you using?"
    print "1:\tresource.metadatacenter.net"
    print "2:\tresource.staging.metadatacenter.net"
    print "3:\tother\n"
    main = "resource.metadatacenter.net"
    staging = "resource.staging.metadatacenter.net"
    choice = "resource.staging.metadatcenter.net" # valid_input("Choice (1, 2, or 3): ", ['1', '2', '3'], [main, staging, "3"])

    if choice == "3":
        host = "resource.metadatacenter.net" # raw_input("Other host name (warning--may not work as intended): ")
    else:
        return choice

    return host


##############################################################################################

if __name__ == "__main__":
    print "main"
    # r = Request("delete")
    MainInterface()
    exit()

    dbs = CedarDB("key", "site", "name", "user")
    print dbs
    print dbs.user_files
    # cursor = dbs.user_files.find({"origin": { $exists: true }})
    cursor = dbs.user_files.find({"_templateId":
                                  "https://repo.metadatacenter.net/templates/f9d107b3-c587-4db3-a1b4-0e21ccd14997"},
                                 {"origin._value": 1})
    for document in cursor:
        print document
    # print dbs.user_files.count()
    print dbs.client
    # print dbs.client.count()
