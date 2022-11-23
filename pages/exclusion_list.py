import json

import exclusionms.apihandler
import requests
import streamlit as st

from constants import EXCLUSION_MS_API_IP

saved_files = json.loads(requests.get(f'{EXCLUSION_MS_API_IP}/exclusionms').content)['files']

st.subheader('Active Exclusion List')

col1, col2 = st.columns(2)
if col1.button("Clear"):
    response = requests.delete(f'{EXCLUSION_MS_API_IP}/exclusionms')
    st.write(response.status_code)
    st.write(response.content)

if col2.button("Stats"):
    response = requests.get(f'{EXCLUSION_MS_API_IP}/exclusionms')
    st.write(response.status_code)
    st.write(json.loads(response.content)['active_exclusion_list'])

st.markdown('---')

st.subheader('Save Active Exclusion List')
name = st.text_input('File Name')
if st.button("Save"):
    exclusionms.apihandler.save_active_exclusion_list(EXCLUSION_MS_API_IP, name)

st.markdown('---')

st.subheader('Load/Delete/Download Exclusion List')
file_option = st.selectbox(label='Select File', options=saved_files, key='load')
col1, col2, col3 = st.columns(3)
if col1.button("Load"):
    exclusionms.apihandler.load_active_exclusion_list(EXCLUSION_MS_API_IP, file_option)

if col2.button("Delete"):
    exclusionms.apihandler.download_exclusion_list_save(EXCLUSION_MS_API_IP, file_option)

if col3.button("Download"):
    def download_file(name):
        download = exclusionms.apihandler.download_exclusion_list_save(EXCLUSION_MS_API_IP, name)
        return download
    st.download_button('Download', download_file(file_option), file_name=f'{file_option}.pkl')

st.markdown('---')

st.subheader('Upload Exclusion List')
file_upload = st.file_uploader(label='Upload exclusion file')
if st.button("Upload"):
    st.write('Not implemented...')
    pass