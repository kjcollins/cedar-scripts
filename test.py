def func1():
    print "this is func1"


def func2():
    print "this is func2"


def interface(self):
    key = raw_input("CEDAR account API key: ")
    website = raw_input("CEDAR host site name: ")
    search = raw_input("Search string in CEDAR: ")
    sort = raw_input("Sort type in CEDAR: ")
    db_name = raw_input("User Name (name of database): ")
    resource = raw_input("CEDAR resource type to use: ")
    resource_id = raw_input("Id of CEDAR resource to use: ")
    folder_id = raw_input("Id of folder to access in CEDAR: ")
    data_file = raw_input("Name of file on computer to use: ")


def main():
    func = func1
    print "func1"
    func()
    func = func2
    print "func2"
    func()

main()