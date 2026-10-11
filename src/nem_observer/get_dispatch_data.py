import pandas as pd
import os
import numpy as np
from datetime import timedelta
from nemosis import static_table, dynamic_data_compiler, defaults
import plotly.express as px
from datetime import datetime

raw_data_cache = './src/nem_observer/data/data_cache'
if os .path.exists(raw_data_cache) is False:
    os.makedirs(raw_data_cache)


def get_dispatch_data(end_date=datetime.now(), length_day=1, duid=None):

    ## This calculates the time of midnight of the given end date
    end_time = end_date.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y/%m/%d %H:%M:%S")
    print(end_time) 
    start_time = (end_date - timedelta(days=length_day)).replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y/%m/%d %H:%M:%S")
    print(start_time)

    table = 'DISPATCH_UNIT_SCADA'
    price_data = dynamic_data_compiler(start_time, end_time, table, raw_data_cache)
# print(defaults.dynamic_tables)
get_dispatch_data(end_date=datetime(2022, 7, 15, 0, 0), length_day=1, duid=None)

