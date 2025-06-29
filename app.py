import streamlit as st
from github_api import get_repo_metadata, get_issues

st.title("GitHub Repo Analyzer")

repo_input: str = st.text_input("Enter repository (owner/repo)", "facebook/react")

with st.sidebar:
    st.header("Filters")
    show_issues = st.checkbox("Show good first issues", value=True)
    max_issues = st.slider("Max issues to show", 1, 10, 5)

if st.button("Analyze"):
    if not repo_input or "/" not in repo_input.strip() or len(repo_input.strip().split("/")) != 2:
        st.error("Please enter a valid repository name in format 'owner/repo' (e.g., 'facebook/react')")
    else:
        with st.spinner("Fetching data..."):
            try:
                metadata = get_repo_metadata(repo_input)
                
                if metadata:
                    st.success(f"Found {metadata['name']}")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("⭐ Stars", metadata['stars'])
                    col2.metric("🍴 Forks", metadata['forks'])
                    col3.metric("💻 Language", metadata['language'] or "Unknown")
                    
                    st.subheader("Repository Description")
                    st.write(metadata['description'] or "No description available")

                    if show_issues:
                        issues = get_issues(repo_input, "good first issue")
                        if issues:
                            st.subheader(f"Good First Issues ({len(issues)})")
                            for issue in issues[:max_issues]:
                                st.write(f"- [{issue['title']}]({issue['html_url']})")
                        else:
                            st.info("No good first issues found for this repository")
                else:
                    st.error("Repository not found or access denied")
            except ValueError as e:
                st.error(f"Invalid repository format: {str(e)}")
            except Exception as e:
                st.error(f"Error analyzing repository: {str(e)}")