import streamlit as st
from exclusionms import apihandler
import plotly.express as px

from constants import EXCLUSION_MS_API_IP

# Streamlit application
st.title('API History')

plot_container = st.empty()
num_entries = st.number_input('Num Entries', 500)
if st.button('Run'):
    timings = apihandler.get_log_entries(EXCLUSION_MS_API_IP, num_entries=500)
    d = {'timestamp': [], 'time_taken': [], 'url': []}
    for t in timings:
        d['timestamp'].append(t['timestamp'])
        d['time_taken'].append(t['time_taken'])
        d['url'].append(t['request']['url'].split('/')[-1])

    fig = px.scatter(d, x='timestamp', y='time_taken', color='url')
    plot_container.plotly_chart(fig)
