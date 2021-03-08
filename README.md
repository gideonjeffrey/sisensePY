# sisensePY
A Python library for retrieving, combining, and formatting/outputting various kinds of data via the Sisense REST API.

## Status of project:
Under construction!

## About

[Sisense](https://www.sisense.com/ "Title") is a powerful analytics platform and competitor of tools like Tableau and PowerBI. One of the many features is offers is a REST API that allows you to see user information, retrieve and manipulate dashbaords and datamodels, query datamodels directly, and many other things - it is extremely powerful.  For documentation of the Sisense REST API, go [here](https://sisense.dev/guides/rest/ "Title").

This project is not exhaustive - you can't use the code here to do *everything* the Sisense REST API can do. Apart from the POST request for authentication, everything used is a GET request. But it does let you do many things I've found useful in my role as a Sisense administrator. 

### Sisense Version Information
These scripts were tested on the Windows implementation of Sisense, version 8.2.5.10151.

### Language
Python 3

### Dependencies:
This project uses the following Python modules that aren't included in standard Python release. If you don't already have them installed, please view the documentation for how to do so by clicking on the link.

* [requests](https://requests.readthedocs.io/en/master/ "Title")
