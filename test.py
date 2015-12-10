# !/usr/bin/python
# coding=utf-8
import unitest
import LF
import os


class Local_Files_Test(unittest, TestCase):
    def setUp(self):
        """
        Testing GBT requires a sample directory tree and few files.
        Create test dir structure, which will be read, transfered to backup
        location, checked for changes and updated.

        Returns dictionary with:
            wcd = full path to working directory
            td1 = full path to first directory created
            f1  = full path to first file created
            td2 = full path to second directory created
            f2  = full path to second file created

        Both file are filled with some sample text so their sizes are
        not equal to zero.
        """
        working_directory = os.getcwd()
        testdir = os.path.join(working_directory, "testdir")
        try:
            os.mkdir(testdir)
        except IOError, error:
            print "Cannot create directory '%s' : '%s'" % (testdir, error)
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
        testdir2 = os.path.join(testdir, "subdir")
        try:
            os.mkdir(testdir2)
        except IOError, error:
            print "Cannot create directory '%s' : '%s'" % (testdir2, error)
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
        test_info = {"wcd": working_directory, "td1": testdir, "f1": file1,
                     "td2": testdir2, "f2": file2}
        return test_info

    def tearDown(self, test_info):
        "todo"
