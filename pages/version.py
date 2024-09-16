import streamlit as st
import subprocess

def get_installed_packages():
    result = subprocess.run(['pip', 'list'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

st.title("Installed Pip Packages and Versions")

packages = get_installed_packages()
st.text(packages)
