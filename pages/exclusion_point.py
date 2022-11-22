import exclusionms.apihandler
import streamlit as st
from exclusionms.components import ExclusionInterval, ExclusionPoint
from exclusionms.exceptions import UnexpectedStatusCodeException
from utils import convert_int, convert_float, convert_str
from constants import EXCLUSION_MS_API_IP


st.header('ExclusionPoint')

charge = convert_int(st.text_input(label='charge', value=''))
mass = convert_float(st.text_input(label='mass', value=''))
rt = convert_float(st.text_input(label='rt', value=''))
ook0 = convert_float(st.text_input(label='ook0', value=''))
intensity = convert_float(st.text_input(label='intensity', value=''))

response = None
interval_query = None
if st.button('query'):
    exclusion_point = ExclusionPoint(charge=charge, mass=mass, rt=rt, ook0=ook0, intensity=intensity)

    try:
        intervals = exclusionms.apihandler.get_intervals_from_point(exclusion_api_ip=EXCLUSION_MS_API_IP,exclusion_point=exclusion_point)
        interval_jsons = [interval.dict() for interval in intervals]
        st.subheader('Overlapping Intervals:')
        if interval_jsons:
            st.write(interval_jsons)
    except UnexpectedStatusCodeException as ex:
        st.error(f'Problem Adding Interval: {ex}')
        st.stop()

