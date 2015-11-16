# !/usr/bin/python
# coding=utf-8
import os
import time


class BackupFile:
    """
    This is a main class in this little backup tool. This is where a
    list of all backuped files with their status is held, as well
    as some other information, like the time of last modification
    and size of files. Apart of that, class hase fallowing fields:
        the_name    = name for this backup object, used for invoking
                      all operations on it, after its creation
        the_owner   = owner, creator of this very backup object
        the_comment = comment field you van fill for future references

    __init__(path, the_name, the_owner, the_comment)
        For initialization class needs path to directory which is
        about to be mirrored. Other atributes are optional.

    __list_dir__(dir_path)
        Private method, used to list all files in path directory
        and subdirectories. DO NOT USE

    __fill_table__()
        Fills table with name of file/dir, its size and date of
        last modification. DO NOT USE

    add_dir(path)
        Method invoked when the object is created. It runs list_dir()
        and get_attr() to update list of files. Checks if the path
        exists, and handles IO errors.

    add_file(path)
        Method invoked when a file is added to the list.

    rem_item(item_name)
        If on the list, this method will remove an item with corresponding
        atributes from self.items

    """

    def __init__(self, path, the_name="Change name", the_owner="Set owner",
                 the_comment="Set comment"):
        self.items = [[], [], []]
        created_on = time.ctime(time.time())
        name = the_name
        last_backup_date = ""
        owner = the_owner
        comment = the_comment
        self.info = [name, owner, created_on, last_backup_date, comment]

        return

    def __fill_table__(self, path):
        """
        This function fills table with file/dir name, its size and date
        of last modification.
        """
        self.items[0].append(path)
        self.items[1].append(os.path.getsize(path))
        self.items[2].append(time.ctime(os.path.getmtime(path)))

    def __list_dir__(self, dir_path):
        """
        This function lists all files in all subfolders in the
        folder given to the function.
        """
        def fill_items(arg, dir, files):
            for file in files:
                path = os.path.join(dir, file)
                path = os.path.normcase(path)
                self.__fill_table__(path)
        os.path.walk(dir_path, fill_items, 0)

    def add_dir(self, new_path):
        """
        This definition takes a full path to dir and lists its all
        files into a self.items. Then it checks file size and date
        of last modification.
        """
        try:
            if os.path.exists(new_path):
                self.__list_dir__(new_path)
            else:
                print "Entered path does not exist"
        except IOError:
            print "Cannot read from directory"

    def add_file(self, new_file):
        """
        Adds a single file to the backup list.
        """
        try:
            if os.path.exists(new_file):
                self.__fill_table__(new_file)
            else:
                print "Entered file doesnt exist."
        except IOError:
            print "Cannot access the file"

    def rem_item(self, item):
        """
        Removes an item and its coresponding atributes
        from the backup list.
        """
        try:
            index = self.items[0].index(item)
            self.items[0].pop(index)
            self.items[1].pop(index)
            self.items[2].pop(index)
        except ValueError:
            print "This item doesnt exist."
