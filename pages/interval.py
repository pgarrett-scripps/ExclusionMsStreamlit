import streamlit as st

from exclusionms.apihandler import add_exclusion_interval_query, get_exclusion_interval_query, \
    delete_exclusion_interval_query
from exclusionms.components import ExclusionInterval
from exclusionms.exceptions import UnexpectedStatusCodeException
from utils import convert_int, convert_float, convert_str
from constants import EXCLUSION_MS_API_IP


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
    exclusion_interval = ExclusionInterval(id=interval_id, charge=charge, min_mass=min_mass, max_mass=max_mass,
                                           min_rt=min_rt, max_rt=max_rt, min_ook0=min_ook0, max_ook0=max_ook0,
                                           min_intensity=min_intensity, max_intensity=max_intensity)

    try:
        add_exclusion_interval_query(exclusion_api_ip=EXCLUSION_MS_API_IP,exclusion_interval=exclusion_interval)
    except UnexpectedStatusCodeException as ex:
        st.error(f'Problem Adding Interval: {ex}')


if c2.button('Remove'):

    exclusion_interval = ExclusionInterval(id=interval_id, charge=charge, min_mass=min_mass, max_mass=max_mass,
                                           min_rt=min_rt, max_rt=max_rt, min_ook0=min_ook0, max_ook0=max_ook0,
                                           min_intensity=min_intensity, max_intensity=max_intensity)

    try:
        delete_exclusion_interval_query(exclusion_api_ip=EXCLUSION_MS_API_IP, exclusion_interval=exclusion_interval)
    except UnexpectedStatusCodeException as ex:
        st.error(f'Problem Adding Interval: {ex}')


if c3.button('Query'):

    exclusion_interval = ExclusionInterval(id=interval_id, charge=charge, min_mass=min_mass, max_mass=max_mass,
                                           min_rt=min_rt, max_rt=max_rt, min_ook0=min_ook0, max_ook0=max_ook0,
                                           min_intensity=min_intensity, max_intensity=max_intensity)

    results = get_exclusion_interval_query(exclusion_api_ip=EXCLUSION_MS_API_IP, exclusion_interval=exclusion_interval)
    if results:
        st.write(results)

