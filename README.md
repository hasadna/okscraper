okscraper
=========

A python module for scraping websites and documents

The module is primarily meant to organize and standardize Open-Knesset scraping needs but is developed as a separate module which might be useful for other similar projects.

Project Goals
=============

* Provide a standard interface for scraping needs
 * There is a lot of code duplication in the scraping processes
 * Some modules do similar scraping tasks but in very different ways
* Monitor the scraping processes
 * Today there is limited to no monitoring of the scraping processes - a scraping process might fail and no one knows about until someone complains
* Allow to do unit testing for the scraping processes
* Make it easier for developers to modify and add scraping processes
