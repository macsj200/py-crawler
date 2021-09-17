from http.server import HTTPServer, BaseHTTPRequestHandler
import json

cacheNamespace = 'davivienda_cache'

manifestFilePath = './{}/{}.json'.format(cacheNamespace, 'manifest')

with open(manifestFilePath) as manifestFile:
  manifest = json.load(manifestFile)

class CacheHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    prefixWithPath = 'https://www.davivienda.com{}'.format(self.path)
    contents = ''
    with open(manifest[prefixWithPath]) as cacheFile:
      contents = cacheFile.read()
    self.send_response(200)
    self.end_headers()
    self.wfile.write(contents.encode("utf-8"))

httpd = HTTPServer(('localhost', 6969), CacheHTTPRequestHandler)
httpd.serve_forever()