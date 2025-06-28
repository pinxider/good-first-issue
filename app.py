import streamlit as st
from github_api import get_repo_metadata, get_issues

st.title("GitHub Repo Analyzer")

repo_input = st.text_input("Enter repository (owner/repo)", "facebook/react")

if st.button("Analyze"):
    with st.spinner("Fetching data..."):
        metadata = get_repo_metadata(repo_input)
        
        if metadata:
            st.success(f"Found {metadata['name']}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Stars", metadata['stars'])
            col2.metric("Language", metadata['language'])
            
            st.subheader("Repository Description")
            st.write(metadata['description'])

            issues = get_issues(repo_input, "good first issue")
            if issues:
                st.subheader(f"Good First Issues ({len(issues)})")
                for issue in issues[:5]:  # Show first 5
                    st.write(f"- {issue['title']}")
        else:
            st.error("No matching repo found.")