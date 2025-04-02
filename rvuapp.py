import streamlit as st
import pandas as pd

st.set_page_config(page_title='Searchable RVU Database', layout='wide')

@st.cache_data
def load_data(file_path):
    data = pd.read_excel(file_path, sheet_name='wRVU')
    data = data.drop(columns=['MOD'], errors='ignore')
    return data

st.title('Searchable Diagnostic Radiology wRVUs Database')

try:
    data = load_data('/mnt/data/Diagnostic_Radiology_wRVUs_PY2025.xlsx')
    st.success('Data loaded successfully')
except Exception as e:
    st.error(f'Error loading data: {e}')
    st.stop()

st.write('### Data Preview')
st.dataframe(data.head())

search_col = st.selectbox('Select column to search', ['CPT', 'DESCRIPTION', 'wRVU'])
search_term = st.text_input('Enter search term')

if search_term:
    filtered_data = data[data[search_col].astype(str).str.contains(search_term, case=False, na=False)]
    st.write(f'### Results for search term "{search_term}" in column "{search_col}"')
    st.dataframe(filtered_data)
    st.write(f'Total results: {len(filtered_data)}')
else:
    st.write('Enter a search term to filter the data')

st.write('### Download Filtered Data')
if st.button('Download as CSV'):
    csv = filtered_data.to_csv(index=False)
    st.download_button('Download CSV', csv, 'filtered_data.csv')
