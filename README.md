# GBT

This is:
## Gumbas Backup Tool
Status:
under development

## Overview:
So what it does? Well, it is designed to keep local folder mirrored at some remote location. It can be another local folder, can be an FTP server, Google Drive, samba server in your local network etc. 

Why not use lftp for example? Because it will not run on Android! :) One of the goals of this program is to keep my files exactly the same across my devices. Some of them run Linux, some of them like my mobile phone or tablet run Android. This is why Python is my weapon of choice. Trying to keep it simple, extendable, scalable, and above all, usable :)

This is very very very! early version. Doesnt work yet. But work is in progress, please stay tuned :) 

## Whats working:

Not much :) Thats the best answear. 
So far i was able to create class to provide an access to files and directories on local file system. More to come.
Test suit created. Functions to deal with local files are working and passing all tests. 

## Whats to do:

A lot :) Again, early version, needs lots of work.

Starting from most important:
- the main program itself, providing backup functionality with existing access classes (so firstly it will mirror one local catalogue to another, then other locations will be available)
- tests. Running through other classes to come, its going to be easier to test bits and pieces (and much faster) with PyUnits doing some work for me :)
- ftp class. Will provide an access to ftp files.
- once ftp is up and runnig, my focus will go to change the way how the backup list are saved. So far pickling is in use. Want to change it to xml, as there will be more and more information to store, xml will be easier to modify/addjust to growing needs. 
- saving remote files in zip, tar, gzip etc files rather then keeping them in raw format. Password protection to the archive, etc.
- Google Drive
- Samba
- ?
- GUI? If i ever need this, i will implement it. But for the moment, its way down down the list of priorities ... :)

## Changelog:

### 18 Jan 2016
Still working on redesigning functions to work with dictionary rather then list. Finding bigger and smaller problems in the way the program seams to develop new functions and unctionalities :) Getting there though :)
### 11 Jan 2016
Ok. I took a look at the project and didnt like it :) So far its working, but its not working the way i want. Paths to all files and directories are kept i the list. All paths are absolute and remote dir path and local dir path are not used by functions in the LF class (i wanted to deal with absolute path in the main program). This is going to change. 
From now i will focus on:
- change the way paths to items are stored (i will use dictionary now)
- path will not be absolute, they will be relative to local dir path now
- i will need functions to split and join all paths
- i will have to redesign test suite, not only to check new functionalities but also put all function tests into seperate test instead keeping them all as part of one big test
### 11 Jan 2016
The whole LF (local folder access) was redesigned.
The testSuit was created.
While working on testSuit i realised that most of functions in LF have to be changed. All public functions return a status now. It is either a OK or error message that has to be handled by main program. The testSuit is checking now all functions in LF, all possible errors and scenerious i was able to come up with. But it has to be changed a bit. 
### 10 Dec 2015
Amount of functions and complication of setting up testing environment every time when something is changed made me think about test suit. The basic setup of local folders and files for test suit was added.
### ...
The local file and dir access created. Its running smooth. The functions of this class will be an outline for future classes, like ftp and samba access. This functions will have the same name across all classes, so no matter whats the destination dir, the main program will be able to use its basic commands to mirror files. This will provide scalability of program and its functions.
### Some time ago:
Came up with idea to create this program. Start working on outline to provide basic file and dir acces on local file system. With the time the basic functions of the class emerged.
