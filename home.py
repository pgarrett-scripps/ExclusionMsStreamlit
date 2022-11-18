import sys

import streamlit as st

st.header('ExclusionMS Streamlit Homepage')
st.markdown("""
### What is ExclusionMS?

ExclusionMS is a platform to enable custom/dynamic exclusion list support for mass spectrometers. It contains 2 main components:

1) Streamlit application (this app)

2) Fast API server (what this app communicates with)

The Streamlit app serves an interactive GUI for the Fast API server, which manages the exclusion list.

### How does the the ExclusionMs work?

There is always a single 'active' exclusion list loaded, so all commands function in regards to the 'active'
list. For example, you can save, load, or delete the active exclusion lists. You can also add/delete/query exclusion 
intervals.

ExclusionMS uses 2 underlying data types: ExclusionInterval's and ExclusionPoint's. An ExclusionInterval is a
 multi-dimensional interval specified by min/max bounds of an ions properties, while an ExclusionPoint is a multi-dimensional
 point in the same space.
   
Ionic Properties (aka Exclusion Dimensions):
1) Charge
2) Mass
3) RT
4) ook0
5) Intensity

 An example ExclusionInterval: {'id': 'example', 'charge': '2', 'min_mass': '793', 'max_mass': '794', 'min_rt': '100', 'max_rt': '105', 'min_ook0': 'None', 'max_ook0': 'None', 'min_intensity': '5000', 'max_intensity': '10000'}

It is possible to set any value of an Exclusion Interval or Point to None, which will effectively disable that 
dimension by setting the min/max bounds to be min/max float values (makes it 'all inclusive')
""")
