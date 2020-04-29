import os, subprocess, zipfile
import http.server as server
from datetime import datetime

from dotenv import dotenv_values

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
    extract_dir = f'/data/{timestamp}'
    with zipfile.ZipFile(filename) as archive:
      archive.extractall(extract_dir)
    rom = dotenv_values(f'{extract_dir}/.env').get('ROM')
    os.rename(extract_dir, f'/data/{rom}{timestamp}')
    
    # mod
    subprocess.run(['./mod.sh', extract_dir, apk_name])

    # check that apk has been successfully disassembled
    if not os.path.exists(f'{extract_dir}/{apk_name}/smali'):
      self.send_error(500)
      return

    # write aligned apk in response
    self.send_response(200)
    with open(f'{extract_dir}/{apk_name}_align.apk', 'rb') as apk:
      self.send_header("Content-Type", 'application/vnd.android.package-archive')
      fs = os.fstat(apk.fileno())
      self.send_header("Content-Length", str(fs[6]))
      self.end_headers()
      self.wfile.write(apk.read())

server.test(HandlerClass=HTTPRequestHandler)
