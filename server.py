#!/usr/bin/env python3
 
"""Simple HTTP Server With Upload.

This module builds on http.server by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

see: https://gist.github.com/UniIsland/3346170
"""
 
 
__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "bones7456"
__home_page__ = "https://gist.github.com/UniIsland/3346170"
 
import os
import posixpath
import http.server
import socketserver
import urllib.request, urllib.parse, urllib.error
import html
import shutil
import mimetypes
import re
import argparse
import base64
import random

from io import BytesIO

from pathlib import Path
from subprocess import check_output

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
r = random.SystemRandom()

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    server_version = "SimpleHTTPWithUpload/" + __version__
    #tmp_dir = ''.join([r.choice(alphabet) for _ in range(24)])

    def do_POST(self):
        r, info = self.deal_post_data()
        print((r, info, "by: ", self.client_address))

        # moding in tmp directory
        tmp_dir = check_output(['mktemp', '-d', '-t', 'nso-XXXXXXXX']).decode().strip()
        check_output(['./mod.sh', tmp_dir])

        # checking that apk has been successfully disassembled
        if not os.path.exists(f'{tmp_dir}/NfcNci/smali') and not os.path.exists(f'{tmp_dir}/NQNfcNci/smali') and not os.path.exists(f'{tmp_dir}/NxpNfcNci/smali'):
            self.send_error(500)
            f.close()
            return	

        # write aligned apk in response
        f = self.send_head()
        shutil.copyfileobj(f, self.wfile)
        f.close()
        
    def deal_post_data(self):
        uploaded_files = []
        content_type = self.headers['content-type']
        if not content_type:
            return (False, "Content-Type header doesn't contain boundary")
        boundary = content_type.split("=")[1].encode()
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            fn = f'apks.zip'
            # Path(self.tmp_dir).mkdir(parents=True, exist_ok=True)
            line = self.rfile.readline()
            remainbytes -= len(line)
            line = self.rfile.readline()
            remainbytes -= len(line)
            try:
                out = open(fn, 'wb')
            except IOError:
                return (False, "Can't create file to write, do you have permission to write?")
            else:
                with out:                    
                    preline = self.rfile.readline()
                    remainbytes -= len(preline)
                    while remainbytes > 0:
                        line = self.rfile.readline()
                        remainbytes -= len(line)
                        if boundary in line:
                            preline = preline[0:-1]
                            if preline.endswith(b'\r'):
                                preline = preline[0:-1]
                            out.write(preline)
                            uploaded_files.append(fn)
                            break
                        else:
                            out.write(preline)
                            preline = line
        return (True, "File '%s' upload success!" % ",".join(uploaded_files))
 
    def send_head(self):
        f = open(f'out.apk', 'rb')
        self.send_response(200)
        self.send_header("Content-type", 'application/zip')
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.end_headers()
        return f
 
parser = argparse.ArgumentParser()
parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
args = parser.parse_args()

PORT = args.port
BIND = args.bind
HOST = BIND

if HOST == '':
	HOST = 'localhost'

Handler = SimpleHTTPRequestHandler

with socketserver.TCPServer((BIND, PORT), Handler) as httpd:
	serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
	print(serve_message.format(host=HOST, port=PORT))
	httpd.serve_forever()
