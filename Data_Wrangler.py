import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
def extract(url):
    # URL of the website to scrape
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
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
    data=pd.DataFrame(columns=df_columns) #Declaring the dataframe
    
    # Extracting the data rows from xml
    rows = soup.find_all("Row")
    for row in rows:
        country = row.find("RowLabels").find("RowLabel").get_text()
        
        cells = row.find("Cells").find_all("C")
        row_list =[]
        row_list.append(country)
        for cell in cells:               # looping on all times for the country
            row_list.append(cell["v"])   #appending the time data to the list
        
        data.loc[len(data)] = row_list #assign the list of country to the dataframe
    return data

def transform(data):
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

    url = "http://www.jodidb.org/TableViewer/getData.aspx?row=1&col=1&rowCount=100&colCount=100&ReportId=93906"
    df=extract(url)
    df_t=transform(df)
    load(df_t)

