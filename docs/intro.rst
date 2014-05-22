Introduction to okscraper
=========================

Writing scrapers
----------------

The main object in okscraper is the scraper object which should be based on the BaseScraper abstract class.

The BaseScraper class defines a basic interface which consists of:

* scrape method - The main entry point into the scraper. When this method is called the scraping process starts. It can optionally accept parameters relating to the scrape job.

* source object - This is an object based on BaseSource. It defines the input of the scraper. For example, a UrlSource allows to get input from a URL.

* storage object - This is an object based on BaseStorage. It defines the output of the scraper - where and how to store it.

It's a fairly simple interface but it provide standarization and interoperability of scrapers.

A best practice for writing scrapers is to write many small scrapers, each one doing a specific part of the scraping process and then incorporating them into a main scraper. You can use the ScraperSource object to use the output of a scraper as the input of another scraper.

Running scrapers and logging errors
-----------------------------------

Another important part of the okscraper framework is to provide facilities for running and logging scraper errors and meta-data.

The basic class for running scrapers is the Runner class. It can be used to run scrapers from the command line. It accepts a parameter of module name where the scrapers exist and a class name of the scraper to run. It then loads the relevant module and runs the scraper. It can optionally pass parameters from the command line into the scraper.

We also provide a LogRunner runner which provides facilities for logging the output of the runner, output differnet log levels according to required verbosity.

If you are using django you should check out okscraper-django which provides a django management command to run scrapers, log the output to django models and viewing the logs through the django admin interface.