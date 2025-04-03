import streamlit as st
import pandas as pd
import io
import requests

st.set_page_config(page_title='Searchable RVU Database', layout='wide')

@st.cache_data
def load_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        data = data.drop(columns=['MOD'], errors='ignore')
        return data
    else:
        st.error('Error loading file from GitHub')
        st.stop()

# Display the MILV logo from GitHub
logo_url = 'https://raw.githubusercontent.com/gibsona83/rvumilv/main/milv.png'
st.image(logo_url, width=200)
st.markdown("# Medical Imaging of Lehigh Valley, P.C.")
st.markdown("### Searchable Diagnostic Radiology wRVUs Database")

url = 'https://raw.githubusercontent.com/gibsona83/rvumilv/main/Diagnostic_Radiology_wRVUs_PY2025.csv'

try:
    data = load_data(url)
    st.success('Data loaded successfully')

    st.markdown("---")
    st.markdown("## Search for Diagnostic Radiology wRVUs")
    search_col = st.selectbox('Select column to search', ['CPT', 'DESCRIPTION'])
    search_term = st.text_input('Enter search term')

    if search_term:
        filtered_data = data[data[search_col].astype(str).str.contains(search_term, case=False, na=False)]
        st.write(f'### Results for search term "{search_term}" in column "{search_col}"')
        st.dataframe(filtered_data)
        st.write(f'Total results: {len(filtered_data)}')
    else:
        st.write('Enter a search term to filter the data')

    st.markdown("---")
    st.markdown("### Data Preview")
    st.dataframe(data.head())

    st.markdown("---")
    st.markdown("## Download Filtered Data")
    if st.button('Download as CSV'):
        csv = filtered_data.to_csv(index=False)
        st.download_button('Download CSV', csv, 'filtered_data.csv')
except Exception as e:
    st.error(f'Error loading data: {e}')
