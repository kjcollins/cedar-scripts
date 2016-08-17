# REQUESTS class imports
import requests
import urllib


class CedarRequest:
    def __init__(self, host_name, api_key):
        self.site = host_name
        self.auth = api_key
        self.request = self.http_request()
        self.text = self.request.text
        self.success = request_success(self.request.status_code)

    def http_request(self):
        raise NotImplementedError


class Delete(CedarRequest):
    def __init__(self, host_name, api_key, resource_type, resource_id):
        CedarRequest.__init__(self, host_name, api_key)
        self.type = valid_resource(resource_type)
        self.resource = urllib.quote_plus(resource_id)

    def http_request(self):
        url = "https://" + self.site + "/" + self.type + "/" + self.resource
        api_header = 'apiKey ' + self.auth
        headers = {'Authorization': api_header}
        delete_request = requests.delete(url, headers=headers)
        return delete_request


class Search(CedarRequest):
    def __init__(self, host_name, api_key, search=None, sort=None):
        if search is None:
            self.search_string = "*"
        else:
            self.search_string = search

        if sort is None:
            self.sort_dir = "name"
        else:
            self.sort_dir = sort
        CedarRequest.__init__(self, host_name, api_key)

    def http_request(self):  # q = self.search_string
        parameter = {'q': "CDE_*", 'sort': self.sort_dir, 'limit': 200000}
        url = "https://" + self.site + "/search-deep"
        api_header = 'apiKey ' + self.auth
        headers = {'Content-Type': 'application/json', 'Authorization': api_header}
        search_request = requests.get(url, params=parameter, headers=headers)
        return search_request
        # return url, parameter, headers


class Post(CedarRequest):
    def __init__(self, host_name, api_key, folder_id, resource_type, data):
        CedarRequest.__init__(self, host_name, api_key)
        self.folder = folder_id
        self.type = valid_resource(resource_type)
        self.json_data = data

    def http_request(self):
        parameter = {'folderId': self.folder}
        url = "https://" + self.site + "/" + self.type
        api_header = 'apiKey ' + self.auth
        headers = {'Content-Type': 'application/json', 'Authorization': api_header}
        post_request = requests.post(url, params=parameter, data=self.json_data, headers=headers)  # make request
        return post_request
        # return url, parameter, headers


class Update(CedarRequest):
    def __init__(self, host_name, api_key):
        CedarRequest.__init__(self, host_name, api_key)

    def http_request(self):
        print self.auth
        # call to search by template id (or not?)
        # call to delete
        # call to post
        # or neither: and just return 2 commands


class Get(CedarRequest):
    def __init__(self, host_name, api_key):
        CedarRequest.__init__(self, host_name, api_key)

    def http_request(self):
        print self.auth


#   UTIL FUNCTIONS   #########################
def valid_resource(item):
    resource_list = ['template-elements', 'template-fields', 'template-instances', 'templates']
    if item in resource_list:
        return item
    else:
        print "invalid resource"
        exit()


def request_success(status):
    if not str(status).startswith("2"):
        print "error: failed request"
        print status.reason
        print status.url
        print status.text
        return False
    else:
        return True
