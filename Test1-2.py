import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
file_path = "university_student_dashboard_data.csv"
data = pd.read_csv(file_path)

# Sidebar filters
years = data['Year'].unique()
selected_year = st.sidebar.multiselect('Select Year', years, default=years)

# Filter data based on selection
filtered_data = data[data['Year'].isin(selected_year)]

# KPIs
total_apps = filtered_data['Applications'].sum()
total_admitted = filtered_data['Admitted'].sum()
total_enrolled = filtered_data['Enrolled'].sum()
avg_retention = filtered_data['Retention Rate (%)'].mean()
avg_satisfaction = filtered_data['Student Satisfaction (%)'].mean()

# Display KPIs
st.title("University Dashboard")
st.metric("Total Applications", total_apps)
st.metric("Total Admitted", total_admitted)
st.metric("Total Enrolled", total_enrolled)
st.metric("Avg. Retention Rate", f"{avg_retention:.2f}%")
st.metric("Avg. Satisfaction Score", f"{avg_satisfaction:.2f}%")

# Visualizations
# Applications, Admissions, Enrollments over time
fig1 = px.line(filtered_data, x='Year', y=['Applications', 'Admitted', 'Enrolled'],
               labels={'value': 'Count', 'variable': 'Metric'},
               title='Applications, Admissions, and Enrollments Over Time')
st.plotly_chart(fig1)

# Retention Rate and Satisfaction over time
fig2 = px.line(filtered_data, x='Year', y=['Retention Rate (%)', 'Student Satisfaction (%)'],
               labels={'value': 'Percentage', 'variable': 'Metric'},
               title='Retention Rate and Satisfaction Trends')
st.plotly_chart(fig2)

# Enrollment breakdown by department
dept_columns = ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']

dept_df = filtered_data[['Year'] + dept_columns].melt(id_vars=['Year'], 
                                                       var_name='Department', value_name='Enrolled')
fig3 = px.bar(dept_df, x='Year', y='Enrolled', color='Department', 
              title='Enrollment Breakdown by Department')
st.plotly_chart(fig3)

# Spring vs. Fall term trends comparison
fig4 = px.bar(filtered_data, x='Year', y='Enrolled', color='Term', barmode='group',
              title='Spring vs. Fall Enrollment Trends')
st.plotly_chart(fig4)

# Department trends comparison
fig5 = px.line(dept_df, x='Year', y='Enrolled', color='Department',
               title='Department Enrollment Trends Over Time')
st.plotly_chart(fig5)
