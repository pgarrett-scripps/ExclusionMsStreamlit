import streamlit as st
from exclusionms.apihandler import add_exclusion_interval
from senpy.dtaselectfilter import from_dta_select_filter
from exclusionms.components import ExclusionPoint, DynamicExclusionTolerance

from constants import EXCLUSION_MS_API_IP

st.header('Convert IP2 files to Intervals')

ip2_file = st.file_uploader(label='IP2 File', type=['.sqt', '.ms2', '.txt'])

# Only used with Add
st.subheader('Exclusion Interval Tolerance')
use_exact_charge = st.checkbox('Use exact charge', value=False)
mass_tolerance = st.text_input(label='mass Tolerance', value='50')
rt_tolerance = st.text_input(label='rt Tolerance', value='100')
ook0_tolerance = st.text_input(label='ook0 Tolerance', value='0.05')
intensity_tolerance = st.text_input(label='Intensity Tolerance', value='0.5')

if st.button('Run'):

    if not ip2_file:
        st.warning(f'Upload a ip2 file!')
        st.stop()

    ip2_file_content = ip2_file.read().decode('utf-8')

    tolerance = DynamicExclusionTolerance.from_strings(exact_charge=use_exact_charge, mass_tolerance=mass_tolerance,
                                                       rt_tolerance=rt_tolerance, ook0_tolerance=ook0_tolerance,
                                                       intensity_tolerance=intensity_tolerance)

    if ip2_file.name.endswith('.sqt'):
        st.warning(f'Not implemented yet!')
        st.stop()
    elif ip2_file.name.endswith('.ms2'):
        st.warning(f'Not implemented yet!')
        st.stop()
    elif ip2_file.name.endswith('.txt'):
        version, header, dta_results, info = from_dta_select_filter(ip2_file_content)
        bar = st.progress(0)
        num_intervals = sum([len(dta_result.peptide_lines) for dta_result in dta_results])
        st.info(f'Uploading {num_intervals} intervals!')
        i = 0
        for dta_result in dta_results:
            for peptide_line in dta_result.peptide_lines:
                exclusion_point = ExclusionPoint(charge=peptide_line.charge,
                                                 mass=peptide_line.mass_plus_hydrogen - 1.00727647,
                                                 rt=peptide_line.ret_time,
                                                 ook0=peptide_line.ion_mobility,
                                                 intensity=peptide_line.total_intensity)

                interval = tolerance.construct_interval(peptide_line.sequence, exclusion_point)
                add_exclusion_interval(exclusion_api_ip=EXCLUSION_MS_API_IP, exclusion_interval=interval)
                i += 1

                if i % 100 == 0:
                    bar.progress(float(i / num_intervals))

    else:
        st.error(f'File Type Not supported!')
        st.stop()
