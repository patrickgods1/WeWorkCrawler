# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WeWorkItem(scrapy.Item):
    # define the fields for your item here like:
    Name = scrapy.Field()
    Brand = scrapy.Field()
    Address = scrapy.Field()
    Country = scrapy.Field()
    Locality = scrapy.Field()
    postalCode = scrapy.Field()
    Telephone = scrapy.Field()
    Latitude = scrapy.Field()
    Longitude = scrapy.Field()
    Amenities = scrapy.Field()
    Rating = scrapy.Field()
    Reviews = scrapy.Field()
    # Monthly_Subscription = scrapy.Field()
    # Pay_As_You_Go = scrapy.Field()
    Transit = scrapy.Field()
    URL = scrapy.Field()
