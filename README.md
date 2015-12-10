# GBT

This is:
## Gumbas Backup Tool

So what it does? Well, it is designed to keep local folder mirrored at some remote location. It can be another local folder, can be an FTP server, Google Drive, samba server in your local network etc. 

Why not use lftp for example? Becouse it will not run on Android! :) One of the goals of this program is to keep my file exactly the same across my devices. Some of them run Linux, some of the like my mobile phone or tablet run Android. This is why Python is my weapon of choice. Trying to keep it simple, extendable, scalable, and above all, usable :)

This is very very very! early version. Doesnt work yet. But work is in progress, please stay tuned :) 

## Whats working:

Not much :) Thats the best answear. 
So far i was able to create class to provide an access to files and directries on local file system. More to come.

## Whats to do:

A lot :) Again, early version, needs lots of work.

Starting from most important:
- the main program itself, providing backup functionality with existing access classes (so firstly it will mirror one local catalogue to another, then other locations will be available)
- tests. Running thru other classes to come, its going to be easier to test bits and pieces (and much faster) with PyUnits doing some work for me :)
- ftp class. Will provide an access to ftp files.
- once ftp is up and runnig, my focus will go to change the way how the backup list are saved. So far pickling is in use. Want to change it to xml, as there will be more and more information to store, xml will be easier to modify/addjust to growing needs. 
- saving remote files in zip, tar, gzip etc files rather then keeping them in raw format. Password protection to the archive, etc.
- Google Drive
- Samba
- ?
- GUI? If i ever need this, i will implement it. But for the moment, its way down down the list of priorities ... :)
