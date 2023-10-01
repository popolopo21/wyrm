import scrapy
from telexhu.items import Webpage
import json
import edgedb
from telexhu.queries.get_website_async_edgeql import get_website
from loguru import logger
import json
from urllib.parse import urlparse
from datetime import datetime


class TelexSitemapSpider(scrapy.Spider):
    name = "telexsitemap"
    start_urls = ["https://telex.hu/sitemap/index.xml"]
    domain = "https://telex.hu"
    client = edgedb.create_async_client()

    namespace = {"sm": "https://www.sitemaps.org/schemas/sitemap/0.9"}

    async def parse(self, response):
        # Extract <loc> tags from sitemapindex
        website = await get_website(self.client, domain=self.domain)
        if website is None:
            logger.error("Could not find website")
        sitemap_urls = response.xpath(
            "//sm:sitemap/sm:loc/text()", namespaces=self.namespace
        ).getall()
        i = 0
        for sitemap_url in sitemap_urls:
            if "news" in sitemap_url:
                i += 1
                yield scrapy.Request(
                    sitemap_url,
                    callback=self.parse_sitemap,
                    cb_kwargs={"website": website},
                )
                if i == 2:
                    break

    def parse_sitemap(self, response, website):
        # Extract <loc> and <lastmod> tags from each sitemap
        urls = response.xpath("//sm:url", namespaces=self.namespace)
        if website.sitemap:
            sitemap = json.loads(website.sitemap)
        # else:
        #     sitemap = {}
        for url in urls:
            loc = url.xpath("./sm:loc/text()", namespaces=self.namespace).get()
            lastmod = url.xpath("./sm:lastmod/text()", namespaces=self.namespace).get()
            lastmod = datetime.fromisoformat(lastmod)

            # Check if URL is in the dictionary
            if loc not in sitemap or datetime.fromisoformat(sitemap[loc]) != lastmod:
                yield scrapy.Request(
                    loc,
                    callback=self.scrape_article,
                    cb_kwargs={"lastmod": lastmod},
                )

    def scrape_article(self, response, lastmod):
        yield Webpage(
            path=urlparse(response.url).path,
            html=response.body,
            lastmod=lastmod,
            domain=self.domain,
        )
