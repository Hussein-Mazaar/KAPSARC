# Overview

This repository includes the Python code that does the following tasks:

1) Scrape the data from http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93906  

  &nbsp;&nbsp;Beyond 20/20 WDS - Table view - jodidb.org\
  &nbsp;&nbsp;Joint Organisations Data Initiative – Primary (last 15 months) Other: Unit . Thousand Barrels per day (kb/d) Product\
  &nbsp;&nbsp;www.jodidb.org\

 &nbsp;&nbsp;with The Balance set to Exports.

 The URL is retrieving empty data and we use the request that fill the website with data
 http://www.jodidb.org/TableViewer/getData.aspx?row=1&col=1&rowCount=100&colCount=100&ReportId=93906

2) Insert the extracted data into a database preferably SQLite or any other database you choose. The data format should be as follows (with 
  country / month-year / value being columns):\
\
    country | month-year | value\
    Algeria   Sep2019      1024\
    Algeria   Oct2019      1023

## Setup
1. install Python IDE on your device
2. Also, make sure to have the following libraries installed — pandas, lxml, requests, beautifulsoup4, wheel.
