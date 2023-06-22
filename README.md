# KAPSARC

This repository includes the Python code that extracts data, transforms, and loads as follows:

1) Scrape the data from http://www.jodidb.org/TableViewer/tableView.aspx?ReportId=93906  

  Beyond 20/20 WDS - Table view - jodidb.org\
  Joint Organisations Data Initiative – Primary (last 15 months) Other: Unit . Thousand Barrels per day (kb/d) Product\
  www.jodidb.org\

 with The Balance set to Exports.

2) Insert the extracted data into a database preferably SQLite or any other database you choose. The data format should be as follows (with 
  country / month-year / value being columns):
    country | month-year | value\
    Algeria   Sep2019      1024\
    Algeria   Oct2019      1023
