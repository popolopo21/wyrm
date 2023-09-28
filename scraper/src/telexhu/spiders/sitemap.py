import scrapy
from telexhu.items import TelexhuArticle
import json
class SitemapSpider(scrapy.Spider):
    name = 'telexsitemap'
    start_urls = ['https://telex.hu/sitemap/index.xml']

    # Load previously scraped sites
    with open('./telexmap.json', 'r') as file:
        sitemap = json.load(file)

    namespaces = {
        's': 'https://www.sitemaps.org/schemas/sitemap/0.9'
    }

    def parse(self, response):
        # Extract <loc> tags from sitemapindex
        sitemap_urls = response.xpath('//s:sitemap/s:loc/text()', namespaces=self.namespaces).getall()
        i = 0
        for sitemap_url in sitemap_urls:
            if 'news' in sitemap_url:
                i += 1
                yield scrapy.Request(sitemap_url, callback=self.parse_sitemap)
                if i == 2:
                    break

    def parse_sitemap(self, response):
        # Extract <loc> and <lastmod> tags from each sitemap
        urls = response.xpath('//s:url', namespaces=self.namespaces)
        for url in urls:
            loc = url.xpath('./s:loc/text()', namespaces=self.namespaces).get()
            lastmod = url.xpath('./s:lastmod/text()', namespaces=self.namespaces).get()
            
            # Check if URL is in the dictionary
            if loc not in self.sitemap or self.sitemap[loc] != lastmod:
                yield scrapy.Request(loc, callback=self.scrape_article, cb_kwargs={'lastmod': lastmod})

    def scrape_article(self, response, lastmod):
        article ={}
        article['title'] = response.xpath('//*[@id="cikk-content"]/div[1]/div[1]/h1/text()').get()
        article['url'] = response.url
        article['content_html'] = response.xpath('//*[@id="cikk-content"]/div[2]/div[1]/div[5]').get()
        article['content_text'] = None
        article['content_text_embedding'] = None
        article['tags'] = response.xpath('//*[@id="cikk-content"]/div[1]/div[2]/div[@class="title-section__tags content-wrapper__child"]/a/text()').getall()
        article['author'] = response.xpath('//*[@id="cikk-content"]/div[2]/div[1]/div[2]/div[1]/div/div[2]/a/text()').get()
        article['a_published_at'] = response.xpath('//*[@id="cikk-content"]/div[1]/div[2]/div[2]/p/span/text()').get()
        if article['a_published_at'] is None:
            article['a_published_at'] = response.xpath('//*[@id="cikk-content"]/div[1]/div[2]/div[3]/p/span/text()').get()
        article['a_modified_at'] = lastmod
        
        article = TelexhuArticle(**article)
        # Update the sitemap dictionary with the new lastmod
        self.sitemap[response.url] = lastmod
        
        # Save the updated sitemap to JSON
        with open('telexmap.json', 'w') as file:
            json.dump(self.sitemap, file)
        
        yield article