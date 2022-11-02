import json
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

st.subheader('Save Active Exclusion List')
name = st.text_input('File Name')
if st.button("Save"):
    response = requests.post(f'{EXCLUSION_MS_API_IP}/exclusionms?save=True&exclusion_list_name={name}')
    st.write(response.status_code)
    st.write(response.content)

st.subheader('Load/Delete/Download Exclusion List')
file_option = st.selectbox(label='Select File', options=saved_files, key='load')
col1, col2, col3 = st.columns(3)
if col1.button("Load"):
    response = requests.post(f'{EXCLUSION_MS_API_IP}/exclusionms?save=False&exclusion_list_name={file_option}')
    st.write(response.status_code)
    st.write(response.content)

if col2.button("Delete"):
    response = requests.delete(f'{EXCLUSION_MS_API_IP}/exclusionms/file?exclusion_list_name={file_option}')
    st.write(response.status_code)
    st.write(response.content)

if col3.button("Download"):
    def download_file(name):
        response = requests.get(f'{EXCLUSION_MS_API_IP}/exclusionms/file?exclusion_list_name={name}')
        st.write(response.status_code)
        return response.content
    st.download_button('Download', download_file(name), file_name=f'{file_option}.pkl')

st.subheader('Upload Exclusion List')
file_upload = st.file_uploader(label='Upload exclusion file')
if st.button("Upload"):
    st.write('Not implemented...')
    pass