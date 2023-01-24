import json
import streamlit as st

from utils import get_tolerance

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
    tolerance = get_tolerance()

    paser_key['exclusionms']['tolerance'] = tolerance.dict()


st.subheader('ExclusionMS Paser Key:')
st.write(str(json.dumps(paser_key)))
