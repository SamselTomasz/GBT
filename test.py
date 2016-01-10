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
            td3 = full path to third, empty dir
            f3  = full path to third file

        Both files are filled with some sample text so their sizes are
        not equal to zero.
        """
        print '----------\nsetting up test directory'
        # get a current dir
        working_directory = os.getcwd()
        # creating main directory in current working path
        testdir = os.path.join(working_directory, "testdir")
        try:
            os.mkdir(testdir)
        except IOError, error:
            print "Cannot create directory '%s' : '%s'" % (testdir, error)
        # creating first file with some text in it
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
        # adding a subdir
        testdir2 = os.path.join(testdir, "subdir")
        try:
            os.mkdir(testdir2)
        except IOError, error:
            print "Cannot create directory '%s' : '%s'" % (testdir2, error)
        # .. and another sample file filled with a bit of text
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
        # new empty dir to work with as a backup path
        testdir3 = os.path.join(working_directory, 'testdir2')
        try:
            os.mkdir(testdir3)
        except IOError, error:
            print "Cannot create directory %s : %s" % (testdir3, error)
        # make a dictionary of paths to all of them
        self.test_info = {"wcd": working_directory, "td1": testdir,
                          "f1": file1, "td2": testdir2, "f2": file2,
                          "td3": testdir3}
        print '----------\n'

    def tearDown(self):
        """
        Cleaning up all created files and folders.
        """
        print '\n----------\ntearing down test directories'
        # just get rid of all the files and directories at once
        try:
            shutil.rmtree(self.test_info['td1'])
            shutil.rmtree(self.test_info['td3'])
        except IOError, error:
            print 'Couldnt delete test directory %s : %s' % (
                self.test_info['td1'], error)
        print '----------\n'


# ---------------------------------------------------------------------------
# create here all tests needed for local folder class
# pass LocalFolderSuper for setting up and tearing down test dirs
class LocalFolderTest (LocalFolderSuper):
    def runTest(self):

        print '\t----------\n\ttesting calling empty test object'

        # create an empty LF object
        test = LF.LocalFolder()

        # after creating an empty test LocalFolder object just check if
        # all fields are empty

        self.failUnless(test.items == [[], [], []],
                        "List of items isnt empty: %s" % test.items)
        self.failUnless(test.backup_local_path == "",
                        "Backup path isnt empty: %s" % test.backup_local_path)
        self.failUnless(test.backup_remote_path == "",
                        "Remote path isnt empty: %s" % test.backup_remote_path)

    # testing add_dir() method

        print '\t----------\n\ttesting LF.add_dir()'

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
        # another test
        print '\t----------\n\tna razie tyle\n\t----------'

    # testing rem_list_item()
        # check if function is working
        self.assertIs(test.rem_list_item(self.test_info['f3']), 'OK',
                      msg='Error while removing %s from list' % file3)
        # check if the function actually removed one item from the list
        self.assertEqual(len(test.items[0]), old_items_count,
                         msg='The lenght of the list is not the same')
        # check if the correct item was removed from list
        self.assertEqual(test.items.count(file3), 0,
                         msg='The file %s wasnt removed from list' % file3)


# ---------------------------------------------------------------------------
# set up the test suite
def suite():

    suite = unittest.TestSuite()
    # add all test to the test suite
    suite.addTest(LocalFolderTest())
    # return created test suite
    return suite

# ---------------------------------------------------------------------------
# and finally if test is run as main program, run test runner
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)
