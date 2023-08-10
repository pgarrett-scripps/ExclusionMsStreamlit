import json

import exclusionms.apihandler
from exclusionms.components import ExclusionInterval
import streamlit as st

from constants import EXCLUSION_MS_API_IP

saved_files = exclusionms.apihandler.get_files(EXCLUSION_MS_API_IP)

st.subheader('Active Exclusion List')


col1, col2, col3 = st.columns(3)
if col1.button("Clear Intervals"):
    response = exclusionms.apihandler.clear(EXCLUSION_MS_API_IP)
    st.success(f'Cleared {response} intervals!')


if col2.button("Exclusion Stats"):
    stats = exclusionms.apihandler.get_statistics(EXCLUSION_MS_API_IP)
    tree_length = stats['interval_tree']

    st.metric(label='Intervals', value=tree_length)

    #st.write(response.status_code)
    #st.write(json.loads(response.content)['active_exclusion_list'])

if col3.button("Download Intervals"):
    exclusion_interval = ExclusionInterval(interval_id=None, charge=None, min_mass=None, max_mass=None,
                                           min_rt=None, max_rt=None, min_ook0=None, max_ook0=None,
                                           min_intensity=None, max_intensity=None)

    intervals = exclusionms.apihandler.search_interval(exclusion_api_ip=EXCLUSION_MS_API_IP, exclusion_interval=exclusion_interval)
    file_contents = json.dumps([interval.dict() for interval in intervals])
    st.download_button(label='Download Intervals',
                       data=file_contents,
                       file_name=f'intervals.txt')

st.markdown('---')
st.subheader('Upload Intervals')

interval_file = st.file_uploader(label='Interval File')

if st.button('Add Intervals'):
    intervals = json.loads(interval_file.getvalue().decode("utf-8"))
    intervals = [ExclusionInterval.from_dict(interval) for interval in intervals]
    exclusionms.apihandler.add_intervals(exclusion_api_ip=EXCLUSION_MS_API_IP, exclusion_intervals=intervals)
    st.success(f'Added {len(intervals)} intervals!')
st.markdown('---')

st.subheader('Save')
name = st.text_input('File Name')
if st.button("Save"):
    exclusionms.apihandler.save(EXCLUSION_MS_API_IP, name)

st.markdown('---')

st.subheader('Load & Delete')
file_option = st.selectbox(label='Select File', options=saved_files, key='load')
col1, col2 = st.columns(2)
if col1.button("Load"):
    exclusionms.apihandler.load(EXCLUSION_MS_API_IP, file_option)

if col2.button("Delete"):
    exclusionms.apihandler.delete(EXCLUSION_MS_API_IP, file_option)