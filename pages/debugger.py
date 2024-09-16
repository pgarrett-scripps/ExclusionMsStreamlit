import random
import time

import exclusionms.apihandler
import streamlit as st
import exclusionms
from exclusionms.components import ExclusionPoint

from constants import EXCLUSION_MS_API_IP
from utils import get_tolerance

st.header('Debugger')

with st.expander('Help'):
    st.markdown("""
    The Debugger is a testing tool for the ExclusionMS API.
    
    What can it do?
    
    1) Add random exclusion intervals (uses tolerance and min/max)
    
    2) Query random exclusion points (uses only min/max)
    
    3) Save random Exclusion intervals to a file (uses tolerance and min/max)
    """)

num_intervals = st.number_input(label='Number of Intervals', value=1_000, min_value=1)
show_msg = st.checkbox(label='Show Messages')
# Used with add and Query
with st.expander('Bounds'):
    min_charge, max_charge = st.slider(label='min/max charge', min_value=0, max_value=10, value=(1, 5))
    min_mass, max_mass = st.slider(label='min/max mass', min_value=0, max_value=10_000, value=(500, 5_000))
    min_rt, max_rt = st.slider(label='min/max rt', min_value=0, max_value=10_000, value=(500, 5_000))
    min_ook0, max_ook0 = st.slider(label='min/max ook0', min_value=0.0, max_value=2.0, value=(0.2, 1.5))
    min_intensity, max_intensity = st.slider(label='min/max intensity', min_value=0, max_value=100_000,
                                             value=(500, 50_000))
    if min_intensity == 0 and max_intensity == 0:
        min_intensity, max_intensity = None, None

    if min_ook0 == 0 and max_ook0 == 0:
        min_ook0, max_ook0 = None, None

    if min_rt == 0 and max_rt == 0:
        min_rt, max_rt = None, None

    if min_mass == 0 and max_mass == 0:
        min_mass, max_mass = None, None

    if min_charge == 0 and max_charge == 0:
        min_charge, max_charge = None, None

# Only used with Add
with st.expander('Tolerance'):
    tolerance = get_tolerance()

add_btn, query_btn = st.columns(2)


def make_random_point(min_charge, max_charge, min_mass, max_mass, min_rt, max_rt, min_ook0, max_ook0, min_intensity,
                      max_intensity):
    charge = None
    if min_charge and max_charge:
        charge = random.randint(min_charge, max_charge)

    mass = None
    if min_mass and max_mass:
        mass = random.uniform(min_mass, max_mass)

    rt = None
    if min_rt and max_rt:
        rt = random.uniform(min_rt, max_rt)

    ook0 = None
    if min_ook0 and max_ook0:
        ook0 = random.uniform(min_ook0, max_ook0)

    intensity = None
    if min_intensity and max_intensity:
        intensity = random.uniform(min_intensity, max_intensity)

    return ExclusionPoint(charge=charge, mass=mass, rt=rt, ook0=ook0, intensity=intensity)


if add_btn.button('Add Intervals'):

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

    if show_msg:
        json_msg = [interval.dict() for interval in intervals]
        st.write(json_msg)

    exclusionms.apihandler.add_intervals(exclusion_api_ip=EXCLUSION_MS_API_IP,
                                         exclusion_intervals=intervals)

    with st.expander('Query'):
        for q in queries:
            st.write(q)

    st.metric(label='Time', value=time.time() - start_time)

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
    exclusion_flags = exclusionms.apihandler.exclusion_search_points(exclusion_api_ip=EXCLUSION_MS_API_IP,
                                                                     exclusion_points=exclusion_points)
    end_time = time.time()
    st.metric(label='time', value=end_time - start_time)

    with st.expander('Results'):
        st.write(exclusion_flags)
