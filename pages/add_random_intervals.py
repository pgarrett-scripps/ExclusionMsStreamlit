import time

import pandas as pd
import streamlit as st

from exclusionms.apihandler import add_exclusion_interval_query
from exclusionms.components import ExclusionInterval, DynamicExclusionTolerance, ExclusionPoint
from constants import EXCLUSION_MS_API_IP
st.header('Populate Active Exclusion List with Random intervals')

num_intervals = st.number_input(label='Random Intervals', value=100_000, min_value=100)

st.subheader('Random number min/max bounds')
min_charge, max_charge = st.slider(label='min/max charge', min_value=0, max_value=10, value=(1, 5))
min_mass, max_mass = st.slider(label='min/max mass', min_value=0, max_value=10_000, value=(500, 5_000))
min_rt, max_rt = st.slider(label='min/max rt', min_value=0, max_value=10_000, value=(500, 5_000))
min_ook0, max_ook0 = st.slider(label='min/max ook0', min_value=0.0, max_value=2.0, value=(0.2, 1.5))
min_intensity, max_intensity = st.slider(label='min/max intensity', min_value=0, max_value=100_000, value=(500, 50_000))

st.subheader('Exclusion Interval Tolerance')
use_exact_charge = st.checkbox('Use exact charge', value=False)
mass_tolerance = st.text_input(label='mass Tolerance', value='50')
rt_tolerance = st.text_input(label='rt Tolerance', value='100')
ook0_tolerance = st.text_input(label='ook0 Tolerance', value='0.05')
intensity_tolerance = st.text_input(label='Intensity Tolerance', value='0.5')


if st.button('Add'):

    tolerance = DynamicExclusionTolerance.from_strings(exact_charge=use_exact_charge, mass_tolerance=mass_tolerance,
                                                       rt_tolerance=rt_tolerance, ook0_tolerance=ook0_tolerance,
                                                       intensity_tolerance=intensity_tolerance)

    times = []
    sizes = []
    start_time = time.time()
    for i in range(num_intervals):
        random_exclusion_point = ExclusionPoint.generate_random(min_charge=min_charge, max_charge=max_charge,
                                                                min_mass=min_mass, max_mass=max_mass,
                                                                min_rt=min_rt, max_rt=max_rt,
                                                                min_ook0=min_ook0, max_ook0=max_ook0,
                                                                min_intensity=min_intensity, max_intensity=max_intensity)
        random_interval = tolerance.construct_interval(interval_id='testing', exclusion_point=random_exclusion_point)
        add_exclusion_interval_query(exclusion_api_ip=EXCLUSION_MS_API_IP, exclusion_interval=random_interval)

        if i % int(num_intervals/100) == 0:
            sizes.append(i)
            times.append(time.time() - start_time)

    df = pd.DataFrame({'size':sizes, 'time':times})
    st.line_chart(data=df, x='size', y='time')









