import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Configure page settings for compact layout
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

# Compact header layout
col1, col2 = st.columns([1, 3])
with col1:
    st.image(
        'https://raw.githubusercontent.com/gibsona83/rvumilv/main/milv.png',
        width=150
    )
with col2:
    st.markdown("""
        <h1 style='margin-bottom:0;'>Medical Imaging of Lehigh Valley</h1>
        <h3 style='margin-top:0;'>Diagnostic Radiology wRVUs Database</h3>
    """, unsafe_allow_html=True)

# Load data without success message
DATA_URL = 'https://raw.githubusercontent.com/gibsona83/rvumilv/main/Diagnostic_Radiology_wRVUs_PY2025.csv'
data = load_data(DATA_URL)

# Compact search interface
st.markdown("---")
search_term = st.text_input(
    '🔍 Search by CPT code or description:',
    help='Example: 732 or MRI'
)

# Search results section
if search_term:
    mask = (
        data['CPT'].str.contains(search_term, case=False, regex=False) |
        data['DESCRIPTION'].str.contains(search_term, case=False, regex=False)
    )
    filtered_data = data[mask]
    
    if not filtered_data.empty:
        # Compact results display
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.subheader(f'Results: {len(filtered_data)} entries')
        with col_b:
            st.download_button(
                '📥 Download',
                filtered_data.to_csv(index=False),
                file_name='rvu_results.csv',
                use_container_width=True
            )
        
        st.dataframe(
            filtered_data,
            use_container_width=True,
            height=300,
            column_config={
                "CPT": "CPT Code",
                "DESCRIPTION": "Description",
                "wRVU": st.column_config.NumberColumn("wRVU", format="%.2f")
            }
        )
    else:
        st.warning('No matching entries found')

# Collapsible full data preview
with st.expander("⚠️ Show Full Dataset (Caution: Large Dataset)"):
    st.dataframe(
        data,
        use_container_width=True,
        height=300,
        hide_index=True,
        column_config={
            "CPT": "CPT Code",
            "DESCRIPTION": "Description",
            "wRVU": st.column_config.NumberColumn("wRVU", format="%.2f")
        }
    )

# Minimal footer
st.markdown("""
    <div style='text-align: center; color: #666; font-size:0.8em; margin-top:1rem;'>
    LV Radiology Reference System • Powered by Streamlit
    </div>
""", unsafe_allow_html=True)