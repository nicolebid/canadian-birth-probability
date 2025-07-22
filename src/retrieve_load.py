import sqlite3
import pandas as pd
import requests
import json
import pycountry
import os 
from .config import DATA_DB, DATA_CSV

# This script defines the functions used to retrieve the required data.  
# See the 'main()' function (at the end of the script) for execution flow. 

def fetch_all_data(indicator_id, start_year=2010, end_year=2023, per_page=1000):
    """
    Retrieves all data related to the given indicator from the World Bank dataset.

    Parameters
    ----------
    indicator_id : str
        The indicator ID to fetch data for.
    start_year : int, optional
        The start year for data retrieval (default is 2010).
    end_year : int, optional
        The end year for data retrieval (default is 2023).
    per_page : int, optional
        Number of results per page (default is 1000).

    Returns
    -------
    list of dict
        A list containing data entries as dictionaries retrieved from the API.
    """
    data_all = []
    page = 1
    total_pages = None

    # Retireve and parse data 
    while total_pages is None or page <= total_pages:
        url = f"https://api.worldbank.org/v2/country/all/indicator/{indicator_id}?format=json&date={start_year}:{end_year}&per_page={per_page}&page={page}"
        response = requests.get(url)
        data = response.json()

        if not data or len(data) <2: 
            break

        if total_pages is None:
            total_pages = data[0]["pages"]
        
        data_all.extend(data[1])
        page += 1

    return data_all 

def insert_data(cursor, data):
        """
        Load JSON data entries into the birthrate_population_data SQL table.

        Parameters
        ----------
        cursor : sqlite3.Cursor
            The  cursor object used to execute SQL commands.
        data : list of dict
            List of data entries tetrieved from the API to be inserted into the database. 

        Returns
        -------
        None
        """

        for item in data:
            cursor.execute(""" 
                INSERT INTO birthrate_population_data (
                    indicator_id, 
                    indicator_name, 
                    country_id, 
                    country_name, 
                    country_iso3, 
                    year, 
                    value, 
                    unit, 
                    obs_status, 
                    decimal
                ) VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (
                item["indicator"]["id"],
                item["indicator"]["value"],
                item["country"]["id"],
                item["country"]["value"],
                item["countryiso3code"],
                int(item["date"]),
                item["value"],
                item["unit"],
                item["obs_status"],
                item["decimal"]
            ))

def main():
    """The main function to run script for retrieving and loading data."""

    ## 1. RETRIEVE DATA 
    # Fetch birth rate and population data using API
    data_br = fetch_all_data("SP.DYN.CBRT.IN")
    data_pop = fetch_all_data("SP.POP.TOTL")

    # Create table to load data into local SQL database 
    conn = sqlite3.connect(DATA_DB)
    cursor = conn.cursor()

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS birthrate_population_data (
        indicator_id TEXT,
        indicator_name TEXT, 
        country_id TEXT, 
        country_name TEXT,
        country_iso3 TEXT,
        year INTEGER, 
        value REAL,
        unit TEXT, 
        obs_status TEXT, 
        decimal INTEGER
        )
    """)

    ## 2. LOAD DATA
    # Load data to the database 
    insert_data(cursor=cursor, data=data_br)
    insert_data(cursor=cursor, data=data_pop)

    conn.commit()
    conn.close()

    conn = sqlite3.connect(DATA_DB)
    cursor = conn.cursor()

    # Obtain valid countries only (ie. No regions)
    valid_iso3 = {country.alpha_3 for country in pycountry.countries}
    valid_iso3_str = ",".join(f"'{code}'" for code in valid_iso3)

    # Birth rate data
    query_br = f""" 
    SELECT country_iso3, country_id, country_name, year, value AS birth_rate
    FROM birthrate_population_data
    WHERE 
        indicator_name = 'Birth rate, crude (per 1,000 people)'	
        AND country_iso3 IN ({valid_iso3_str})
    """
    # Population data 
    query_pop = f""" 
    SELECT country_iso3, country_id, country_name, year, value AS population
    FROM birthrate_population_data
    WHERE 
        indicator_name = 'Population, total'
        AND country_iso3 IN ({valid_iso3_str})	
    """
    
    # create pandas dataframes using queries 
    df_br = pd.read_sql_query(query_br, conn)
    df_pop = pd.read_sql_query(query_pop, conn)
    df_merged = pd.merge(df_br, df_pop, how='outer', on=['year', 'country_iso3', 'country_name', 'country_id'])
    
    # save for later processing 
    df_merged.to_csv(DATA_CSV, index=False) 
  
if __name__ == "__main__":
    main() 