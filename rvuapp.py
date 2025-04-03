import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Configure page settings
st.set_page_config(
    page_title='Searchable RVU Database',
    layout='wide',
    page_icon='⚕️'  # Added medical emoji as page icon
)

@st.cache_data(ttl=3600)  # Cache data for 1 hour
def load_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = pd.read_csv(
            StringIO(response.content.decode('utf-8')),
            dtype={'CPT': str, 'DESCRIPTION': str}  # Specify column types
        )
        return data.drop(columns=['MOD'], errors='ignore')
    except requests.exceptions.RequestException as e:
        st.error(f'Network error: {str(e)}')
        st.stop()
    except Exception as e:
        st.error(f'Data processing error: {str(e)}')
        st.stop()

# Centered header with styled components
header_col1, header_col2, header_col3 = st.columns([1, 3, 1])
with header_col2:
    st.image(
        'https://raw.githubusercontent.com/gibsona83/rvumilv/main/milv.png',
        width=250
    )
    st.markdown(
        "<h1 style='text-align: center; margin-bottom: 0;'>Medical Imaging of Lehigh Valley, P.C.</h1>"
        "<h2 style='text-align: center; margin-top: 0;'>Searchable Diagnostic Radiology wRVUs Database</h2>",
        unsafe_allow_html=True
    )

# Load data with error handling
DATA_URL = 'https://raw.githubusercontent.com/gibsona83/rvumilv/main/Diagnostic_Radiology_wRVUs_PY2025.csv'
data = load_data(DATA_URL)
st.success('📊 Data loaded successfully!')

# Search interface
with st.expander("🔍 Search for Diagnostic Radiology wRVUs", expanded=True):
    search_term = st.text_input(
        'Enter CPT code or description:',
        help='Search supports partial matches (e.g., "732" or "MRI")'
    )

# Search functionality
if search_term:
    # Create filtered dataset
    mask = (
        data['CPT'].str.contains(search_term, case=False, regex=False) |
        data['DESCRIPTION'].str.contains(search_term, case=False, regex=False)
    )
    filtered_data = data[mask]
    
    # Display results
    st.subheader(f'Results for "{search_term}"')
    st.dataframe(
        filtered_data,
        use_container_width=True,
        height=400,
        column_config={
            "CPT": "CPT Code",
            "DESCRIPTION": "Procedure Description",
            "wRVU": st.column_config.NumberColumn("wRVU", format="%.2f ⚕")
        }
    )
    
    # Results summary and download
    st.metric("Total Results", len(filtered_data))
    st.download_button(
        label='📥 Download Filtered Results',
        data=filtered_data.to_csv(index=False),
        file_name='filtered_rvu_data.csv',
        mime='text/csv',
        use_container_width=True
    )

# Data preview section
with st.expander("📋 Full Dataset Preview", expanded=True):
    st.dataframe(
        data,
        use_container_width=True,
        height=400,
        hide_index=True,
        column_config={
            "CPT": "CPT Code",
            "DESCRIPTION": "Procedure Description",
            "wRVU": st.column_config.NumberColumn("wRVU", format="%.2f ⚕")
        }
    )

# Add footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by Streamlit ⚡ | Medical Coding Reference System"
    "</div>",
    unsafe_allow_html=True
)