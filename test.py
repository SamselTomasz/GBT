# !/usr/bin/python
# coding=utf-8
import unitest
import Bf
import os


class Local_Files_Test(unittest, TestCase):
    def setUp(self):
        """
        Testing BackupFile requires a sample directory tree and few files.
        Create test dir structure, which will be read, transfered to backup
        location, checked for changes and updated.
        """
        path = os.getcwd()

    def tearDown(self):
        print "Cleaning directory structure"
