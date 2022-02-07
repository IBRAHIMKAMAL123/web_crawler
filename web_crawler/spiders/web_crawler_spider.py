import scrapy


class WebCrawlerSpider(scrapy.Spider):
    name = 'web_crawler'

    start_urls = ['https://www.bayut.com/to-rent/property/dubai/']

    def parse(self, response):
        property_links = response.xpath("//a[@aria-label='Listing link']")
        yield from response.follow_all(property_links, self.parse_property)

        # pagination_links = response.css('li.next a')
        # yield from response.follow_all(pagination_links, self.parse)

    def parse_property(self, response):
        def extract_with_xpath(query):
            return response.xpath(query +'/text()').get()
        yield {
            'property_id': extract_with_xpath('//span[@aria-label="Reference"]'),
            'purpose': extract_with_xpath('//span[@aria-label="Purpose"]'),
            'type': extract_with_xpath('//span[@aria-label="Type"]'),
            'added_on': extract_with_xpath('//span[@aria-label="Reactivated date"]'),
            'furnishing': extract_with_xpath('//span[@aria-label="Furnishing"]'),
            'price': extract_with_xpath('//span[@aria-label="Price"]'),
            'location': extract_with_xpath('//div[@aria-label="Property header"]'),
            'bed_bath_size': {
                    "bedrooms": extract_with_xpath('//span[@aria-label="Beds"]/span'), 
                    "bathrooms": extract_with_xpath('//span[@aria-label="Baths"]/span'), 
                    "size": extract_with_xpath('//span[@aria-label="Area"]/span/span')
                    },
            'permit_number': extract_with_xpath('//div[@aria-label="Agency info"]/div/div[2]/span[3]'),
            'agent_name': extract_with_xpath('//div[@aria-label="Agency info"]/div/div[3]'),
            'image_url': response.xpath('//div[@aria-label="Property image"]/div/picture/source/@srcset').extract(),
            'breadcrumbs': response.xpath('//span[@aria-label="Link name"]').extract(),
            'amenities': response.xpath('//h3["Features / Amenities"]/following-sibling::div/div/div[2]/span').extract(),

            
        }