import time
import traceback

import streamlit as st
from exclusionms.apihandler import add_exclusion_interval_query
from exclusionms.components import ExclusionInterval
from exclusionms.exceptions import UnexpectedStatusCodeException

from constants import EXCLUSION_MS_API_IP

st.header('Upload intervals from file')

with st.expander('Example File'):
    st.code("""{'id': 'testing', 'charge': 'None', 'min_mass': '4793.648071543348', 'max_mass': '4794.127460319942', 'min_rt': '1795.5161653090868', 'max_rt': '1995.5161653090868', 'min_ook0': '1.4130889560519646', 'max_ook0': '1.5130889560519647', 'min_intensity': '48877.013731932144', 'max_intensity': '48878.013731932144'}
{'id': 'testing', 'charge': 'None', 'min_mass': '2542.5471494809444', 'max_mass': '2542.801416909264', 'min_rt': '4083.6743867151863', 'max_rt': '4283.674386715186', 'min_ook0': '1.34100833885607', 'max_ook0': '1.4410083388560702', 'min_intensity': '16458.773544936346', 'max_intensity': '16459.773544936346'}
{'id': 'testing', 'charge': 'None', 'min_mass': '4453.44447551579', 'max_mass': '4453.889842231677', 'min_rt': '472.54394586499484', 'max_rt': '672.5439458649948', 'min_ook0': '0.7726771304511113', 'max_ook0': '0.8726771304511114', 'min_intensity': '26485.055189254774', 'max_intensity': '26486.055189254774'}
""")

interval_file = st.file_uploader(label='Interval File')

start_time = time.time()
if st.button('Add Intervals'):
    bar = st.progress(0)
    interval_lines = interval_file.getvalue().decode("utf-8").split("\n")
    exclusion_intervals = [ExclusionInterval.from_str(interval_str) for interval_str in interval_lines if interval_str]
    for i, interval in enumerate(exclusion_intervals):

        try:
            add_exclusion_interval_query(exclusion_api_ip=EXCLUSION_MS_API_IP, exclusion_interval=interval)
        except UnexpectedStatusCodeException as e:
            tb = traceback.format_exc()
            st.error(e)
            st.error(tb)

        if i % 100 == 0:
            bar.progress(float(i/len(exclusion_intervals)))

    bar.progress(1.0)

    st.metric(label='Time', value=time.time() - start_time)


