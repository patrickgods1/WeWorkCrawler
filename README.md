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

## WeWork Locations Map
The location and amenities inforation is mapped and visualized on Google Maps:
![WeWorkNA](https://user-images.githubusercontent.com/60832092/144689076-b19c0a0c-1da0-42df-a026-817688e9c66b.PNG)

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