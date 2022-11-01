import json

import streamlit as st
import requests

from utils import convert_int, convert_float, convert_str, make_interval_query
from constants import EXCLUSION_API_IP


st.header('Exclusion Interval')

interval_id = convert_str(st.text_input(label='interval_id', value=''))
charge = convert_int(st.text_input(label='charge', value=''))
c1, c2 = st.columns(2)
min_mass = convert_float(c1.text_input(label='min_mass', value=''))
max_mass = convert_float(c2.text_input(label='max_mass', value=''))
c1, c2 = st.columns(2)
min_rt = convert_float(c1.text_input(label='min_rt', value=''))
max_rt = convert_float(c2.text_input(label='max_rt', value=''))
c1, c2 = st.columns(2)
min_ook0 = convert_float(c1.text_input(label='min_ook0', value=''))
max_ook0 = convert_float(c2.text_input(label='max_ook0', value=''))
c1, c2 = st.columns(2)
min_intensity = convert_float(c1.text_input(label='min_intensity', value=''))
max_intensity = convert_float(c2.text_input(label='max_intensity', value=''))


c1,c2,c3 = st.columns(3)
response = None
interval_query = None
if c1.button('Add'):
    query = make_interval_query(interval_id, charge, min_mass, max_mass, min_rt, max_rt, min_ook0, max_ook0, min_intensity, max_intensity)
    interval_query = f'{EXCLUSION_API_IP}/exclusionlist/interval{query}'
    response = requests.post(interval_query)

if c2.button('Remove'):
    query = make_interval_query(interval_id, charge, min_mass, max_mass, min_rt, max_rt, min_ook0, max_ook0, min_intensity, max_intensity)
    interval_query = f'{EXCLUSION_API_IP}/exclusionlist/interval{query}'
    response = requests.delete(interval_query)

if c3.button('Query'):
    query = make_interval_query(interval_id, charge, min_mass, max_mass, min_rt, max_rt, min_ook0, max_ook0, min_intensity, max_intensity)
    interval_query = f'{EXCLUSION_API_IP}/exclusionlist/interval{query}'
    response = requests.get(interval_query)

if response:
    st.subheader('Query sting')
    st.write(interval_query)

    st.subheader('Status Code')
    st.write(response.status_code)

    st.subheader('Content')

    try:
        st.json(json.loads((response.content)))
    except json.decoder.JSONDecodeError:
        pass