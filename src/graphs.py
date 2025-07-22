import pandas as pd
import requests
import kaleido
import os 
import plotly.graph_objs as go 
import plotly.express as px
from .config import DATA_DB, DATA_CSV, DATA_ALL_PROB_CSV, CANADA_BARCHART, DATA_BIRTHS_CSV, CAN_BAR_HTML, CANADA_TIMELINE, CANADA_TIME_HTML, COUNTRY_TIME_HTML, COUNTRY_TIMELINE
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
        title='Probability of Being Born in Canada Over Years' 
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

def country_timeline(data):
    """
    Creates a timeline of the probabilities for the countries in the given data. 

    Parameters
    ----------
    data : pandas.DataFrame
        The main dataframe transfromed from data/country_prob.csv

    Returns
    -------
    plotly.graph_objs._figure.Figure
        A Plotly timeline object showing counrty timelines. 
    """

    fig = px.line(
        data,
        x='Year',
        y='Probability',
        color='Country',
        category_orders={'Country': data}, 
        title='Birth Probability: Top 5, Bottom 5 and Canada Over Time'
    )

    fig.update_layout(template='plotly_white')
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


    # 3. Timeline for top and bottom 5 countries 
    # load data
    df_countries_prob = pd.read_csv(DATA_ALL_PROB_CSV)

    # Determine 5 highest and 5 lowest average probabilities off all countries
    avg_probs = df_countries_prob.groupby('Country')['Probability'].mean().reset_index()
    avg_probs = avg_probs.rename(columns={'Probability': 'average_prob'})
    avg_probs.sort_values(by='average_prob')
    
    top_5 = avg_probs.nlargest(5, 'average_prob')['Country'].tolist()
    bottom_5 = avg_probs.nsmallest(5, 'average_prob')['Country'].tolist()
    selected_countries = top_5.copy()
    
    selected_countries.append('Canada') # include canada for comparison
    
    for c in bottom_5:
        selected_countries.append(c)
   

    # Filter for selected countries
    df_selected = df_countries_prob[df_countries_prob['Country'].isin(selected_countries)].copy()

    # Set ordering for timeline
    df_selected['Country'] = pd.Categorical(df_selected['Country'], categories=selected_countries, ordered=True)
  
    # Generate plot
    country_timelines = country_timeline(df_selected)

    country_timelines.write_image(COUNTRY_TIMELINE)
    country_timelines.write_html(COUNTRY_TIME_HTML)




    
if __name__ == "__main__":
    main() 