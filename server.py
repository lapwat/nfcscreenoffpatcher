import os, zipfile
import http.server as server
from datetime import datetime

from patcher import Patcher

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
  def do_GET(self):
    self.path = '/data/stats.csv'
    return server.SimpleHTTPRequestHandler.do_GET(self)

  def do_PUT(self):
    try:
      # save archive
      filename = os.path.basename(self.path)
      file_length = int(self.headers['Content-Length'])
      with open(filename, 'wb') as output_file:
          output_file.write(self.rfile.read(file_length))

      # unzip
      timestamp = int(datetime.timestamp(datetime.now()))
      extract_dir = f'data/{timestamp}'
      with zipfile.ZipFile(filename) as archive:
        archive.extractall(extract_dir)

      # disassemble
      patcher = Patcher.factory(extract_dir)
      patcher.disassemble()

      # check that apk has been successfully disassembled
      if not patcher.is_successfully_disassembled():
        # manufacturer = patcher.manufacturer.replace(' ', '')
        # model = patcher.model.replace(' ', '')
        # os.rename(extract_dir, f'data/fail-{timestamp}-{manufacturer}-{model}')
        patcher.clean()
        patcher.log_stats('fail-disassemble')
        self.send_error(500)
        return

      # patch
      patcher.patch_ScreenStateHelper()
      patcher.patch_NfcService()
      patcher.assemble()

      # write aligned apk in response
      self.send_response(200)
      with open(f'{extract_dir}/{patcher.apk_name}_align.apk', 'rb') as apk:
        self.send_header("Content-Type", 'application/vnd.android.package-archive')
        fs = os.fstat(apk.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.end_headers()
        self.wfile.write(apk.read())

      patcher.clean()
      patcher.log_stats()
    except Exception as error:
      print(timestamp, error)
      patcher.clean()
      patcher.log_stats('exception')

server.test(HandlerClass=HTTPRequestHandler)