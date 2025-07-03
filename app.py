import streamlit as st
import pandas as pd
from github_api import analyze_repository
from time_utils import format_time, to_date_time, TIME_FILTERS

st.set_page_config(page_title="the Good First Issue Finder", layout="wide")

st.markdown("# 🔍 the Good First Issue Finder")
st.divider()

# --- Sidebar Input ---
with st.sidebar:
    st.header("⚙️ Repo Settings")
    repo_input: str = st.text_input(
        "Enter GitHub Repo",
        "facebook/react",
        help="Format: owner/repo (e.g. facebook/react)"
    )
    
    st.markdown("### Time Filter")
    date_filter_option = st.selectbox(
        "Show issues updated within the last...",
        options=TIME_FILTERS,
        index=0
    )
    updated_after = to_date_time(date_filter_option)
    if st.button("Analyze"):
        st.session_state['analyze'] = True

# --- Analyze ---
if st.session_state.get('analyze'):
    try:
        with st.spinner("Fetching data from Github..."):
            analysis = analyze_repository(repo_input, updated_after)
        
        if "error" in analysis:
            st.warning(analysis["error"])
            st.stop()
            
        metadata = analysis["metadata"]
        good_first_issues_df = analysis["good_first_issues_df"]
        good_first_count = analysis["good_first_count"]
        secs_since_update = analysis["secs_since_update"]
        status = analysis["status"]
        
        st.markdown(f"**🔗 [{metadata['Full Name']}](https://github.com/{repo_input})**")
        with st.container():
            badge_cols = st.columns(4)
            badge_cols[0].badge("README.md", icon=status["readme"]["icon"], color=status["readme"]["color"])
            badge_cols[1].badge("CONTRIBUTING.md", icon=status["contributing"]["icon"], color=status["contributing"]["color"])
            badge_cols[2].badge(f"Last updated: {format_time(secs_since_update)} ago", icon=status["update"]["icon"], color=status["update"]["color"])
            badge_cols[3].badge(f"{good_first_count} good first issue", icon=status["good_first"]["icon"], color=status["good_first"]["color"])
        
        tab1, tab2 = st.tabs(["Issues", "Repository Info"])
        with tab1:
            if good_first_count == 0:
                st.write(f"⚠️ This repository doesn't have any good first issue within the last {date_filter_option}")
            else:
                st.dataframe(good_first_issues_df)
        with tab2:
            col1, col2, col3= st.columns(3)
            col1.metric("👩‍💻 Language", metadata['Primary Language'])
            col2.metric("⭐ Stars", metadata['Stars'])
            col3.metric("🍴 Forks", metadata['Forks'])
    except ValueError as e:
        st.error(f"Invalid repository format: {e}")
    except Exception as e:
        st.error(f"Error fetching repository data: {e}")