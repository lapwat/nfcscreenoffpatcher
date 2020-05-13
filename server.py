import os, subprocess, zipfile
import http.server as server
from datetime import datetime

from dotenv import dotenv_values

from patcher import Patcher

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
  def do_PUT(self):
    # save archive
    filename = os.path.basename(self.path)
    apk_name = os.path.splitext(filename)[0]
    file_length = int(self.headers['Content-Length'])
    with open(filename, 'wb') as output_file:
        output_file.write(self.rfile.read(file_length))

    # unzip
    timestamp = int(datetime.timestamp(datetime.now()))
    tmp_dir = f'/data/{timestamp}'
    with zipfile.ZipFile(filename) as archive:
      archive.extractall(tmp_dir)
    env = dotenv_values(f'{tmp_dir}/.env')
    manufacturer = env.get('MANUFACTURER').replace(' ', '')
    model = env.get('MODEL').replace(' ', '')
    extract_dir = f'/data/{manufacturer}-{model}-{timestamp}'
    os.rename(tmp_dir, extract_dir) 
    
    # disassemble
    patcher = Patcher(extract_dir)
    subprocess.run(['./disassemble.sh', extract_dir, apk_name])

    # check that apk has been successfully disassembled
    if not patcher.is_successfully_disassembled():
      os.rename(extract_dir, f'/data/fail-{manufacturer}-{model}-{timestamp}')
      self.send_error(500)
      return

    # patch
    patcher.patch_ScreenStateHelper()
    patcher.patch_NfcService()

    # assemble
    subprocess.run(['./assemble.sh', extract_dir, apk_name])

    # write aligned apk in response
    self.send_response(200)
    with open(f'{extract_dir}/{apk_name}_align.apk', 'rb') as apk:
      self.send_header("Content-Type", 'application/vnd.android.package-archive')
      fs = os.fstat(apk.fileno())
      self.send_header("Content-Length", str(fs[6]))
      self.end_headers()
      self.wfile.write(apk.read())

    patcher.clean()

server.test(HandlerClass=HTTPRequestHandler)
