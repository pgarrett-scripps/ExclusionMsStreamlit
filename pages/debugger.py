import random
import time

import exclusionms.apihandler
import matplotlib.pyplot as plt
import streamlit as st
import exclusionms
from exclusionms.components import DynamicExclusionTolerance, ExclusionPoint

from constants import EXCLUSION_MS_API_IP

st.header('Populate Active Exclusion List with Random intervals')

with st.expander('Help'):
    st.markdown("""
    The Debugger is a testing tool for the ExclusionMS API.
    
    What can it do?
    
    1) Add random exclusion intervals (uses tolerance and min/max)
    
    2) Query random exclusion points (uses only min/max)
    
    3) Save random Exclusion intervals to a file (uses tolerance and min/max)
    """)

num_intervals = st.number_input(label='Random Intervals', value=1_000, min_value=100)

# Used with add and Query
st.subheader('Random number min/max bounds')
min_charge, max_charge = st.slider(label='min/max charge', min_value=0, max_value=10, value=(1, 5))
min_mass, max_mass = st.slider(label='min/max mass', min_value=0, max_value=10_000, value=(500, 5_000))
min_rt, max_rt = st.slider(label='min/max rt', min_value=0, max_value=10_000, value=(500, 5_000))
min_ook0, max_ook0 = st.slider(label='min/max ook0', min_value=0.0, max_value=2.0, value=(0.2, 1.5))
min_intensity, max_intensity = st.slider(label='min/max intensity', min_value=0, max_value=100_000, value=(500, 50_000))

# Only used with Add
st.subheader('Exclusion Interval Tolerance')
use_exact_charge = st.checkbox('Use exact charge', value=False)
mass_tolerance = st.text_input(label='mass Tolerance', value='50')
rt_tolerance = st.text_input(label='rt Tolerance', value='100')
ook0_tolerance = st.text_input(label='ook0 Tolerance', value='0.05')
intensity_tolerance = st.text_input(label='Intensity Tolerance', value='0.5')

add_btn, query_btn, interval_file_btn = st.columns(3)


def make_random_point(min_charge, max_charge, min_mass, max_mass, min_rt, max_rt, min_ook0, max_ook0, min_intensity,
                      max_intensity):
    charge = random.randint(min_charge, max_charge)
    mass = random.uniform(min_mass, max_mass)
    rt = random.uniform(min_rt, max_rt)
    ook0 = random.uniform(min_ook0, max_ook0)
    intensity = random.uniform(min_intensity, max_intensity)

    return ExclusionPoint(charge=charge, mass=mass, rt=rt, ook0=ook0, intensity=intensity)


if add_btn.button('Add Interval'):

    tolerance = DynamicExclusionTolerance.from_strings(exact_charge=use_exact_charge, mass_tolerance=mass_tolerance,
                                                       rt_tolerance=rt_tolerance, ook0_tolerance=ook0_tolerance,
                                                       intensity_tolerance=intensity_tolerance)

    times = []
    sizes = []
    start_time = time.time()
    queries = []
    intervals = []
    for i in range(num_intervals):
        random_exclusion_point = make_random_point(min_charge=min_charge, max_charge=max_charge,
                                                   min_mass=min_mass, max_mass=max_mass,
                                                   min_rt=min_rt, max_rt=max_rt,
                                                   min_ook0=min_ook0, max_ook0=max_ook0,
                                                   min_intensity=min_intensity,
                                                   max_intensity=max_intensity)
        random_interval = tolerance.construct_interval(interval_id='testing', exclusion_point=random_exclusion_point)
        intervals.append(random_interval)
    exclusionms.apihandler.add_exclusion_intervals(exclusion_api_ip=EXCLUSION_MS_API_IP,
                                                   exclusion_intervals=intervals)

    with st.expander('Query'):
        for q in queries:
            st.write(q)

    st.metric(label='Time', value=time.time()-start_time)

if query_btn.button('Query Points'):

    exclusion_points = []
    for i in range(num_intervals):
        random_exclusion_point = make_random_point(min_charge=min_charge, max_charge=max_charge,
                                                   min_mass=min_mass, max_mass=max_mass,
                                                   min_rt=min_rt, max_rt=max_rt,
                                                   min_ook0=min_ook0, max_ook0=max_ook0,
                                                   min_intensity=min_intensity,
                                                   max_intensity=max_intensity)

        exclusion_points.append(random_exclusion_point)

    start_time = time.time()
    exclusion_flags = exclusionms.apihandler.get_excluded_points(exclusion_api_ip=EXCLUSION_MS_API_IP,
                                                                 exclusion_points=exclusion_points)
    st.metric(label='time', value=time.time() - start_time)

    with st.expander('Results'):
        st.write(exclusion_flags)

    fig = plt.figure()
    plt.hist([int(b) for b in exclusion_flags])
    st.pyplot(fig)


if interval_file_btn.button('Generate Interval File'):

    interval_dict_strs = []

    tolerance = DynamicExclusionTolerance.from_strings(exact_charge=use_exact_charge, mass_tolerance=mass_tolerance,
                                                       rt_tolerance=rt_tolerance, ook0_tolerance=ook0_tolerance,
                                                       intensity_tolerance=intensity_tolerance)

    for i in range(num_intervals):
        random_exclusion_point = make_random_point(min_charge=min_charge, max_charge=max_charge,
                                                   min_mass=min_mass, max_mass=max_mass,
                                                   min_rt=min_rt, max_rt=max_rt,
                                                   min_ook0=min_ook0, max_ook0=max_ook0,
                                                   min_intensity=min_intensity,
                                                   max_intensity=max_intensity)
        random_interval = tolerance.construct_interval(interval_id='testing', exclusion_point=random_exclusion_point)
        interval_dict_strs.append(f'{str(random_interval.dict())}\n')

    file_contents = ''.join(interval_dict_strs)

    st.download_button(label='Download Interval File', data=file_contents, file_name='intervals.txt')
