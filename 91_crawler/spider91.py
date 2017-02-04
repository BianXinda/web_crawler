from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import sys
from db91 import Db91

def soup_video_page(tag):
  return not tag.has_attr('title') and tag.has_attr('href') and bool(re.search('viewkey', tag['href']))

class Spider91:
  def __init__(self, url, count):
    self.db = Db91()
    self.entry_url = url
    self.page_count = count

  def query_mp4_file(self, mp4_url):
    result = re.search(r'/([1-9]*\.mp4)', mp4_url)
    if result:
      keyid = result.group(1)
    else:
      print 'Cannot get keyid, quit. ', mp4_url
      return
    if self.db.select_db(keyid):
      return
    mp4_url = mp4_url + '&start=0&id=91&client=FLASH%20MAC%2024,0,0,194&version=4.1.60'
    print mp4_url
    urllib.urlretrieve(mp4_url, keyid)
    self.db.insert_db(keyid)
    print keyid, ' downloaded!'

  def query_mp4_url(self, mp4_link_url):
    res = urllib2.urlopen(mp4_link_url)
    file_url = re.search(r'file=(.*)$', res.read())
    if file_url:
      mp4_url = file_url.group(1)
      print 'file url:', mp4_url
      self.query_mp4_file(mp4_url)

  def query_link_url(self, link_url):
    res = urllib2.urlopen(link_url)
    soup = BeautifulSoup(res.read().decode('utf-8'), 'html.parser')
    links = soup.find_all('textarea')
    link = links[1].contents
    print 'link:', link
    self.query_mp4_url(link)

  def query_page_url(self, page_url):
    res = urllib2.urlopen(page_url)
    data = res.read().decode('utf-8')
    soup = BeautifulSoup(data, 'html.parser')
    links = soup.find_all(soup_video_page)
    for link in links:
      self.query_link_url(link['href'])

  def query_entry_url(self):
    for i in range(1, self.page_count+1):
      page_url = self.entry_url + "%s" % i
      print 'page%s:' % i, page_url
      self.query_page_url(page_url)


if __name__ == "__main__":
  if len(sys.argv) > 2:
    print './spider91.py \t\t# default 20 pages \n./spider91.py 100 \t# download 100 pages'
  if len(sys.argv) == 1:
    page_count = 20
  else:
    page_count = int(sys.argv[1])
    print '91spider will download videos from page 1 to page ', page_count
  entry_url = 'http://www.91porn.com/v.php?next=watch&page='
  spider = Spider91(entry_url, page_count)
  spider.query_entry_url()
