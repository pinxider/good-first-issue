import streamlit as st
from github_api import get_repo_metadata, get_issues, get_readme_file, get_contributing_file
from time_utils import format_time, seconds_since_update, SECONDS_IN_30_DAYS, TIME_FILTERS

st.title("🔍 Good First Commit")
st.divider()

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
    

if st.button("Analyze"):
    if not repo_input or "/" not in repo_input.strip() or len(repo_input.strip().split("/")) != 2:
        st.error("Please enter a valid repository name in format 'owner/repo' (e.g., 'facebook/react')")
    else:
        with st.spinner("Fetching data..."):
            try:
                metadata = get_repo_metadata(repo_input)
                
                if metadata:
                    st.markdown(f"**🔗 [{metadata['name']}](https://github.com/{repo_input})**")
                    
                    # Status badges  
                    readme_link = get_readme_file(repo_input)
                    contributing_link = get_contributing_file(repo_input)
                    
                    # Get issues filtered by time
                    from time_utils import to_date_time
                    updated_after = to_date_time(date_filter_option)
                    issues = get_issues(repo_input, "good first issue", updated_after.isoformat())
                    good_first_count = len(issues) if issues else 0
                    
                    # Calculate time since last update
                    secs_since_update = seconds_since_update(metadata['updated_at'])
                    
                    with st.container():
                        badge_cols = st.columns(4)
                        
                        readme_icon, readme_color = ("✅", "green") if readme_link else ("❌", "red") 
                        contrib_icon, contrib_color = ("✅", "green") if contributing_link else ("❌", "red")
                        
                        time_str = format_time(secs_since_update)
                        update_icon, update_color = ("✅", "green") if secs_since_update <= SECONDS_IN_30_DAYS else ("❌", "red")
                        
                        issues_icon, issues_color = ("✅", "green") if good_first_count > 0 else ("❌", "red")
                        
                        badge_cols[0].badge("README.md", icon=readme_icon, color=readme_color)
                        badge_cols[1].badge("CONTRIBUTING.md", icon=contrib_icon, color=contrib_color)
                        badge_cols[2].badge(f"Last updated: {time_str} ago", icon=update_icon, color=update_color)
                        badge_cols[3].badge(f"{good_first_count} good first issues", icon=issues_icon, color=issues_color)
                    
                    tab1, tab2 = st.tabs(["Issues", "Repository Info"])
                    
                    with tab1:
                        if good_first_count == 0:
                            st.write(f"⚠️ This repository doesn't have any good first issues within the last {date_filter_option}")
                        else:
                            # Convert issues to dataframe for display
                            import pandas as pd
                            issues_df = pd.DataFrame([{
                                'title': issue['title'],
                                'url': issue['html_url'],
                                'created_at': issue['created_at'],
                                'updated_at': issue['updated_at'],
                                'comments': issue['comments']
                            } for issue in issues])
                            st.dataframe(issues_df)
                    
                    with tab2:
                        col1, col2, col3 = st.columns(3)
                        col1.metric("👩‍💻 Language", metadata['language'] or "Unknown")
                        col2.metric("⭐ Stars", f"{metadata['stars']:,}")
                        col3.metric("🍴 Forks", f"{metadata['forks']:,}")

                else:
                    st.error("❌ Repository not found or access denied")
            except ValueError as e:
                st.error(f"Invalid repository format: {str(e)}")
            except Exception as e:
                st.error(f"Error analyzing repository: {str(e)}")