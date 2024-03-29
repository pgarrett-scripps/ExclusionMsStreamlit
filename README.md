# ExclusionMsStreamlit

This Streamlit application provides an easy-to-use interface for managing and interacting with the ExclusionMS system. 
ExclusionMS is designed to manage exclusion lists for mass spectrometry experiments, offering various functionalities 
such as querying, adding, and removing exclusion intervals in real-time.

## Features

The ExclusionMS Streamlit Application includes the following features (pages):

- **Exclusion List:** Displays and manages the active exclusion list.
- **Debugger:** Allows users to add random intervals to the exclusion list, and query random exclusion points.
- **Generate:** Paser Key: Generates a Paser Key for enabling ExclusionMS.
- **Interval:** Lets users add, remove, and query exclusion intervals.
- **Convert IP2 Files to Intervals:** Converts IP2 files to ExclusionMS intervals with user-defined tolerances.
- **Point:** Queries the exclusion list based on a given Exclusion Point.

## Install 

Requires ExclusionMsAPI is running.

### ExclusionMsStreamlit
```
git clone https://github.com/pgarrett-scripps/ExclusionMsStreamlit.git
cd ExclusionMsStreamlit
pip install -r requirements.txt
```

### ExclusionMsAPI
Install Instructions can be found here: https://github.com/pgarrett-scripps/ExclusionMsApi

## Usage

```
# streamlit run .\home.py -- ExclusionMsAPI:Port
streamlit run .\home.py -- 127.0.0.1:8000 
```
