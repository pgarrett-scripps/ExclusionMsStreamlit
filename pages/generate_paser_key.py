import json
import streamlit as st

from exclusionms.components import DynamicExclusionTolerance

st.header('Make ExclusionMS Key')
with st.expander('Help'):
    st.markdown('''
    This app will generate a Paser Key to enable ExclusionMS.

    There are a few ways to use ExclusionMS:
    1) Dynamic
    2) Offline (manual)
    
    Dynamic mode will automatically add exclusion intervals based on the fragmented precursor ionic properties: 
    (charge, mass, retention time, mobility, and intensity). This mode requires using inputted tolerances to create 
    intervals from the fragmented ions. It is possible to leave any tolerance blank, which will cause this property to
    be ignored.

    Offline (manual) mode requires that you create the exclusion list prior to acquisition. For example, you could
    upload intervals from a file, or spectral library which will 'pre load' these intervals into the exclusion list and
    any experiment with a matching EXID in its paser_key will use this exclusion list.
    
    It is also possible to use a combination of the two. For example you could preload 'intervals' into a exclusion 
    list and then use 'dynamic exclusion' to add additional fragmented ions. 
    ''')


paser_key = st.text_input(label='paser key', help='can get from the paser homepage (paserKeyGenerator.html)')
exid = st.text_input(label='EXID', value='', help='The unique name of the exclusion list.')
dynamic_exclusion = st.checkbox(label='Use Dynamic Exclusion', value=False, help='automatically add intervals to the exclusion list based on fragemnted ions.')

if not paser_key:
    st.warning(f'Input Paser Key!')
    st.stop()


paser_key = json.loads(paser_key)
exid = exid if exid else None
paser_key['exclusionms'] = {'exid': exid, 'dynamic': dynamic_exclusion}

if dynamic_exclusion:

    # Only used with Add
    st.subheader('Exclusion Interval Tolerance')
    use_exact_charge = st.checkbox('Use exact charge', value=False, help='Will require that a ExclusionInterval have the same charge in order to exclude.')
    mass_tolerance = st.text_input(label='mass Tolerance', value='', help='Represents the mass tolerance (in ppm): mass +/- mass*mass_tolerance/1_000_000')
    rt_tolerance = st.text_input(label='rt Tolerance', value='', help='Represents the rt tolerance (in seconds): rt +/- rt_tolerance')
    ook0_tolerance = st.text_input(label='ook0 Tolerance', value='', help='Represents the ook0 tolerance (in %): ook0 +/- ook0*ook0_tolerance')
    intensity_tolerance = st.text_input(label='Intensity Tolerance', value='', help='Represents the intensity tolerance (in %): intensity +/- intensity*intensity_tolerance')

    tolerance = DynamicExclusionTolerance(charge=use_exact_charge,
                                          mass=float(mass_tolerance) if mass_tolerance else None,
                                          rt=float(rt_tolerance) if rt_tolerance else None,
                                          ook0=float(ook0_tolerance) if ook0_tolerance else None,
                                          intensity=float(intensity_tolerance) if intensity_tolerance else None)

    paser_key['exclusionms']['tolerance'] = tolerance.dict()


st.subheader('ExclusionMS Paser Key:')
st.write(str(json.dumps(paser_key)))
