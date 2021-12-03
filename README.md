# WeWorkCrawler
WeWorkCrawler is an application designed to scrape all WeWork locations for the followng information:

* Name
* Address
* Country
* Locality
* Postal Code
* Telephone
* Latitude
* Longitude
* Amenities
* Rating
* Reviews
* Transit
* URL

## Development
These instructions will get you a copy of the project up and running on your local machine for development.

### Built With
* [Python 3.6](https://docs.python.org/3/) - The scripting language used.
* [Scrapy](https://scrapy.org/) - Framework for crawling and extracting the data from webpages.

### Running the Script
Run the following command to installer all the required Python modules:
```
pip install -r requirements.txt
```

To run the application, call the following in the root directory of the project:
```
scrapy crawl scrapeWeWork
```

## Authors
* **Patrick Yu** - *Initial work* - [patrickgods1](https://github.com/patrickgods1)