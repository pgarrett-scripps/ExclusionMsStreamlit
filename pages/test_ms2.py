import time
from io import StringIO

from exclusionms.components import ExclusionPoint
from serenipy.ms2 import from_ms2
import streamlit as st
import exclusionms.apihandler

from constants import EXCLUSION_MS_API_IP
from utils import get_tolerance

ms2_file = st.file_uploader(label='MS2 File', type='.ms2')

# Only used with Add
st.subheader('Exclusion Interval Tolerance')
tolerance = get_tolerance()

bar = st.progress(0)

if st.button('Run'):

    header_lines, ms2_spectras = from_ms2(StringIO(ms2_file.getvalue().decode("utf-8")))

    intervals = []
    points = []
    for i, ms2_spectra in enumerate(ms2_spectras):
        point = ExclusionPoint(mass=ms2_spectra.mass, charge=ms2_spectra.charge, rt=ms2_spectra.rt,
                               ook0=ms2_spectra.ook0, intensity=ms2_spectra.prec_intensity)
        interval = tolerance.construct_interval(interval_id='ms2', exclusion_point=point)
        intervals.append(interval)
        points.append(point)

        if i % 100 == 0:
            bar.progress(i/len(ms2_spectras))

    exclusionms.apihandler.clear_active_exclusion_list(exclusion_api_ip=EXCLUSION_MS_API_IP)
    exclusionms.apihandler.add_exclusion_intervals(exclusion_api_ip=EXCLUSION_MS_API_IP, exclusion_intervals=intervals)

    start_time = time.time()
    exclusion_flags = exclusionms.apihandler.get_excluded_points(exclusion_api_ip=EXCLUSION_MS_API_IP, exclusion_points=points)
    st.metric(label='time', value=time.time() - start_time)

    with st.expander('Results'):
        st.write(exclusion_flags)


