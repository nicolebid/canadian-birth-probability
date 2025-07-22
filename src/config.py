import os

# Directories
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# File paths 
DATA_DB = os.path.join(ROOT_DIR, 'data/data.db') 
DATA_CSV = os.path.join(ROOT_DIR, 'data/country_br_pop.csv')
DATA_ALL_PROB_CSV = os.path.join(ROOT_DIR, 'data/countries_prob.csv')
DATA_BIRTHS_CSV = os.path.join(ROOT_DIR, 'data/data_br_pop_births.csv')

YR_2012_EX = os.path.join(ROOT_DIR, 'output/yr_2012.npy')
YR_2012_RATIO = os.path.join(ROOT_DIR, 'output/yr_2012_ratio.npy')
GLOBAL_AVG_BIRTHS = os.path.join(ROOT_DIR, 'output/global_avg_births.npy')

CANADA_BARCHART = os.path.join(ROOT_DIR, 'output/canada_barchart.png')
CANADA_TIMELINE = os.path.join(ROOT_DIR, 'output/canada_timeline.png')
COUNTRY_TIMELINE = os.path.join(ROOT_DIR, 'output/country_timeline.png')

CAN_BAR_HTML = os.path.join(ROOT_DIR, "output/canada_barchart_2012.html")
CANADA_TIME_HTML = os.path.join(ROOT_DIR, "output/canada_timeline.html")
COUNTRY_TIME_HTML = os.path.join(ROOT_DIR, 'output/country_timeline.html')