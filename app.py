"""
Screen Time Management System - Streamlit Web Application
A beautiful and interactive web app to track and analyze screen time usage.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import database as db
from config import APP_TITLE, THRESHOLD_HOURS

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'db_initialized' not in st.session_state:
        st.session_state.db_initialized = False
    if 'page' not in st.session_state:
        st.session_state.page = 'Dashboard'


def show_dashboard():
    """Display the dashboard with statistics and visualizations."""
    st.markdown('<div class="main-header">📊 Dashboard</div>', unsafe_allow_html=True)
    
    try:
        # Get statistics
        stats = db.get_statistics()
        
        # Display key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Screen Time", f"{stats['total_hours']:.1f} hrs", 
                     help="Total hours tracked across all entries")
        
        with col2:
            st.metric("Total Entries", stats['total_entries'],
                     help="Number of screen time records")
        
        with col3:
            st.metric("Avg Daily Usage", f"{stats['avg_daily_hours']:.1f} hrs",
                     delta=f"{stats['avg_daily_hours'] - THRESHOLD_HOURS:.1f} hrs" if stats['avg_daily_hours'] > 0 else None,
                     delta_color="inverse",
                     help=f"Threshold: {THRESHOLD_HOURS} hrs/day")
        
        with col4:
            if stats['first_date'] and stats['last_date']:
                days_tracked = (stats['last_date'] - stats['first_date']).days + 1
                st.metric("Days Tracked", days_tracked,
                         help="Number of days with recorded data")
        
        st.divider()
        
        # Get data for visualizations
        daily_totals = db.get_daily_totals()
        category_totals = db.get_category_totals()
        
        if not daily_totals.empty:
            # Create two columns for charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Daily Screen Time Trend")
                
                # Add threshold line to daily chart
                fig_daily = px.line(daily_totals, x='entry_date', y='total_hours',
                                   title='',
                                   labels={'entry_date': 'Date', 'total_hours': 'Hours'},
                                   markers=True)
                
                # Add threshold line
                fig_daily.add_hline(y=THRESHOLD_HOURS, line_dash="dash", 
                                   line_color="red", 
                                   annotation_text=f"Threshold ({THRESHOLD_HOURS}h)")
                
                fig_daily.update_traces(line_color='#667eea', line_width=3)
                fig_daily.update_layout(height=400)
                st.plotly_chart(fig_daily, use_container_width=True)
                
                # Show days exceeding threshold
                high_usage_days = daily_totals[daily_totals['total_hours'] > THRESHOLD_HOURS]
                if not high_usage_days.empty:
                    st.warning(f"⚠️ **{len(high_usage_days)} day(s)** exceeded the {THRESHOLD_HOURS}h threshold!")
            
            with col2:
                st.subheader("🎯 Usage by Category")
                
                if not category_totals.empty:
                    fig_category = px.pie(category_totals, values='total_hours', names='category',
                                         title='',
                                         color_discrete_sequence=px.colors.qualitative.Set3)
                    fig_category.update_traces(textposition='inside', textinfo='percent+label')
                    fig_category.update_layout(height=400)
                    st.plotly_chart(fig_category, use_container_width=True)
            
            st.divider()
            
            # Category breakdown bar chart
            st.subheader("📊 Category Breakdown")
            if not category_totals.empty:
                fig_bar = px.bar(category_totals, x='category', y='total_hours',
                               title='',
                               labels={'category': 'Category', 'total_hours': 'Total Hours'},
                               color='total_hours',
                               color_continuous_scale='Blues')
                fig_bar.update_layout(height=350, showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("📝 No data available yet. Add some entries to see visualizations!")
            
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")


def show_add_entry():
    """Display the form to add a new entry."""
    st.markdown('<div class="main-header">➕ Add Screen Time Entry</div>', unsafe_allow_html=True)
    
    with st.form("add_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            entry_date = st.date_input(
                "Date",
                value=date.today(),
                max_value=date.today(),
                help="Select the date for this entry"
            )
            
            category = st.selectbox(
                "Category",
                options=["Study", "Work", "Social Media", "Entertainment", 
                        "Gaming", "Reading", "Exercise", "Other"],
                help="Select the activity category"
            )
        
        with col2:
            hours_spent = st.number_input(
                "Hours Spent",
                min_value=0.0,
                max_value=24.0,
                value=1.0,
                step=0.5,
                help="Enter hours (e.g., 2.5 for 2 hours 30 minutes)"
            )
            
            remarks = st.text_area(
                "Remarks (Optional)",
                placeholder="Add any notes about this activity...",
                help="Optional notes or comments"
            )
        
        submitted = st.form_submit_button("Add Entry", use_container_width=True, type="primary")
        
        if submitted:
            if hours_spent <= 0:
                st.error("Please enter a valid number of hours (greater than 0).")
            else:
                success, message = db.add_entry(entry_date, category, hours_spent, remarks)
                if success:
                    st.success(f"✅ {message}")
                    st.balloons()
                else:
                    st.error(f"❌ {message}")


def show_view_records():
    """Display all recorded entries in a table."""
    st.markdown('<div class="main-header">📋 View Records</div>', unsafe_allow_html=True)
    
    try:
        # Date range filter
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            start_date = st.date_input("From Date", value=date.today() - timedelta(days=30))
        
        with col2:
            end_date = st.date_input("To Date", value=date.today())
        
        with col3:
            show_all = st.checkbox("Show All", value=False)
        
        # Fetch data
        if show_all:
            df = db.get_all_entries()
        else:
            df = db.get_date_range_entries(start_date, end_date)
        
        if not df.empty:
            st.info(f"📊 Showing **{len(df)}** record(s)")
            
            # Format the dataframe
            df['entry_date'] = pd.to_datetime(df['entry_date']).dt.strftime('%Y-%m-%d')
            df['hours_spent'] = df['hours_spent'].round(2)
            
            # Rename columns for display
            display_df = df.rename(columns={
                'entry_id': 'ID',
                'entry_date': 'Date',
                'category': 'Category',
                'hours_spent': 'Hours',
                'remarks': 'Remarks'
            })
            
            # Display the table
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Hours": st.column_config.NumberColumn(
                        "Hours",
                        format="%.2f",
                    ),
                }
            )
            
            # Delete entry option
            st.divider()
            st.subheader("🗑️ Delete Entry")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                entry_id_to_delete = st.number_input(
                    "Enter Entry ID to delete",
                    min_value=1,
                    step=1,
                    help="Enter the ID of the entry you want to delete"
                )
            with col2:
                st.write("")  # Spacer
                st.write("")  # Spacer
                if st.button("Delete", type="secondary"):
                    success, message = db.delete_entry(entry_id_to_delete)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        else:
            st.warning("📭 No records found for the selected date range.")
            
    except Exception as e:
        st.error(f"Error loading records: {e}")


def show_analysis():
    """Display detailed analysis and insights."""
    st.markdown('<div class="main-header">🔍 Analysis & Insights</div>', unsafe_allow_html=True)
    
    try:
        daily_totals = db.get_daily_totals()
        category_totals = db.get_category_totals()
        
        if not daily_totals.empty:
            # Summary statistics
            st.subheader("📈 Summary Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                max_day = daily_totals.loc[daily_totals['total_hours'].idxmax()]
                st.metric(
                    "Highest Usage Day",
                    f"{max_day['total_hours']:.1f} hrs",
                    delta=f"{max_day['entry_date'].strftime('%Y-%m-%d')}"
                )
            
            with col2:
                min_day = daily_totals.loc[daily_totals['total_hours'].idxmin()]
                st.metric(
                    "Lowest Usage Day",
                    f"{min_day['total_hours']:.1f} hrs",
                    delta=f"{min_day['entry_date'].strftime('%Y-%m-%d')}"
                )
            
            with col3:
                avg_hours = daily_totals['total_hours'].mean()
                st.metric(
                    "Average Daily",
                    f"{avg_hours:.1f} hrs",
                    delta=f"{avg_hours - THRESHOLD_HOURS:+.1f} from threshold"
                )
            
            st.divider()
            
            # Category insights
            st.subheader("🎯 Category Insights")
            
            if not category_totals.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Top Categories by Time**")
                    for idx, row in category_totals.head(5).iterrows():
                        percentage = (row['total_hours'] / category_totals['total_hours'].sum()) * 100
                        st.progress(percentage / 100)
                        st.caption(f"{row['category']}: {row['total_hours']:.1f} hrs ({percentage:.1f}%)")
                
                with col2:
                    # Weekly pattern (if enough data)
                    if len(daily_totals) >= 7:
                        st.markdown("**Weekly Pattern**")
                        daily_totals['day_of_week'] = pd.to_datetime(daily_totals['entry_date']).dt.day_name()
                        weekly = daily_totals.groupby('day_of_week')['total_hours'].mean().reindex(
                            ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                        )
                        
                        fig_weekly = px.bar(
                            x=weekly.index,
                            y=weekly.values,
                            labels={'x': 'Day', 'y': 'Avg Hours'},
                            color=weekly.values,
                            color_continuous_scale='Viridis'
                        )
                        fig_weekly.update_layout(height=300, showlegend=False)
                        st.plotly_chart(fig_weekly, use_container_width=True)
            
            st.divider()
            
            # Recommendations
            st.subheader("💡 Recommendations")
            
            avg_daily = daily_totals['total_hours'].mean()
            high_days = len(daily_totals[daily_totals['total_hours'] > THRESHOLD_HOURS])
            
            if avg_daily > THRESHOLD_HOURS:
                st.warning(f"⚠️ Your average daily screen time ({avg_daily:.1f} hrs) exceeds the recommended threshold of {THRESHOLD_HOURS} hours.")
                st.info("💡 **Tip:** Try to reduce screen time by taking regular breaks and engaging in offline activities.")
            else:
                st.success(f"✅ Great job! Your average daily screen time ({avg_daily:.1f} hrs) is within healthy limits.")
            
            if high_days > 0:
                st.warning(f"📊 You exceeded the threshold on {high_days} day(s). Consider setting daily limits.")
            
            # Top category recommendation
            if not category_totals.empty:
                top_category = category_totals.iloc[0]
                top_percentage = (top_category['total_hours'] / category_totals['total_hours'].sum()) * 100
                
                if top_percentage > 50:
                    st.info(f"📱 **{top_category['category']}** accounts for {top_percentage:.1f}% of your screen time. Consider diversifying your activities.")
        else:
            st.info("📝 No data available for analysis. Start adding entries to see insights!")
            
    except Exception as e:
        st.error(f"Error generating analysis: {e}")


def show_settings():
    """Display settings and database management."""
    st.markdown('<div class="main-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    st.subheader("🗄️ Database Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Initialize Database", use_container_width=True):
            success, message = db.initialize_database()
            if success:
                st.success(message)
                st.session_state.db_initialized = True
            else:
                st.error(message)
    
    with col2:
        if st.button("📊 Insert Sample Data", use_container_width=True):
            success, message = db.insert_sample_data()
            if success:
                st.success(message)
                st.balloons()
            else:
                st.error(message)
    
    st.divider()
    
    st.subheader("📝 About")
    st.info(f"""
    **{APP_TITLE}**
    
    A comprehensive web application to track and analyze your daily screen time usage.
    
    **Features:**
    - 📊 Interactive dashboard with visualizations
    - ➕ Easy data entry with form validation
    - 📋 View and filter records
    - 🔍 Detailed analysis and insights
    - 💡 Smart recommendations
    
    **Threshold:** {THRESHOLD_HOURS} hours/day
    
    Built with Streamlit, MySQL, and Plotly.
    """)


def main():
    """Main application function."""
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Add Entry", "View Records", "Analysis", "Settings"],
        label_visibility="collapsed"
    )
    
    st.sidebar.divider()
    
    # Quick stats in sidebar
    try:
        stats = db.get_statistics()
        st.sidebar.metric("Total Hours Tracked", f"{stats['total_hours']:.1f}")
        st.sidebar.metric("Total Entries", stats['total_entries'])
        
        if stats['avg_daily_hours'] > THRESHOLD_HOURS:
            st.sidebar.warning(f"⚠️ Avg: {stats['avg_daily_hours']:.1f}h/day")
        else:
            st.sidebar.success(f"✅ Avg: {stats['avg_daily_hours']:.1f}h/day")
    except:
        st.sidebar.info("Initialize database to start tracking!")
    
    st.sidebar.divider()
    st.sidebar.caption("Screen Time Management © 2025")
    
    # Display selected page
    if page == "Dashboard":
        show_dashboard()
    elif page == "Add Entry":
        show_add_entry()
    elif page == "View Records":
        show_view_records()
    elif page == "Analysis":
        show_analysis()
    elif page == "Settings":
        show_settings()


if __name__ == "__main__":
    main()
