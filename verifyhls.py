#!/usr/bin/python
import os, glob, subprocess, time

from hashlib import md5

dir = os.path.dirname(os.path.abspath(__file__))

def check(file):
   ts = None
   with open(file, 'r') as fr:
      for line in fr:
         if '.ts' in line:
            ts = line

   if ts is None:
      os.remove(file.replace('.m3u8','.mp4'))
      os.rename(file, '/path/to/verified/hls/%s' % os.path.basename(file))
      print('verifying %s completed!' % file)

def start():
   file = os.path.abspath(__file__)
   name = os.path.basename(file)
   hash = md5(file).hexdigest()
   this = file.replace(name, hash)

   print('script hash [%s]' % hash)

   if os.path.exists(this):
      age = time.time() - os.path.getmtime(this)
      if age > 300:
         os.remove(this)

      exit()

   open(this, 'w').close()

   files = glob.glob(os.path.join(dir, 'mp4', '*.m3u8'))

   for m3u8 in files:
      check(m3u8)

   os.remove(this)

start()