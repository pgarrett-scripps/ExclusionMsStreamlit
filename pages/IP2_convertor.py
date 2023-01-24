import json
from io import StringIO

import streamlit as st
from serenipy.dtaselectfilter import from_dta_select_filter
from exclusionms.components import ExclusionPoint

from utils import get_tolerance

st.header('Convert IP2 files to Intervals')

ip2_files = st.file_uploader(label='IP2 File', type='.txt', accept_multiple_files=True)
x_corr_threshold = st.number_input(label='Xcorr filter', value= 0.0)

# Only used with Add
st.subheader('Exclusion Interval Tolerance')
tolerance = get_tolerance()

if st.button('Run'):

    if not ip2_files:
        st.warning(f'Upload a ip2 file!')
        st.stop()

    intervals = []
    for ip2_file in ip2_files:
        ip2_file_content = StringIO(ip2_file.getvalue().decode("utf-8"))

        if ip2_file.name.endswith('.txt'):
            version, header, dta_results, info = from_dta_select_filter(ip2_file_content)
            num_intervals = sum([len(dta_result.peptide_lines) for dta_result in dta_results])
            for dta_result in dta_results:
                for peptide_line in dta_result.peptide_lines:
                    if peptide_line.x_corr < x_corr_threshold:
                        continue

                    exclusion_point = ExclusionPoint(charge=peptide_line.charge,
                                                     mass=peptide_line.mass_plus_hydrogen - 1.00727647,
                                                     rt=peptide_line.ret_time,
                                                     ook0=peptide_line.ion_mobility,
                                                     intensity=peptide_line.total_intensity)

                    interval = tolerance.construct_interval(peptide_line.sequence, exclusion_point)
                    intervals.append(interval)
        else:
            st.error(f'File Type Not supported!')
            continue

    file_contents = json.dumps([interval.dict() for interval in intervals])
    st.download_button(label='Download Intervals',
                       data=file_contents,
                       file_name=f'intervals.txt')

