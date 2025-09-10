import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import json

# OMDB API configuration
OMDB_API_KEY = "9c62f8c2"
OMDB_BASE_URL = "http://www.omdbapi.com/"

# Initialize session state
def init_session_state():
    if 'tracked_movies' not in st.session_state:
        st.session_state.tracked_movies = []
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'current_movie' not in st.session_state:
        st.session_state.current_movie = None

# Set page config
st.set_page_config(page_title="Movie Revenue Tracker", layout="wide")

# Initialize session state
init_session_state()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "🔍 Search Movies", "📊 Tracking Dashboard", "⚙️ Settings"])

def fetch_movie_data(movie_title):
    """Fetch movie data from OMDB API"""
    params = {
        'apikey': OMDB_API_KEY,
        't': movie_title,
        'type': 'movie'
    }
    
    response = requests.get(OMDB_BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            return {
                'Title': data.get('Title', ''),
                'Year': data.get('Year', ''),
                'BoxOffice': data.get('BoxOffice', 'N/A'),
                'Genre': data.get('Genre', ''),
                'Language': data.get('Language', ''),
                'Country': data.get('Country', '')
            }
    return None

# Main Content based on navigation
if page == "🏠 Home":
    st.title("Movie Revenue Tracker")
    st.write("## 🎬 Welcome to Movie Revenue Tracker!")
    st.write("### How to use:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### 1. Search for Movies")
        st.write("- Use the Search Movies page")
        st.write("- Enter a movie title (e.g., 'Avatar', 'Inception')")
        st.write("- View detailed analytics")
        
    with col2:
        st.write("#### 2. Track and Analyze")
        st.write("- Add movies to tracking list")
        st.write("- Compare multiple movies")
        st.write("- Export your analysis")
        
    # Show quick stats if there are tracked movies
    if st.session_state.tracked_movies:
        st.write("### 📈 Quick Stats")
        quick_stats_col1, quick_stats_col2, quick_stats_col3 = st.columns(3)
        tracked_df = pd.DataFrame(st.session_state.tracked_movies)
        
        with quick_stats_col1:
            st.metric("Movies Tracked", len(tracked_df))
        with quick_stats_col2:
            st.metric("Total Revenue", f"${tracked_df['Revenue'].sum():,.2f}")
        with quick_stats_col3:
            st.metric("Genres Covered", len(tracked_df['Genre'].unique()))

elif page == "🔍 Search Movies":
    st.title("Search Movies")
    
    # Search section
    with st.container():
        movie_title = st.text_input("Enter movie title", key="movie_search")
        if st.button("🔍 Search Movie", key="search_button"):
            if movie_title:
                st.session_state.search_results = fetch_movie_data(movie_title)
                if st.session_state.search_results is None:
                    st.error("Movie not found or API error occurred")
            else:
                st.warning("Please enter a movie title")
    
    # Display search results
    if st.session_state.search_results:
        movie_data = st.session_state.search_results
        st.write("### Movie Details")
        
        # Create three columns for better layout
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.write("**Title:**", movie_data['Title'])
            st.write("**Year:**", movie_data['Year'])
            st.write("**Box Office:**", movie_data['BoxOffice'])
        
        with col2:
            st.write("**Genre:**", movie_data['Genre'])
            st.write("**Language:**", movie_data['Language'])
            st.write("**Country:**", movie_data['Country'])
        
        # Convert box office to number for analytics
        box_office = movie_data['BoxOffice']
        revenue = 0
        if box_office != 'N/A':
            revenue = float(box_office.replace('$', '').replace(',', ''))
            
        # Display analytics in the third column
        with col3:
            st.write("**Analytics Summary:**")
            if revenue > 0:
                st.write(f"💰 Revenue: ${revenue:,.2f}")
                if revenue > 100000000:
                    st.write("🌟 Blockbuster Status: Hit")
                elif revenue > 50000000:
                    st.write("⭐ Blockbuster Status: Moderate Success")
                else:
                    st.write("📊 Blockbuster Status: Limited Release")
            else:
                st.write("📊 Revenue data not available")

        # Show detailed analytics
        st.write("### Movie Analytics")
        
        # Create tabs for different analytics views
        tab1, tab2, tab3 = st.tabs(["Revenue Analysis", "Genre Comparison", "Market Share"])
        
        with tab1:
            if revenue > 0:
                try:
                    # Revenue breakdown visualization
                    plt.figure(figsize=(10, 6))
                    categories = ['Production Budget (Est.)', 'Marketing (Est.)', 'Net Revenue (Est.)']
                    budget_est = revenue * 0.4
                    marketing_est = revenue * 0.2
                    net_revenue = revenue - budget_est - marketing_est
                    values = [budget_est, marketing_est, net_revenue]
                    
                    plt.bar(categories, values, color=['#FF9999', '#66B2FF', '#99FF99'])
                    plt.xticks(rotation=45)
                    plt.title(f"Estimated Revenue Breakdown for {movie_data['Title']}")
                    plt.tight_layout()
                    st.pyplot(plt)
                    plt.close()
                except Exception as e:
                    st.error(f"Error creating revenue breakdown chart: {str(e)}")
                
                # Add metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Revenue", f"${revenue:,.0f}")
                col2.metric("Est. Net Revenue", f"${net_revenue:,.0f}")
                col3.metric("ROI (Est.)", f"{(net_revenue/budget_est)*100:.1f}%")
        
        with tab2:
            # Genre performance visualization
            genres = movie_data['Genre'].split(', ')
            fig, ax = plt.subplots(figsize=(8, 8))
            genre_shares = [100/len(genres)] * len(genres)
            plt.pie(genre_shares, labels=genres, autopct='%1.1f%%')
            plt.title(f"Genre Distribution - {movie_data['Title']}")
            st.pyplot(fig)
            
            # Add genre insights
            st.write("#### Genre Insights")
            for genre in genres:
                st.write(f"- {genre}: Common in {movie_data['Country']} market")
        
        with tab3:
            # Market distribution
            fig, ax = plt.subplots(figsize=(10, 6))
            markets = ['Domestic', 'International']
            market_shares = [0.4, 0.6]
            ax.bar(markets, [revenue * share for share in market_shares], color=['#7FB3D5', '#E59866'])
            plt.title(f"Estimated Market Distribution - {movie_data['Title']}")
            st.pyplot(fig)
            
            # Add market insights
            st.write("#### Market Insights")
            st.write(f"- Primary Release: {movie_data['Country']}")
            st.write(f"- Language: {movie_data['Language']}")

        # Add to tracking list button
        if st.button("➕ Add to Tracking List"):
            if 'tracked_movies' not in st.session_state:
                st.session_state.tracked_movies = []
            
            # Create movie entry for tracking
            movie_entry = {
                'Movie': movie_data['Title'],
                'Year': movie_data['Year'],
                'Revenue': revenue,
                'Genre': movie_data['Genre'].split(', ')[0],
                'Language': movie_data['Language'].split(', ')[0],
                'Region': movie_data['Country'].split(', ')[0]
            }
            
            # Check if movie is already tracked
            if not any(movie['Movie'] == movie_entry['Movie'] for movie in st.session_state.tracked_movies):
                st.session_state.tracked_movies.append(movie_entry)
                st.success(f"Added {movie_data['Title']} to tracking list!")
            else:
                st.warning(f"{movie_data['Title']} is already in your tracking list!")
    # This block was causing the duplicate display, removing it
        
        # Convert box office to number for analytics
        box_office = movie_data['BoxOffice']
        if box_office != 'N/A':
            revenue = float(box_office.replace('$', '').replace(',', ''))
        else:
            revenue = 0
            
        # Display analytics in the third column
        with col3:
            st.write("**Analytics Summary:**")
            if revenue > 0:
                st.write(f"💰 Revenue: ${revenue:,.2f}")
                if revenue > 100000000:
                    st.write("🌟 Blockbuster Status: Hit")
                elif revenue > 50000000:
                    st.write("⭐ Blockbuster Status: Moderate Success")
                else:
                    st.write("📊 Blockbuster Status: Limited Release")
            else:
                st.write("📊 Revenue data not available")

        # Show detailed analytics
        st.write("### Movie Analytics")
        
        # Create tabs for different analytics views
        tab1, tab2, tab3 = st.tabs(["Revenue Analysis", "Genre Comparison", "Market Share"])
        
        with tab1:
            if revenue > 0:
                # Revenue breakdown visualization
                fig, ax = plt.subplots(figsize=(10, 6))
                categories = ['Production Budget (Est.)', 'Marketing (Est.)', 'Net Revenue (Est.)']
                # Estimated values for visualization
                budget_est = revenue * 0.4  # Estimated 40% of revenue
                marketing_est = revenue * 0.2  # Estimated 20% of revenue
                net_revenue = revenue - budget_est - marketing_est
                values = [budget_est, marketing_est, net_revenue]
                
                ax.bar(categories, values, color=['#FF9999', '#66B2FF', '#99FF99'])
                plt.xticks(rotation=45)
                plt.title(f"Estimated Revenue Breakdown for {movie_data['Title']}")
                st.pyplot(fig)
                
                # Add metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Revenue", f"${revenue:,.0f}")
                col2.metric("Est. Net Revenue", f"${net_revenue:,.0f}")
                col3.metric("ROI (Est.)", f"{(net_revenue/budget_est)*100:.1f}%")
        
        with tab2:
            # Genre performance visualization
            genres = movie_data['Genre'].split(', ')
            fig, ax = plt.subplots(figsize=(8, 8))
            genre_shares = [100/len(genres)] * len(genres)  # Equal distribution for visualization
            plt.pie(genre_shares, labels=genres, autopct='%1.1f%%')
            plt.title(f"Genre Distribution - {movie_data['Title']}")
            st.pyplot(fig)
            
            # Add genre insights
            st.write("#### Genre Insights")
            for genre in genres:
                st.write(f"- {genre}: Common in {movie_data['Country']} market")
        
        with tab3:
            # Market distribution
            fig, ax = plt.subplots(figsize=(10, 6))
            markets = ['Domestic', 'International']
            market_shares = [0.4, 0.6]  # Estimated market share
            ax.bar(markets, [revenue * share for share in market_shares], color=['#7FB3D5', '#E59866'])
            plt.title(f"Estimated Market Distribution - {movie_data['Title']}")
            st.pyplot(fig)
            
            # Add market insights
            st.write("#### Market Insights")
            st.write(f"- Primary Release: {movie_data['Country']}")
            st.write(f"- Language: {movie_data['Language']}")
            
        # Show performance metrics
        st.write("### Performance Metrics")
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        with metrics_col1:
            st.metric(
                "Revenue per Market",
                f"${revenue/len(movie_data['Country'].split(', ')):,.0f}"
            )
        with metrics_col2:
            st.metric(
                "Revenue per Genre",
                f"${revenue/len(genres):,.0f}"
            )
        with metrics_col3:
            avg_yearly = revenue / (2025 - int(movie_data['Year'][:4]) + 1)
            st.metric(
                "Avg. Yearly Revenue",
                f"${avg_yearly:,.0f}"
            )
        with metrics_col4:
            st.metric(
                "Days Since Release",
                f"{(datetime.now() - datetime.strptime(movie_data['Year'][:4], '%Y')).days}"
            )
        
        # Add to tracking list
        if st.button("Add to Tracking List"):
            if 'tracked_movies' not in st.session_state:
                st.session_state.tracked_movies = []
            
            # Convert box office string to number
            box_office = movie_data['BoxOffice']
            if box_office != 'N/A':
                box_office = float(box_office.replace('$', '').replace(',', ''))
            else:
                box_office = 0
                
            movie_entry = {
                'Movie': movie_data['Title'],
                'Year': movie_data['Year'],
                'Revenue': box_office,
                'Genre': movie_data['Genre'].split(', ')[0],  # Take first genre
                'Language': movie_data['Language'].split(', ')[0],  # Take first language
                'Region': movie_data['Country'].split(', ')[0]  # Take first country
            }
            st.session_state.tracked_movies.append(movie_entry)
            st.success(f"Added {movie_data['Title']} to tracking list!")
    else:
        st.error("Movie not found or error in fetching data")

elif page == "📊 Tracking Dashboard":
    st.title("Tracking Dashboard")
    
    if st.session_state.tracked_movies:
        tracked_df = pd.DataFrame(st.session_state.tracked_movies)
        
        # Filters in sidebar
        st.sidebar.markdown("### Filters")
        genres = tracked_df['Genre'].unique()
        selected_genres = st.sidebar.multiselect("Select Genres", options=genres, default=list(genres))
        
        regions = tracked_df['Region'].unique()
        selected_regions = st.sidebar.multiselect("Select Regions", options=regions, default=list(regions))
        
        # Filter the dataframe
        filtered_df = tracked_df[
            tracked_df['Genre'].isin(selected_genres) &
            tracked_df['Region'].isin(selected_regions)
        ]
        
        # Dashboard Layout
        # Overview metrics
        st.write("### Overview")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total Movies", len(filtered_df))
        with m2:
            st.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.2f}")
        with m3:
            st.metric("Avg Revenue/Movie", f"${filtered_df['Revenue'].mean():,.2f}")
        with m4:
            st.metric("Unique Genres", len(filtered_df['Genre'].unique()))
            
        # Movie List with Details
        st.write("### Tracked Movies")
        st.dataframe(filtered_df.style.format({
            'Revenue': '${:,.2f}'
        }))
        
        # Visualizations
        st.write("### Analytics")
        viz_tab1, viz_tab2 = st.tabs(["Revenue Analysis", "Genre Distribution"])
        
        with viz_tab1:
            try:
                # Revenue comparison bar chart
                plt.figure(figsize=(12, 6))
                filtered_df.plot(kind='bar', x='Movie', y='Revenue')
                plt.xticks(rotation=45)
                plt.title("Revenue Comparison")
                plt.tight_layout()  # Adjust layout to prevent text cutoff
                st.pyplot(plt)
                plt.close()  # Close the figure
            except Exception as e:
                st.error(f"Error creating revenue chart: {str(e)}")
            
        with viz_tab2:
            try:
                # Genre distribution pie chart
                plt.figure(figsize=(8, 8))
                genre_data = filtered_df.groupby('Genre')['Revenue'].sum()
                plt.pie(genre_data, labels=genre_data.index, autopct='%1.1f%%')
                plt.title("Revenue by Genre")
                plt.tight_layout()  # Adjust layout
                st.pyplot(plt)
                plt.close()  # Close the figure
            except Exception as e:
                st.error(f"Error creating genre chart: {str(e)}")
            
        # Export options
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Export Data")
        if st.sidebar.button("Download CSV"):
            csv = filtered_df.to_csv(index=False)
            st.sidebar.download_button(
                label="📥 Download Data",
                data=csv,
                file_name="movie_tracker_export.csv",
                mime="text/csv"
            )
            
    else:
        st.info("No movies in tracking list. Go to Search Movies to add some!")
    
    # This block was causing duplicate visualizations, removing it
elif page == "⚙️ Settings":
    st.title("Settings")
    
    # Clear data option
    st.write("### Data Management")
    if st.button("Clear All Tracked Movies"):
        st.session_state.tracked_movies = []
        st.success("All tracked movies have been cleared!")
    
    # About section
    st.write("### About")
    st.write("Movie Revenue Tracker v1.0")
    st.write("Data provided by OMDB API")
    
    # Help section
    st.write("### Help")
    st.write("Having issues? Here are some tips:")
    st.write("- Make sure to enter the exact movie title")
    st.write("- Some movies might not have revenue data available")
    st.write("- Try refreshing the page if charts don't load")
    
    # Contact
    st.write("### Contact")
    st.write("For support or feedback, please contact:")
    st.write("� support@movietracker.com")

# Add data download option
if 'tracked_movies' in st.session_state and st.session_state.tracked_movies:
    st.sidebar.markdown("---")
    if st.sidebar.button("Download Tracked Data"):
        csv = tracked_df.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name="movie_revenue_data.csv",
            mime="text/csv"
        )
