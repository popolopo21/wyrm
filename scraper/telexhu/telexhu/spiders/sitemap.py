from scrapy.spiders import SitemapSpider

class Sitemap(SitemapSpider):
    name = "sitemap"
    allowed_domains = ["telex.hu"]
    sitemap_urls = ["https://telex.hu/sitemap/index.xml"]
    sitemap_follow = ['news']

    def parse(self, response):            
        yield {
            'Page Title': response.css('title ::Text').get(),
            'Article Title': response.xpath("//div[@class='title-section__top'])[1]").get()
    
        }