import urllib
import urllib2
import re
from db91 import Db91


class Spider91:
    def __init__(self, url, count):
        self.db = Db91()
        self.db.create_db()
        self.entry_url = url
        self.page_count = count

    def query_mp4_file(self, mp4_url):
        keyid = mp4_url[-10:]
        if self.db.select_db(keyid):
            return
        self.db.insert_db(keyid)
        urllib.urlretrieve(mp4_url, keyid)
        print keyid, ' downloaded!'

    def query_mp4_url(self, mp4_link_url):
        pattern = re.compile('http.*mp4')
        request = urllib2.Request(mp4_link_url)
        response = urllib2.urlopen(request)
        file_url = re.findall(pattern, response.read())
        if file_url:
            print 'file url:', file_url[0]
            mp4_url = file_url[0]
            self.query_mp4_file(mp4_url)

    def query_link_url(self, link_url):
        request = urllib2.Request(link_url)
        response = urllib2.urlopen(request)
        pattern = re.compile('video_id=.*\' quality')
        keywords = re.findall(pattern, response.read())
        if keywords:
            for key in keywords:
                keyid = key[9:-16]
                values = {'VID': keyid, 'v': 'NaN', 'mp4': key[-11:-9]}
                data = urllib.urlencode(values)
                mp4_link_url = 'http://91.bestchic.com/getfile_jw.php?' + data
                print 'mp4 link:', mp4_link_url
                self.query_mp4_url(mp4_link_url)

    def query_page_url(self, page_url):
        request = urllib2.Request(page_url)
        response = urllib2.urlopen(request)
        pattern = re.compile('<a href="http://www.91porn.com/view_video.php\?viewkey=.*viewtype=basic&category=rf">')
        data = response.read().decode('utf-8')
        links = re.findall(pattern, data)
        for link in links:
            link_url = link[9:-2]
            print 'link:', link_url
            self.query_link_url(link_url)

    def query_entry_url(self):
        for i in range(1, self.page_count+1):
            page_url = self.entry_url + "%s" % i
            print 'page%s:' % i, page_url
            self.query_page_url(page_url)


if __name__ == "__main__":
    entry_url = 'http://www.91porn.com/video.php?category=rf&page='
    page_count = 20
    spider = Spider91(entry_url, page_count)
    spider.query_entry_url()
