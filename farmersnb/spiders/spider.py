import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import FarmersnbItem
from itemloaders.processors import TakeFirst


class FarmersnbSpider(scrapy.Spider):
	name = 'farmersnb'
	start_urls = ['http://banking.farmersnb.com/news/all']

	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2/a/span/text()').get()
		description = response.xpath('//div[@class="section post-body"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@id="hubspot-author_data"]/text()[normalize-space()]').get()
		date = re.findall(r'[A-Za-z]+,\s\d{2},\s\d{2}', date) or ['']

		item = ItemLoader(item=FarmersnbItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date[0])

		return item.load_item()
