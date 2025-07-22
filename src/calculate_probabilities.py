import pandas as pd
import numpy as np 
import os 
from .config import *

# This script defines the functions used to calculate the probabilities for a 
# the specified country and year. 
# See the 'main()' function (at the end of the script) for execution flow. 

def calc_probability_country(data, yr=2010, country="Canada"):
    """
    Calculates the percentage probability of being born in a given country for the given year.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame (created from data/country_br_pop.csv)
    yr : int, optional
        The year to calculate the probability for, must be between 2010 and 2023, inclusive (default is 2010).
    country: string
        The country to calculate the probability for (default is Canada). 

    Returns
    -------
    percent_prob: float
        The percentage of births in the given country relative to total births in the given year.
    """
    
    # total births
    df_year = data[data['year'] == yr]
    total = df_year['births'].sum()

    # obtain total given country births for a given year
    country_total = df_year[df_year['country_name'] == country]['births'].values[0]
    
    percent_prob = country_total/total*100
    return percent_prob

def main():
    """The main function to execute processing the data and calculating required probabilities."""
    # load data 
    df = pd.read_csv(DATA_CSV)

    # Determine number of births by country in the dataframe 
    df['births'] = df['birth_rate']*df['population']/1000
    df.to_csv(DATA_BIRTHS_CSV, index=False) # save for later usage

    # Example calculation for Canada for a given year
    yr_2012 = calc_probability_country(data=df, yr=2012, country='Canada')
    yr_2012_ratio = round(1 / yr_2012*100)

    np.save(YR_2012_EX, yr_2012)
    np.save(YR_2012_RATIO, yr_2012_ratio)

    #Calculate additional probabilites for each country (optional task)
    country_dict = {} # to store values 

    # Obtain probability of being born in each country for each year
    for c in df['country_name'].unique():
        year = []
        prob = []
        
        for yr in df['year'].unique():
            country_prob = calc_probability_country(data=df, yr=yr, country=c)/100 
            prob.append(float(country_prob))
            year.append(int(yr))
        
        country_dict[c] = {'Year': year, 'Probability':prob} # Store values 

    # covert to a dataframe
    records = []

    for country, data in country_dict.items():
        years = data['Year']
        probs = data['Probability']
        
        for year, prob in zip(years, probs):
            records.append({
                'Country': country,
                'Year': year,
                'Probability': prob
            })

    df_probs = pd.DataFrame(records)
    df_probs.to_csv(DATA_ALL_PROB_CSV, index=False) # save for later usage

    # Calculate the Global Average of Births per year
    df = pd.read_csv(DATA_BIRTHS_CSV)
    total_births_per_yr = df.groupby('year')['births'].sum()
    global_avg_births = total_births_per_yr.mean()
    np.save(GLOBAL_AVG_BIRTHS, global_avg_births) 

if __name__ == "__main__":
    main() 