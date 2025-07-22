import pandas as pd
import requests
import kaleido
import os 
import plotly.graph_objs as go 
import plotly.express as px
from .config import *
from .calculate_probabilities import calc_probability_country

# This script defines the functions used to create graphs to present the results. 
# See the 'main()' function (at the end of the script) for execution flow. 

def canada_bar_chart(data, yr=2010): 
    """
    Creates a bar chart comparing the probability of being born in Canada vs. the rest of the world for a given year.

    Parameters
    ----------
    yr : int, optional
        The year to calculate and display the birth probability (default is 2010).
    data : pandas.DataFrame
        The main dataframe obtained from data/country_br_pop_births.csv

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A Plotly bar chart object showing the probability distribution.
    """
    cat = ['Rest of the World', 'Canada']
    can_prob = calc_probability_country(data=data, yr=yr, country="Canada")
    values = [1-(can_prob/100), can_prob/100]

    fig = go.Figure(go.Bar(
        x=values, 
        y=cat, 
        orientation='h', 
        hovertemplate='%{x:.2%}<extra></extra>'
    ))
    fig.update_layout(
        title=f'Probability of Being Born in Canada vs Rest of the World ({yr})', 
        xaxis_title='Percentage',
        xaxis=dict(
            title='Percentage',
            tickformat='.0%',
        ),
        yaxis_title='Countries',
        template='plotly_white'
    )
    return fig 

def canada_timeline(data):
    """
    Creates a timeline comparing the probability of being born in Canada over the time period in the given data. 

    Parameters
    ----------
    data : pandas.DataFrame
        The main dataframe obtained from data/country_br_pop_births.csv

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A Plotly timeline object showing the probability distribution.
    """
    fig = px.line(
        data, 
        x='Year', 
        y='Probability', 
        title='Probability of Being Born in Canada Over Time', 
        markers=True
    ) 
    fig.update_layout(
        xaxis_title='Year',
        yaxis=dict(
            title='Probability',
            tickformat='.3%',
        ),
        yaxis_title='Probability',
        template='plotly_white'
    )
    return fig 

def country_timeline(data, order):
    """
    Creates a timeline of the probabilities for the countries in the given data. 

    Parameters
    ----------
    data : pandas.DataFrame
        The main dataframe transfromed from data/country_prob.csv

    order : list
        The list of countries ordered by average probability for legend. 

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A Plotly timeline object showing counrty timelines. 
    """
    fig = px.line(data,
    x='Year',
    y='Probability',
    color='Country',
    markers=True,
    category_orders={'Country': order},  
    title='Birth Probability Trends Over Time: Comparing Top 5, Bottom 5, and Canada', 
    height=500
    )

    fig.update_layout(
            yaxis=dict( 
                ticksuffix='%'       
        ),
        xaxis_title='Year',
        yaxis_title='Probability',
        template='plotly_white'
    )
    return fig 

def main():
    """The main function to run script for creating the graphs."""

    # load the data
    df = pd.read_csv(DATA_BIRTHS_CSV)

    # 1. Bar chart for probability of being born in Canada
    can_barchart = canada_bar_chart(yr=2012, data=df)
    can_barchart.write_image(CANADA_BARCHART)
    can_barchart.write_html(CAN_BAR_HTML)

    # 2. Timeline of the change in probability for Canada overtime
    # transform data to include probabilites for all years
    year = []
    prob = []

    for i in df['year'].unique():

        can_prob = calc_probability_country(data=df, yr=i, country="Canada")/100
        year.append(int(i))
        prob.append(float(can_prob))

    data = {'Year': year,'Probability': prob}
    df_can_probs = pd.DataFrame(data)
    
    can_timeline = canada_timeline(data=df_can_probs)
    can_timeline.write_image(CANADA_TIMELINE)
    can_timeline.write_html(CANADA_TIME_HTML)


    # 3. Timeline for top 5, bottom 5, and Canada.
    # load data
    df_countries_prob = pd.read_csv(DATA_ALL_PROB_CSV)

    # Determine 5 highest and 5 lowest average probabilities off all countries
    # Calculate averages
    avg_probs = df_countries_prob.groupby('Country')['Probability'].mean().reset_index()
    avg_probs = avg_probs.rename(columns={'Probability': 'average_prob'})
    avg_probs.sort_values(by='average_prob', ascending=False, inplace=True)
    
    # select top 5, bottom 5, and canada
    top_5 = avg_probs.head(5)
    bottom_5 = avg_probs.tail(5)
    can = avg_probs[avg_probs['Country'] == 'Canada']

    selected_avgs = pd.concat([top_5, can, bottom_5], ignore_index=True)
    selected_countries = selected_avgs['Country'].to_list()

    # Filter for selected countries
    df_selected = df_countries_prob[df_countries_prob['Country'].isin(selected_countries)]
   
    # Set ordering for timeline
    df_selected.loc[:, 'Country'] = pd.Categorical(df_selected['Country'], categories=selected_countries, ordered=True)

    # adjust to percentage probabilities
    df_selected.loc[:, 'Probability'] = df_selected['Probability']*100
  
    # Generate plot
    country_timelines = country_timeline(df_selected, selected_countries)
    country_timelines.write_image(COUNTRY_TIMELINE)
    country_timelines.write_html(COUNTRY_TIME_HTML)
    
if __name__ == "__main__":
    main() 