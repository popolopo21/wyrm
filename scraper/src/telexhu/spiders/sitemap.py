import scrapy
from telexhu.items import TelexhuArticle
import json
import edgedb
from telexhu.queries.get_website_async_edgeql import get_website
from loguru import logger
import json

class TelexSitemapSpider(scrapy.Spider):
    name = 'telexsitemap'
    start_urls = ['https://telex.hu/sitemap/index.xml']

    client = edgedb.create_async_client()
    
    namespaces = {
        's': 'https://www.sitemaps.org/schemas/sitemap/0.9'
    }

    async def parse(self, response):
        # Extract <loc> tags from sitemapindex
        website = await get_website(self.client, domain='telex.hu')
        if website.sitemap is None:
            raise Exception('Could not find sitemap')
        
        sitemap = json.loads(website.sitemap)
        logger.info(sitemap)
        sitemap_urls = response.xpath('//s:sitemap/s:loc/text()', namespaces=self.namespaces).getall()
        i = 0
        for sitemap_url in sitemap_urls:
            if 'news' in sitemap_url:
                i += 1
                yield scrapy.Request(sitemap_url, callback=self.parse_sitemap, cb_kwargs = {'sitemap': sitemap})
                if i == 2:
                    break

    def parse_sitemap(self, response, sitemap):
        # Extract <loc> and <lastmod> tags from each sitemap
        urls = response.xpath('//s:url', namespaces=self.namespaces)
        for url in urls:
            loc = url.xpath('./s:loc/text()', namespaces=self.namespaces).get()
            lastmod = url.xpath('./s:lastmod/text()', namespaces=self.namespaces).get()
            
            # Check if URL is in the dictionary
            if loc not in sitemap or sitemap[loc] != lastmod:
                yield scrapy.Request(loc, callback=self.scrape_article, cb_kwargs={'lastmod': lastmod})


    def scrape_article(self, response, lastmod):
        article = {}
        article['title'] = response.xpath('//*[@id="cikk-content"]/div[1]/div[1]/h1/text()').get()
        article['url'] = response.url
        article['content_html'] = response.xpath('//*[@id="cikk-content"]/div[2]/div[1]/div[5]').get()
        article['content_text'] = None
        article['content_text_embedding'] = [i for i in range(1536)]
        article['tags'] = response.xpath('//*[@id="cikk-content"]/div[1]/div[2]/div[@class="title-section__tags content-wrapper__child"]/a/text()').getall()
        article['author'] = response.xpath('//*[@id="cikk-content"]/div[2]/div[1]/div[2]/div[1]/div/div[2]/a/text()').get()
        article['sitemap_date'] = lastmod
        article['a_published_at'] = response.xpath('//*[@id="cikk-content"]/div[1]/div[2]/div[2]/p/span/text()').get()
        if article['a_published_at'] is None:
            article['a_published_at'] = response.xpath('//*[@id="cikk-content"]/div[1]/div[2]/div[3]/p/span/text()').get()
        article['a_modified_at'] = lastmod
        
        article = TelexhuArticle(**article)
        
        yield article