import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
def extract(url):
    # URL of the website to scrape
    response = requests.get(url)
    # Parse the XML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "xml")
    
    # Extracting the header of xml to dataframe columns
    Country=soup.find_all('DimLabel')[1].get_text()
    Time=[]
    col_labels=soup.find_all('ColLabel')
    for col_label in col_labels:
        Time.append(col_label.get_text())
    df_columns=[]
    df_columns.append(Country)
    df_columns.extend(Time) 
    #Declaring the dataframe 
    data=pd.DataFrame(columns=df_columns) 
    
    # Extracting the data rows from xml
    rows = soup.find_all("Row")
    for row in rows:
        country = row.find("RowLabels").find("RowLabel").get_text()
        
        cells = row.find("Cells").find_all("C")
        row_list =[]
        row_list.append(country)
        # looping on all times for the country
        for cell in cells:               
            row_list.append(cell["v"])   #appending the time data to the list
        #assigning the row list of each country to the dataframe
        data.loc[len(data)] = row_list 
    return data

def transform(data):
    # tranform the dataframe from country Feb2022... into country |month-year|value 
    df_transformed = data.melt(id_vars=['Country'], var_name='month_year', value_name='value')
    return df_transformed

def get_db_connection():
    # SQLite database configuration
    DATABASE = 'countries_data.db'
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def load(data):
    # Create the database file
    conn = get_db_connection()

    # Create a table named 'data'
    table_name = 'data'
    query = f'Create table if not Exists {table_name} (country text, month_year text, value real)'
    conn.execute(query)
    # Insert data into database
    data.to_sql(table_name,conn,if_exists='replace',index=False)
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    return 'data inserted successfully'

if __name__ == '__main__':
    # the url is the request the fill the targeted page, scraping the url 
    # that sent in email, always return empty data
    url = "http://www.jodidb.org/TableViewer/getData.aspx?row=1&col=1&rowCount=100&colCount=100&ReportId=93906"
    # extracting and scraping the data from URL
    df=extract(url) 
    # transforming the data to country | month-year | value
    df_t=transform(df) 
    # loading the data into SQLite 
    load(df_t)

