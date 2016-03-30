from scrapy.spider import BaseSpider
from bs4 import BeautifulSoup
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from datetime import datetime
from scrapy.selector import Selector
from nysocial.items import NysocialItem


class DmozSpider(CrawlSpider):
    name = "nysocial"
    allowed_domains = ["newyorksocialdiary.com"]
    start_urls = [
        "http://www.newyorksocialdiary.com",
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow=('/party-pictures',)),callback='parse_items',follow=True),
    )

    def parse_items(self, response):
        soup = BeautifulSoup(response.body_as_unicode())
        items = []
        datestr = soup.select('.pane-node-created')
        if datestr:
            datestr = datestr[0].text.strip().replace("\n","")
            if datetime.strptime(datestr, "%A, %B %d, %Y") < datetime(2014,12,1,0,0):
                caption1 = soup.select('.photocaption')
                caption2 = soup.select('td div font')
                caption = caption1 + caption2
                for cap in caption:
                    if cap.text.strip() != "\n" and cap.text.strip() != "":
                        item = NysocialItem()
                        item['caption'] = cap.text
                        item['date'] = datestr
                        items.append(item)
        return items