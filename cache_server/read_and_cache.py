import requests
import json
from bs4 import BeautifulSoup

cacheNamespace = 'davivienda_cache'

manifest = {}

def parseResources(pageContents):
  soup = BeautifulSoup(pageContents, 'html.parser')
  for link in soup.find_all('link'):
    linkUrl = 'https://www.davivienda.com{}'.format(link['href'])
    try:
      lastSlug = linkUrl.split('/')[-1]

      print('Fetching', linkUrl)
      contents = requests.get(linkUrl).text

      lastSlug = linkUrl.split('/')[-1]
      cacheFilePath = './{}/{}.html'.format(cacheNamespace, lastSlug)

      print('Writing', cacheFilePath)
      with open(cacheFilePath, 'w') as cacheFile:
        cacheFile.write(contents)
        cacheFile.close()
      
      manifest[linkUrl] = cacheFilePath
    except:
      print('Error fetching', linkUrl)


  for script in soup.find_all('script'):
    if not script.has_attr('src'):
      continue
    scriptSrc = 'https://www.davivienda.com{}'.format(script['src'])
    try:
      lastSlug = scriptSrc.split('/')[-1]

      print('Fetching', scriptSrc)

      contents = requests.get(scriptSrc).text

      lastSlug = scriptSrc.split('/')[-1]
      cacheFilePath = './{}/{}.html'.format(cacheNamespace, lastSlug)

      print('Writing', cacheFilePath)
      with open(cacheFilePath, 'w') as cacheFile:
        cacheFile.write(contents)
        cacheFile.close()
      
      manifest[scriptSrc] = cacheFilePath
    except:
      print('Error fetching', scriptSrc)


def cachePage(pageUrl):
  print('Fetching', pageUrl)
  contents = requests.get(pageUrl).text

  lastSlug = pageUrl.split('/')[-1]
  cacheFilePath = './{}/{}.html'.format(cacheNamespace, lastSlug)

  print('Writing', cacheFilePath)
  with open(cacheFilePath, 'w') as cacheFile:
    cacheFile.write(contents)
    cacheFile.close()

  manifest[pageUrl] = cacheFilePath

  parseResources(contents)

  manifestFilePath = './{}/{}.json'.format(cacheNamespace, 'manifest')

  with open(manifestFilePath, 'w') as manifestFile:
    json.dump(manifest, manifestFile, indent=4)
    manifestFile.close()

loginUrl = 'https://www.davivienda.com/wps/portal/personas/nuevo'
cachePage(loginUrl)