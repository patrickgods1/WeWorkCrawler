from scrapy.spiders import SitemapSpider
from WeWork.items import WeWorkItem
from scrapy import Request
from scrapy.loader import ItemLoader
import json
import logging


class scrapeWeWork(SitemapSpider):
    name = "scrapeWeWork"
    allowed_domains = ['wework.com', 'api.wework.cn', 'api.wework.hk']
    sitemap_urls = ['https://www.wework.com/sitemap.xml']
    sitemap_rules = [('/buildings/', 'parse')]


    def __init__(self):
        SitemapSpider.__init__(self)
        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.DEBUG)

        logFormatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

        # file handler
        fileHandler = logging.FileHandler("Output.log")
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

        # console handler
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)


    def parse(self, response):
        # Determine region and parse accordingly
        if 'wework.cn' in response.request.url:
            yield from self.parseCN(response, 'cn')
        elif 'wework.hk' in response.request.url:
            yield from self.parseCN(response, 'hk')
        else:
            yield from self.parseOther(response)


    def parseOther(self, response):
        # Parse response and grab needed information
        script = response.xpath("//script[contains(., 'streetAddress')]/text()").extract_first()
        jsonResponse = json.loads(script)
        jsonResponse = jsonResponse['@graph'][2]
        buildingItemLoader = ItemLoader(item=WeWorkItem(), response=response)
        name = str(jsonResponse['name'])
        # brand = str(jsonResponse['brand'])
        addressJSON = jsonResponse['address']
        streetAddress = str(addressJSON['streetAddress'])
        country = str(addressJSON['addressCountry'])
        locality  = str(addressJSON['addressLocality'])
        postalCode  = str(addressJSON['postalCode'])
        telephone = str(jsonResponse['telephone'])
        geoJSON = jsonResponse['geo']
        latitude  = str(geoJSON['latitude'])
        longitude  = str(geoJSON['longitude'])
        amenitiesJSON = jsonResponse['hasOfferCatalog']["itemListElement"]
        amenitiesList = set()
        for item in amenitiesJSON:
            amenityName = '•  ' + str(item['itemOffered']['name'])
            amenitiesList.add(amenityName)
        amenities = "\n".join(sorted(amenitiesList))
        rating = response.css('p.ray-text.rating__container-header > span::text').extract_first()
        reviewCount = response.css('a.rating__link--header > u::text').extract_first()
        if rating:
            reviewCount = reviewCount.split(' ')[0]
        else:
            rating = 'No ratings'
            reviewCount = 'No reviews'
        
        transportationList = set()
        for li in response.css('li.transportation'):
            transportType = li.css('img::attr(alt)').extract_first().replace(' icon', '').capitalize()
            if transportType:
                description = li.css('div.transportation-description::text').extract_first()
                transportationList.add(f'•  {transportType} - {description}')
        if transportationList:
            transportation = "\n".join(sorted(transportationList))
        else:
            transportation = ''

        URL = response.request.url
        buildingItemLoader.add_value('Name', name)
        # buildingItemLoader.add_value('Brand', brand)
        buildingItemLoader.add_value('Address', streetAddress)
        buildingItemLoader.add_value('Country', country)
        buildingItemLoader.add_value('Locality', locality)
        buildingItemLoader.add_value('postalCode', postalCode)
        buildingItemLoader.add_value('Telephone', telephone)
        buildingItemLoader.add_value('Latitude', latitude)
        buildingItemLoader.add_value('Longitude', longitude)
        buildingItemLoader.add_value('Amenities', str(amenities))
        buildingItemLoader.add_value('Rating', str(rating))
        buildingItemLoader.add_value('Reviews', str(reviewCount))
        buildingItemLoader.add_value('Transit', str(transportation))
        buildingItemLoader.add_value('URL', URL)
        yield buildingItemLoader.load_item()


    def parseCN(self, response, region):
        # If CN webpage, construct the api URL and yield the request
        script = response.xpath("//script[contains(., 'streetAddress')]/text()").extract_first()
        buildingSlug = response.request.url.split('/')[-1].split('?')[0]
        apiURL = f'https://api.wework.{region}/api/v2/buildings/{buildingSlug}'
        header = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        #     'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'DNT': 1,
            'Host': 'api.wework.cn',
            'locale': 'en_US',
            'Origin': 'https://www.wework.cn',
        #     'Pragma': 'no-cache',
            'Referer': 'https://www.wework.cn/',
        #     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        #     'sec-ch-ua-mobile': '?1',
        #     'Sec-Fetch-Dest': 'empty',
        #     'Sec-Fetch-Mode': 'cors',
        #     'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
            }
        yield Request(apiURL, headers=header, callback=self.parseAPI)


    def parseAPI(self, response):
        # Parse the json response from the API call. Grab needed information.
        jsonResponse = json.loads(response.body)
        jsonResponse = jsonResponse['data']
        buildingItemLoader = ItemLoader(item=WeWorkItem(), response=response)
        name = str(jsonResponse['name'])
        # brand = str(jsonResponse['brand'])
        address = str(jsonResponse['address'])
        if 'hk' in response.request.url:
            country = 'HK'
            URL = f"https://wework.hk/locations/{response.request.url.split('/')[-1]}?lang=en-us"
        elif 'cn' in response.request.url:
            country = 'CN'
            URL = f"https://www.wework.cn/building/{response.request.url.split('/')[-1]}?lang=en-us"
        else:
            country = ''
        locality  = str(jsonResponse['cityName'])
        if 'postalCode' in jsonResponse:
            postalCode  = str(jsonResponse['postalCode'])
        else:
            postalCode = ''
        # telephone = str(jsonResponse['telephone'])
        telephone = ''
        latitude  = str(jsonResponse['latitude'])
        longitude  = str(jsonResponse['longitude'])
        amenitiesList = set()
        for item in jsonResponse['amenities']:
            #• ‣
            amenityName = '•  ' + str(item['name'])
            amenitiesList.add(amenityName)
        amenities = "\n".join(sorted(amenitiesList))
        # rating = response.css('p.ray-text.rating__container-header > span::text').extract_first()
        # reviewCount = response.css('a.rating__link--header > u::text').extract_first()
        # if rating:
        #     reviewCount = reviewCount.split(' ')[0]
        # else:
        rating = 'No ratings'
        reviewCount = 'No reviews'

        transportationList = set()
        for item in jsonResponse['transportations']:
            #• ‣
            transportationName = f"•  {item['type'].capitalize()} - {item['station']} station on {item['line']}"
            transportationList.add(transportationName)
        transportation = "\n".join(sorted(transportationList))

        # URL = response.request.url
        buildingItemLoader.add_value('Name', name)
        # buildingItemLoader.add_value('Brand', brand)
        buildingItemLoader.add_value('Address', address)
        buildingItemLoader.add_value('Country', country)
        buildingItemLoader.add_value('Locality', locality)
        buildingItemLoader.add_value('postalCode', postalCode)
        buildingItemLoader.add_value('Telephone', telephone)
        buildingItemLoader.add_value('Latitude', latitude)
        buildingItemLoader.add_value('Longitude', longitude)
        buildingItemLoader.add_value('Amenities', str(amenities))
        buildingItemLoader.add_value('Rating', str(rating))
        buildingItemLoader.add_value('Reviews', str(reviewCount))
        buildingItemLoader.add_value('Transit', str(transportation))
        buildingItemLoader.add_value('URL', URL)
        yield buildingItemLoader.load_item()