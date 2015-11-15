# !/usr/bin/python
# coding=utf-8
import os
import time


class BackupFile:
    """
    This is a main class in this little backup tool. This is where a
    list of all backuped files with their status is held, as well
    as some other information. More on it soon.
    """

    def __init__(self, the_name = "Change name", the_owner = "Set owner",
                 the_comment = "Set comment", path):
        self.items = [[], [], []]
        created_on = time.ctime(time.time())
        name = the_name
        last_backup_date = ""
        owner = the_owner
        comment = the_comment
        self.info = [name, owner, created_on, last_backup_date, comment]

        return

    def list_dir(self, dir_path):
        """
        This function lists all files in all subfolders in the
        folder given to the function.
        """
        def fill_items(arg, dir, files):
            for file in files:
                path = os.path.join(dir, file)
                path = os.path.normcase(path)
                self.items[0].append(path)

        os.path.walk(dir_path, fill_items, 0)

    def get_attr(self):
        """
        Takes all files listed, and checks its size and
        date of last modification.
        """
        #if self.items[0] != []:
        #    for path in self.items[0]:
        #        self.items[1].append(os.path.getsize(path))
        #        self.items[2].append(time.ctime(os.path.getmtime(path)))
        # This method wasn't good, as it didnt allow you to change
        # the list of files. New attributes was added to the end of
        # the list. Messy. Lets do it the proper way.

    def add_dir(self, new_path):
        """
        This definition takes a full path to dir and lists its all
        files into a self.items. Then it checks file size and date
        of last modification.
        """
        try:
            if os.path.exists(new_path):
                self.list_dir(new_path)
                self.get_attr()
            else:
                print "Entered path does not exist"
        except IOError:
            print "Cannot read from directory"

    def add_file(self, new_file):
        print "Little to do here, change the get_attr() first"
