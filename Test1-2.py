import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
file_path = "university_student_dashboard_data.csv"
data = pd.read_csv(file_path)

# Sidebar filters
years = data['Year'].unique()
selected_year = st.sidebar.multiselect('Select Year', years, default=years)

# Filter data based on selection
filtered_data = data[data['Year'].isin(selected_year)]

# Ensure we are using only Spring term values (since Spring and Fall are the same for each year)
filtered_data_spring = filtered_data[filtered_data['Term'] == 'Spring']

# KPIs based on Spring term for each year
total_apps = filtered_data_spring['Applications'].sum()
total_admitted = filtered_data_spring['Admitted'].sum()
total_enrolled = filtered_data_spring['Enrolled'].sum()
avg_retention = filtered_data_spring['Retention Rate (%)'].mean()
avg_satisfaction = filtered_data_spring['Student Satisfaction (%)'].mean()

# Display KPIs
st.title("University Dashboard Academic Years 2015-2024")
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

# Filter data to show either Spring or Fall term only for each year
selected_term = st.sidebar.selectbox('Select Term', ['Spring', 'Fall'])

# Filter the data based on the selected term
filtered_data_term = filtered_data[filtered_data['Term'] == selected_term]

# Enrollment breakdown by department (one term per year)
dept_columns = ['Engineering Enrolled', 'Business Enrolled', 'Arts Enrolled', 'Science Enrolled']

# Ensure only one term per year, since the enrollment is the same for both terms
dept_df = filtered_data_term[['Year', 'Term'] + dept_columns].melt(id_vars=['Year', 'Term'], 
                                                                   var_name='Department', value_name='Enrolled')

fig3 = px.bar(dept_df, x='Year', y='Enrolled', color='Department', 
              title=f'Enrollment Breakdown by Department ({selected_term} Term)', barmode='stack')
st.plotly_chart(fig3)

# Department trends comparison
fig5 = px.line(dept_df, x='Year', y='Enrolled', color='Department',
               title='Department Enrollment Trends Over Time')
st.plotly_chart(fig5)

# Spring vs. Fall term trends comparison
fig4 = px.bar(filtered_data, x='Year', y='Enrolled', color='Term', barmode='group',
              title='Spring vs. Fall Enrollment Trends')
st.plotly_chart(fig4)

