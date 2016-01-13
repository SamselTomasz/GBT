# !/usr/bin/python
# coding=utf-8
import unittest
import LF
import os
import shutil
import sys


# ---------------------------------------------------------------------------
# LocalFolderSuper is preparing test directory with sample files and
# deletes it after the test are done
class LocalFolderSuper (unittest.TestCase):

    print '----------\nBegin testing LF'
    # this dictionary will be returned after a setUp()
    test_info = {}

    def setUp(self):

        """
        Testing LF requires a sample directory tree and few files.
        Create test dir structure, which will be read, transfered to backup
        location, checked for changes and updated.

        Returns dictionary with:
            wcd = full path to working directory
            td1 = full path to first directory created
            f1  = full path to first file created
            td2 = full path to second directory created
            f2  = full path to second file created
            td3 = full path to third dir
            td4 = full path to empty dir

        Dir tree:

            wcd
            |
            |___td1
            |   |___f1
            |   |
            |   |___td2
            |       |___f2
            |
            |___td3
            |
            |___td4

        Both files are filled with some sample text so their sizes are
        not equal to zero.
        """

        # wcd - current working directory
        working_directory = os.getcwd()

        # td1 - creating main directory in current working path
        # use as backup local path
        testdir = os.path.join(working_directory, "testdir")
        try:
            os.mkdir(testdir)
        except IOError, error:
            print "Cannot create directory '%s' : '%s'" % (testdir, error)

        # f1 - creating first file with some text in it
        file1 = os.path.join(testdir, "file1.txt")
        try:
            sample_file = file(file1, "w")
            sample_file.write("""
                              Sample line 1
                              Sample line 2
                              Sample line 3
                              """)
            del sample_file
        except IOError, error:
            print "Cannot create file '%s' : '%s'" % (file1, error)

        # td2 - adding a subdir
        testdir2 = os.path.join(testdir, "subdir")
        try:
            os.mkdir(testdir2)
        except IOError, error:
            print "Cannot create directory '%s' : '%s'" % (testdir2, error)

        # f2 - .. and another sample file filled with a bit of text
        file2 = os.path.join(testdir2, "file2.txt")
        try:
            sample_file = file(file2, "w")
            sample_file.write("""
                              Sample line x
                              Sample line y
                              Sample line z
                              Sample line a
                              Sample line b
                              Sample line c
                              """)
            del sample_file
        except IOError, error:
            print "Cannot create file %s : %s" % (file2, error)

        # td3 - new empty dir
        testdir3 = os.path.join(working_directory, 'testdir2')
        try:
            os.mkdir(testdir3)
        except IOError, error:
            print "Cannot create directory %s : %s" % (testdir3, error)

        # td4 - another empty dir
        # use it for remote path
        testdir4 = os.path.join(working_directory, 'testdir24')
        try:
            os.mkdir(testdir4)
        except IOError, error:
            print "Cannot create directory %s : %s" % (testdir4, error)

        # make a dictionary of paths to all of them
        self.test_info = {"wcd": working_directory, "td1": testdir,
                          "f1": file1, "td2": testdir2, "f2": file2,
                          "td3": testdir3, "td4": testdir4}

    def tearDown(self):

        """
        Cleaning up all created files and folders.
        """

        # just get rid of all the files and directories
        try:
            shutil.rmtree(self.test_info['td1'])
            shutil.rmtree(self.test_info['td3'])
            shutil.rmtree(self.test_info['td4'])
        except IOError, error:
            print 'Couldnt delete test directory %s : %s' % (
                self.test_info['td1'], error)


# ---------------------------------------------------------------------------
# create here all tests needed for local folder class
# pass LocalFolderSuper for setting up and tearing down test dirs

class CallEmptyTestObject (LocalFolderSuper):
    def runTest(self):
        print '\ttesting calling empty test object'

        # create an empty LF object
        test = LF.LocalFolder()

        # after creating an empty test LocalFolder object just check if
        # all fields are empty

        # check if items list is empty
        self.failUnless(test.items == {},
                        "List of items isnt empty: %s" % test.items)

        # check if backup_local_path is empty
        self.failUnless(test.backup_local_path == '',
                        "Backup path isnt empty: %s" % test.backup_local_path)

        # check if backup_remote_path is empty
        self.failUnless(test.backup_remote_path == '',
                        "Remote path isnt empty: %s" % test.backup_remote_path)


class CallFilledTestObject (LocalFolderSuper):
    def runTest(self):
        print '\ttesting calling test object with data passed'

        # create filled LF object
        items = {'item1': 'value1', 'item2': 'value2'}
        local_path = '/local/path'
        remote_path = '/remote/path'

        # call filled LF
        test = LF.LocalFolder(items, local_path, remote_path)

        # lets check if everything is ok, compare values from object
        # with their passed values

        # check items list first
        self.failUnless(test.items == {'item1': 'value1', 'item2': 'value2'},
                        "Passed values from items list didnt mach")

        # check local_path
        self.failUnless(test.backup_local_path == '/local/path',
                        "Passed value from backup_local_path didnt match")

        # check remote_path
        self.failUnless(test.backup_remote_path == '/remote/path',
                        "Passed value from backup_remote_path didnt match")

        # check if we can access single item from items list
        self.failUnless(test.items['item1'] == 'value1',
                        "Single item from dictionary of items didnt match")


class __path_split__Test (LocalFolderSuper):
    def runTest(self):
        print '\ttesting __path_split__()'

        # create filled LF object
        local_path = '/local/path'
        remote_path = '/remote/path'
        local_split = '/local/path/split/this.file'
        remote_split = '/remote/path/split/this.file'
        split = 'split/this.file'
        # call filled LF
        test = LF.LocalFolder(local_path=local_path, remote_path=remote_path)

        # split local_split using local_path form test object
        self.assertEqual(test.__path_split__(test.backup_local_path,
                                             local_split),
                         split,
                         msg='Splitting folder using local path didnt work')

        # split remote
        self.assertEqual(test.__path_split__(test.backup_remote_path,
                                             remote_split),
                         'split/this.file',
                         msg='Splitting folder using remote path didnt work')

        # handle error
        self.assertIs(test.__path_split__(test.backup_remote_path,
                                          '/bad/path'),
                      'Error',
                      msg="Function didnt handle bad path")


class __path_join__Test (LocalFolderSuper):
    def runTest(self):
        2+2


class LocalFolderTest (LocalFolderSuper):
    def runTest(self):

        print '\n\n\n\t---------- old tests ----------'
        print '\t----------\n\ttesting LF.add_dir()'

        test = LF.LocalFolder

        # adding content of test dir 1
        self.assertIs(test.add_dir(self.test_info['td1']), 'OK',
                      msg='Didnt list existing directory')
        # have a look if list isnt still empty
        self.failIf(test.items == [[], [], []],
                    "LF.add_dir didnt list dir %s" % self.test_info['td1'])
        # check if the first item on the list match the first test file
        self.failUnless(test.items[0][0] == self.test_info['f1'],
                        "Listed file doesnt mach: %s\n%s" %
                        (test.items[0][0], self.test_info['f1']))
        # adding not existing dir
        self.assertIsNot(test.add_dir('/this/dir/doesnt/exist'), 'OK',
                         msg='Listed not existing file')

    # testing add_list_item() method

        # lets create new not listed file
        print '\t----------\n\ttesting LF.add_list_item()'
        file3 = os.path.join(self.test_info['td3'], "file3.txt")
        try:
            sample_file = file(file3, "w")
            sample_file.write("""
                              Sample line xx
                              Sample line yy
                              Sample line zz
                              Sample line aa
                              Sample line bb
                              Sample line cc
                              """)
            del sample_file
        except:
            print "Cannot create file %s : %s" % (file3, sys.exc_info())

        # fill in test_info with a name of new file
        self.test_info.update({'f3': file3})

        # now do the test
        # save how many items is on the list
        old_items_count = len(test.items[0])
        # check if adding went without errors
        self.assertIs(test.add_list_item(self.test_info['f3']), 'OK',
                      msg='Error adding %s' % file3)
        # check if list is longer by one
        self.assertTrue(old_items_count == len(test.items[0]) - 1,
                        msg="Didnt add %s to the list of items" % file3)
        # check if path of file is of the string type
        self.failUnless(type(test.items[0][old_items_count]) == str,
                        "Didnt list path attribute of new file %s" % file3)
        # check if it matchs the actual path of the file
        self.assertIs(test.items[0][-1], file3, msg='Path is wrong')
        # check if the size was updated
        self.failUnless(type(test.items[1][old_items_count]) == long,
                        "Dindt list size attribute of new file %s" % file3)
        # check if the date was updated
        self.failUnless(type(test.items[2][old_items_count]) == str,
                        "Didnt list date attribute of new file %s" % file3)
        # try to add file that doesnt exist
        self.assertIsNot(test.add_list_item('/file/doesnt/exist'), 'OK',
                         msg='Error while adding not existing folder')
        # try to add items thats already on the list
        self.assertIsNot(test.add_list_item(test.items[0][old_items_count]),
                         'OK', msg='No error while adding existing item')

    # testing rem_list_item()

        print '\t----------\n\ttesting LF.rem_list_item()'
        # check if function is working
        self.assertIs(test.rem_list_item(self.test_info['f3']), 'OK',
                      msg='Error while removing %s from list' % file3)
        # check if the function actually removed one item from the list
        self.assertEqual(len(test.items[0]), old_items_count,
                         msg='The lenght of the list is not the same')
        # check if the correct item was removed from list
        self.assertEqual(test.items.count(file3), 0,
                         msg='The file %s wasnt removed from list' % file3)

    # testing copy_to_remote()

        print '\t----------\n\ttesting LF.copy_to_remote()'
        # lets prepare few variables, for the file first
        local_item = self.test_info['f1']
        file_name = os.path.split(local_item)[1]
        remote_item = os.path.join(self.test_info['td3'], file_name)
        # try to copy a file
        self.assertIs(test.copy_to_remote(local_item, remote_item), 'OK',
                      msg='Error while copying file')
        # check if the file was copied
        self.assertTrue(os.path.exists(remote_item),
                        msg='The file %s wasnt copied to %s' % (
                            local_item, remote_item))
        # lets see how it handles not existing file
        self.assertIsNot(test.copy_to_remote('/fake/file', remote_item), 'OK',
                         msg='No error while copying not existing file')
        # update test_info with remote file
        self.test_info.update({'rf': remote_item})

        # lets try how its working with directories
        # first create another dir
        remote_dir = os.path.join(self.test_info['td3'], os.path.split(
            self.test_info['td4'])[1])
        # and copy (create) dir in remote location
        self.assertIs(test.copy_to_remote(self.test_info['td4'], remote_dir),
                      'OK', msg='Error copying directory')
        # check if the dir was actually created
        self.assertTrue(os.path.exists(remote_dir),
                        msg='Directory wasnt created')
        # and dir that doesnt exist
        self.assertIsNot(test.copy_to_remote('/some/dir', '/not/existing/dir'),
                         'OK', msg='Function didnt handle not existing dir')

    # testing copy_from_remote()

        print '\t----------\n\ttesting LF.copy_from_remote()'
        # first delete empty folder to make room for tests and create short
        # names for remote and local items
        try:
            shutil.rmtree(remote_dir)
        except:
            print 'Couldnt delete %s' % remote_dir
        self.assertFalse(os.path.exists(remote_dir))
        local_item = remote_dir
        remote_item = self.test_info['td4']
        # lets test these directories first
        self.assertIs(test.copy_from_remote(remote_item, local_item), 'OK',
                      msg='Error while copying dir')
        # check if dir was created
        self.assertTrue(os.path.exists(local_item), msg='Dir wasnt created.')
        # check how it handles not existing dir
        self.assertIsNot(test.copy_from_remote('/some/dir', '/not/existing'),
                         'OK', msg='Function didnt handle not existing folder')
        # what if directories exist?
        self.assertIs(test.copy_from_remote(remote_item, local_item), 'OK',
                      msg='Error while copying dir')

        # now for files, set up some variables
        remote_item = self.test_info['f1']
        file_name = os.path.split(remote_item)[1]
        local_item = os.path.join(self.test_info['td3'], file_name)
        if os.path.exists(local_item):
            try:
                os.remove(local_item)
            except:
                print 'Couldnt delete %s' % (local_item)
        # now do the test for files
        self.assertIs(test.copy_from_remote(remote_item, local_item), 'OK',
                      msg='Error while copying file')
        # check if file was actually copied
        self.assertTrue(os.path.exists(local_item), msg='File wasnt copied')

    # testing delete_item()

        print '\t----------\n\ttesting LF.delete_item()'
        # check if the file exists first before we go any further
        item_path = self.test_info['f1']
        self.assertTrue(os.path.exists(item_path))
        # check the function with existing file
        self.assertIs(test.delete_item(item_path), 'OK',
                      msg='Didnt delete file %s' % item_path)
        # check if it worked
        self.assertFalse(os.path.exists(item_path),
                         msg='File wasnt deleted')
        # check it for file that doesnt exist
        self.assertIs(test.delete_item('/some/dir/or/file'), 'OK',
                      msg='Didnt handle not existing file')
        # check the function with folders
        item_path = self.test_info['td2']
        self.assertIs(test.delete_item(item_path), 'OK',
                      msg='Error deleting folder')
        # lets have a look was the folder actually deleted
        self.assertFalse(os.path.exists(item_path),
                         msg='Folder wasnt deleted')

    # testing save_backup_list()

        print '\t----------\n\ttesting LF.save_backup_list()'
        # lets prepare the path for save file
        file_path = os.path.join(self.test_info['td3'], 'save')
        # check saving function
        self.assertIs(test.save_backup_list(file_path), 'OK',
                      msg='Error while saving backup object')
        # see if pickle was created
        self.assertTrue(os.path.exists(file_path),
                        msg='Pickle wasnt created')
        # pickle second time
        self.assertIs(test.save_backup_list(file_path), 'OK',
                      msg='Error while saving backup object')

    # testing load_backup_list()

        print '\t----------\n\ttesting LF.load_backup_list()'
        # as we know the backup file was created, lets create a backup
        # of object itself, delete it, load it from pickle and
        # compare if they are the same
        test_backup = test
        self.assertEqual(test, test_backup,
                         msg='Copied objects are not equal')
        del(test)
        test = LF.LocalFolder()
        self.assertIs(test.load_backup_list(file_path), 'OK',
                      msg='Error loading pickled file')
        # and compare loaded object and saved one
        self.assertEqual(test.items, test_backup.items,
                         msg='Loaded object isnt the same')
        # was the pickle file deleted?
        self.assertTrue(os.path.exists(file_path),
                        msg='The pickle file is missing')


# ---------------------------------------------------------------------------
# set up the test suite
def suite():

    suite = unittest.TestSuite()
    # add all test to the test suite
    suite.addTest(CallEmptyTestObject())
    suite.addTest(CallFilledTestObject())
    suite.addTest(__path_split__Test())
    suite.addTest(__path_join__Test())
    # below old test -- need to change them after redesigning functions
    suite.addTest(LocalFolderTest())
    # return created test suite
    return suite

# ---------------------------------------------------------------------------
# and finally if test is run as main program, run test runner
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
