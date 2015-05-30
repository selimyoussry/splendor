#!flask/bin/python
import os
import shutil


appdbfile = 'app.db'
os.remove(appdbfile)
print 'File {} deleted'.format(appdbfile)

appdbdir = 'db_repository'
shutil.rmtree(appdbdir)
print 'Directory {} deleted'.format(appdbdir)