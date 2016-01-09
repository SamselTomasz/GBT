# !/usr/bin/python
# coding=utf-8
import unittest
import LF
import os
import shutil


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
        test.add_dir(self.test_info['td1'])
        self.failIf(test.items == [[], [], []],
                    "LF.add_dir didnt list dir %s" % self.test_info['td1'])
        self.failUnless(test.items[0][0] == self.test_info['f1'],
                        "Listed file doesnt mach: %s\n%s" %
                        (test.items[0][0], self.test_info['f1']))
        # adding not existing dir
        self.assertRaises(IOError, test.add_dir('/this/dir/doesnt/exist'))

    # testing add_list_item method
        # lets create new not listed yet file
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
        except IOError, error:
            print "Cannot create file %s : %s" % (file3, error)
        self.test_info.update({'f3': file3})
        # now do the test
        old_items_count = len(test.items[0])
        test.add_list_item(self.test_info['f3'])
        self.failUnless(old_items_count == len(test.items[0]) - 1,
                        "Didnt add %s to the list of items" % file3)
        self.failUnless(type(test.items[0][old_items_count]) == str,
                        "Didnt list path attribute of new file %s" % file3)
        self.failUnless(type(test.items[1][old_items_count]) == long,
                        "Dindt list size attribute of new file %s" % file3)
        self.failUnless(type(test.items[2][old_items_count]) == str,
                        "Didnt list date attribute of new file %s" % file3)
        # try to add file that doesnt exist
# --- tu sie bije
        self.assertRaises(OSError, test.add_list_item('/file/doesnt/exist'))
        self.assertRaises(OSError, test.add_list_item('fuck'))
        # try to add items thats already on the list
        self.assertRaisesRegexp(ValueError, test.add_list_item(
            test.items[0][old_items_count]))
        # another test
        print '\t----------\n\tna razie tyle\n\t----------'


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
