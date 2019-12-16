from __future__ import print_function
import glob, os.path, pickle, time
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from hashlib import md5

dir = os.path.dirname(os.path.abspath(__file__))
tok = os.path.join(dir, 'token.pickle')

def session():
   creds = None
   if os.path.exists(tok):
      with open(tok, 'rb') as token:
         creds = pickle.load(token)

   if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
         creds.refresh(Request())
      else:
         flow = InstalledAppFlow.from_client_secrets_file(os.path.join(dir, 'credentials.json'), ['https://www.googleapis.com/auth/drive'], redirect_uri='urn:ietf:wg:oauth:2.0:oob')
         creds = flow.run_console()
         with open(tok, 'wb') as token:
            pickle.dump(creds, token)

   return build('drive', 'v3', credentials=creds)

def upload(drive, file):
   print('uploading %s' % file)
   media = MediaFileUpload(file)
   result = drive.files().create(body={'name': os.path.basename(file), 'parents': ['1c8mEtLoGpksbRRGOV2NUYm4tAHf-qh5r']}, media_body=media, fields='id').execute()
   fileId = result['id']

   drive.permissions().create(body={"role":"reader", "type":"anyone"}, fileId=fileId).execute()

   playlist(file, fileId)

   os.remove(file)

def uqload(drive, file):
   print('uploading %s' % file)
   media = MediaFileUpload(file)
   result = drive.files().create(body={'name': os.path.basename(file), 'parents': ['1GzMbpMdoysmvM4PD5wGIxMhwwBVpnNKk']}, media_body=media, fields='id').execute()
   fileId = result['id']

   drive.permissions().create(body={"role":"reader", "type":"anyone"}, fileId=fileId).execute()

   print('upload complete: https://lh3.googleusercontent.com/d/%s' %fileId)

def playlist(file, id):
   fn = os.path.basename(file).replace('.png', '.ts')
   url = 'https://lh3.googleusercontent.com/d/%s' % id
   m3u8 = '%s.m3u8' % file.split('_')[0]

   with open(m3u8, 'r') as fr:
      pl = fr.read()
      pl = pl.replace(fn, url)

      print('updating playlist: %s -> %s' % (fn, url))

      with open(m3u8, 'w') as fw:
         fw.write(pl)

def start():
   file = os.path.abspath(__file__)
   name = os.path.basename(file)
   hash = md5(file).hexdigest()
   this = file.replace(name, hash)

   print('script hash [%s]' % hash)

   if os.path.exists(this):
      age = time.time() - os.path.getmtime(this)

      if age > 3600: os.remove(this)

      exit()

   with open(this, 'w') as phash:
      phash.write(file)

   files = glob.glob(os.path.join(dir, 'mp4', '*.png'))

   if files: drive = session()

   for file in files:
      if os.stat(file).st_size > 408:
         upload(drive, file)

   os.remove(this)

start()
