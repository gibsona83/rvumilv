import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(
    page_title='RVU Database',
    layout='centered',
    page_icon='⚕️'
)

@st.cache_data(ttl=3600)
def load_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = pd.read_csv(
            StringIO(response.content.decode('utf-8')),
            dtype={'CPT': str, 'DESCRIPTION': str}
        )
        return data.drop(columns=['MOD'], errors='ignore')
    except Exception as e:
        st.error(f'Error loading data: {str(e)}')
        st.stop()

# Header with logo and title
st.markdown("""
    <style>
        .header-container { text-align: center; }
        .header-title { font-size: 2rem; margin: 0; }
        .header-subtitle { font-size: 1.2rem; margin: 0; color: #555; }
        .search-bar { width: 80%; margin: auto; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='header-container'>", unsafe_allow_html=True)
st.image(
    'https://raw.githubusercontent.com/gibsona83/rvumilv/main/milv.png',
    width=150
)
st.markdown("<h1 class='header-title'>Medical Imaging of Lehigh Valley</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='header-subtitle'>Diagnostic Radiology wRVUs Database</h3>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Load data
DATA_URL = 'https://raw.githubusercontent.com/gibsona83/rvumilv/main/Diagnostic_Radiology_wRVUs_PY2025.csv'
data = load_data(DATA_URL)

# Search bar
st.markdown("<div class='search-bar'>", unsafe_allow_html=True)
search_term = st.text_input(
    '🔍 Search by CPT code or description:',
    help='Example: 732 or MRI',
    placeholder='Type here...'
)
st.markdown("</div>", unsafe_allow_html=True)

# Search results
if search_term:
    mask = (
        data['CPT'].str.contains(search_term, case=False, regex=False) |
        data['DESCRIPTION'].str.contains(search_term, case=False, regex=False)
    )
    filtered_data = data[mask]
    st.markdown(f'**Results: {len(filtered_data)} entries**')
    st.dataframe(
        filtered_data,
        use_container_width=True,
        height=300
    )
    st.download_button(
        '📥 Download Results',
        filtered_data.to_csv(index=False),
        file_name='rvu_results.csv'
    )
else:
    st.markdown("Enter a search term to filter the data.")

# Full dataset preview
with st.expander("⚠️ Show Full Dataset (Large Dataset)"):
    st.dataframe(
        data,
        use_container_width=True,
        height=300
    )
