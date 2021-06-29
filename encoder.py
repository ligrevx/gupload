#!/usr/bin/python

import os, glob, subprocess, time

from hashlib import md5
from random import randint

dir = os.path.dirname(os.path.abspath(__file__))

def generatehls(file):
   hlsfile = file.replace('.mp4','.m3u8')
   segfile = file.replace('.mp4','_%03d.ts')
   subprocess.check_output(['ffmpeg3', '-hide_banner', '-y', '-i', file, '-profile:v', 'baseline', '-level', '3.0', '-s', '640x360', '-start_number', '0', '-hls_time', '4', '-hls_list_size', '0', '-hls_segment_filename', segfile, '-f', 'hls', hlsfile])

def generatejpg(mp4):
   jpg = mp4.replace('/mp4/','/jpeg/').replace('.mp4','.jpg')
   tss = randint(10,30)

   subprocess.check_output(['ffmpeg3', '-hide_banner', '-y', '-ss', str(tss), '-i', mp4, '-s', '640x360', '-vframes', '1', jpg])

   if os.path.exists(jpg): os.remove(mp4)

def generatepng(file):   
   hlsfile = file.replace('.mp4','.m3u8')
   segfile = file.replace('.mp4','_%03d.ts')
   try:
      subprocess.check_output(['ffmpeg3', '-hide_banner', '-y', '-i', file, '-profile:v', 'baseline', '-s', '640x360', '-level', '3.0', '-start_number', '0', '-hls_time', '5', '-hls_list_size', '0', '-hls_segment_filename', segfile, '-f', 'hls', hlsfile])

   except:
      print('error generating hls %s' % file)

def main():
   file = os.path.abspath(__file__)
   name = os.path.basename(file)
   hash = md5(file).hexdigest()
   this = file.replace(name, hash)

   print('script hash [%s]' % hash)

   if os.path.exists(this):
      age = time.time() - os.path.getmtime(this)
      if age > 7200:
         os.remove(this)

      exit()

   open(this, 'w').close()

   files = glob.glob(dir + "/mp4/*.mp4")
   files.sort(key=os.path.getmtime)

   for mp4 in files:
      m3u8 = mp4.replace('.mp4', '.m3u8')

      if not os.path.exists(m3u8):
         generatehls(mp4)

      if os.path.exists(m3u8):
         generatejpg(mp4)

   os.remove(this)

main()
