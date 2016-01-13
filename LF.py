# !/usr/bin/python
# coding=utf-8
import os
import time
import shutil
import pickle
import sys


class LocalFolder:
    """
    This is a generic class supporting access to local files and folders.
    Supporting reading folder content, copying and removing files and folders,
    adding and removing elements of the list and saving to and reading list
    from file (for the moment just a pickle option implemented, work on xml
    file support in progress)
    It reads the catalogue contents, fills in the table with elements
    properties as size of file and the date of modification and provides
    api for working with listed elements and the list itself.

    The list of elements is stored in:
        self.items.
    It also stores the path to local and remote catalogue:
    (note, remote catalogue is needed only if mirroring to local file system)
        self.backup_local_path
        self.backup_remote_path

    Class hases methods are as fallows:

        __fill_table__(path_item)
            - internall method used to fill lists elements
            Do not use!

        __list_dir__(dir_path)
            - internall method used to return a folder content
            Do not use!

        add_dir(dir_path)
            - fills items list with directory content.

        add_list_items(new_file)
            - adds a single file or directory to list of items

        rem_list_item(item)
            - removes as item and its atributes from items list

        copy_to_remote(local_item, remote_item)
            - copy local file or directory to remote location

        copy_from_remote(remote_item, local_item)
            - copy remote file or directory to local location

        delete_item(item_path)
            - delete file or directory from local file system

        save_backup_list(save_file)
            - save list of items and paths to local and remote directory

        load_backup_list(save_file)
            - load saved list of items and paths
    """

    # setup some starting parameters
    items = {}
    backup_local_path = ''
    backup_remote_path = ''

    def __init__(self, items=items, local_path=backup_local_path,
                 remote_path=backup_remote_path):
        self.items = items
        self.backup_local_path = local_path
        self.backup_remote_path = remote_path
        return

    def __path_split__(self, directory, path):
        if path != '' and directory != '':
            if isinstance(path, str):
                splited = path.split(directory)
                if len(splited) == 2:
                    splited = splited[1][1:]
                else:
                    splited = 'Error'
            else:
                splited = 'Error'
        else:
            splited = 'Error'
        return splited

    def __fill_table__(self, path_item):
        """
        This function fills table with file/dir name, its size and date
        of last modification.
        Takes one argument, the full path to a file or directory.
        Do not use on its own!
        """
        self.items[0].append(path_item)
        self.items[1].append(os.path.getsize(path_item))
        self.items[2].append(time.ctime(os.path.getmtime(path_item)))

    def __list_dir__(self, dir_path):
        """
        This method lists all files in all subfolders in the
        folder given to the function.
        Takes one argument, a full path to a directory.
        """

        def fill_items(arg, dir, files):
            for file in files:
                path = os.path.join(dir, file)
                path = os.path.normcase(path)
                self.__fill_table__(path)
        os.path.walk(dir_path, fill_items, 0)

    def add_dir(self, new_path):
        """
        This method takes a full path to directory and lists its all
        files into a self.items object. Then it checks file size and date
        of last modification and stores them along with file/dir path.
        Takes full path to directory as an argument.
        """
        status = 'OK'
        if os.path.exists(new_path):
            try:
                self.__list_dir__(new_path)
            except:
                status = sys.exc_info()
        else:
            status = 'File %s doesnt exist.' % new_path
        return status

    def add_list_item(self, new_file):
        """
        Adds a single item to the backup list.
        Checks items atributes after adding it to the list.
        Takes a full path to an item as argument.
        """
        status = 'OK'
        if self.items[0].count(new_file) == 0:
            if os.path.exists(new_file) is True:
                try:
                    self.__fill_table__(new_file)
                except:
                    status = sys.exc_info()
            else:
                status = 'Cannot read file %s' % new_file
        else:
            status = 'File %s already listed' % new_file
        return status

    def rem_list_item(self, item):
        """
        Removes an item and its coresponding atributes
        from the backup list.
        Takes a full path to a file/dir as atribute.
        """
        status = 'OK'
        if self.items[0].count(item) != 0:
            try:
                index = self.items[0].index(item)
                self.items[0].pop(index)
                self.items[1].pop(index)
                self.items[2].pop(index)
            except:
                status = sys.exc_info()
        else:
            status = 'An item %s is not on the list' % item
        return status

    def copy_to_remote(self, local_item, remote_item):
        """
        Copy local file or directory to remote server.
        Takes two atributes, full paths to local file/dir as the one to copy,
        and full path to remote file/dir as destination.
        Does not dive into subdirs!
        If directory name passed, method only creates a directory on remote
        location, nothing more.
        Files and subdirs in it must be copied on them own.
        """
        status = 'OK'
        if os.path.exists(local_item):
            if os.path.isfile(local_item):
                try:
                    shutil.copy2(local_item, remote_item)
                except:
                    status = sys.exc_info()
            elif os.path.isdir(local_item):
                if not os.path.exists(remote_item):
                    try:
                        os.mkdir(remote_item)
                    except:
                        status = sys.exc_info()
            else:
                status = 'The item %s is not dir or file' % local_item
        else:
            status = 'File %s doesnt exist and cannot be copy' % local_item
        return status

    def copy_from_remote(self, remote_item, local_item):
        """
        Copy remote file or directory to local location.
        Takes two atributes, full path to remote file/dir as the one to copy,
        and full path to local file/dir as destination.
        Does not dive into subdirs!
        If directory name passed, method only creates a directory on local
        location, nothing more.
        Files and subdirs in it must be copied on them own.

        """
        status = 'OK'
        if os.path.exists(remote_item):
            if os.path.isfile(remote_item):
                try:
                    shutil.copy2(remote_item, local_item)
                except:
                    status = sys.exc_info()
            elif os.path.isdir(remote_item):
                if not os.path.exists(local_item):
                    try:
                        os.mkdir(local_item)
                    except:
                        status = sys.exc_info()
            else:
                status = 'The item %s is not a dir or file.' % remote_item
        else:
            status = 'File %s doesnt exist and cannot be copy' % remote_item
        return status

    def delete_item(self, item_path):
        """
        Deletes file or directory.
        Takes one argument, full path to an item.
        """
        status = 'OK'
        if os.path.exists(item_path):
            if os.path.isfile(item_path):
                try:
                    os.remove(item_path)
                except:
                    status = sys.exc_info()
            elif os.path.isdir:
                try:
                    shutil.rmtree(item_path)
                except:
                    status = sys.exc_info()
            else:
                status = 'The item %s is not a dir or a file' % item_path
        return status

    def save_backup_list(self, save_file):
        """
        Saves created/updated list of items and local and remote paths.
        Takes a full path to the file as an argument!
        """
        status = 'OK'
        try:
            save_data = [[self.items], [self.backup_local_path],
                         [self.backup_remote_path]]
            pickle_file = file(save_file, "w")
            pickle.dump(save_data, pickle_file)
        except:
            status = sys.exc_info()
        return status

    def load_backup_list(self, save_file):
        """
        Loads saved list of items and local and remote paths.
        Takes a full path to the file as an argument!
        """
        status = 'OK'
        try:
            pickle_file = file(save_file)
            [[self.items], [self.backup_local_path],
             [self.backup_remote_path]] = pickle.load(pickle_file)
        except:
            status = sys.exc_info()
        return status

if __name__ == '__main__':
    print 'This class is not a standalone program'
