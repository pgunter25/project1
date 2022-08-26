#Imports 
from collections import namedtuple
from multiprocessing.dummy import current_process
from tkinter.filedialog import test
import altair as alt
import math
import pandas as pd
import streamlit as st
import pickle 
from pickle import load
from math import log, floor
from pathlib import Path


#Header information 
st.title("UC Berekeley Student Progress Tracker Tool", anchor=None)
st.subheader("Project 1 by Phoebe Gunter")
st.caption("This Bot allows professors of UC Berkeley courses to see which students are falling behind and not actively participating in class", unsafe_allow_html=False)


#Importing Assignments CSV and creating Assignments Dataframe 
data = Path("/Users/phoebegunter/Documents/FinTech-Workspace/Project1/Data/assignments.csv")
assignments_df = pd.read_csv(data, delimiter=",").rename(columns={"Unnamed: 0":"Assignment"})
assignments_df.set_index('Assignment', inplace=True) #sets the index of the Assignment dataframe 
assignments_transposed = assignments_df.T #Transposed Assignments Dataframe so that the student IDs are on the rows 
#Summing the values of the assignments and renaming the headers
col_count = len(assignments_df.columns) #counts the number of student IDs in the class 
assignments_df.loc[col_count,:]= assignments_df.sum(axis=0)
max_assignment_value = assignments_df.loc[col_count,:].max()
avg_assignment_value = assignments_df.loc[col_count,:].mean()
assignments_df.rename({42: "Total"},inplace=True)

#Student IDs Dataframe
student_ids = assignments_transposed.index

#Page Views Dataframe 
data = Path("/Users/phoebegunter/Documents/FinTech-Workspace/Project1/Data/page_views.csv")
page_views_df = pd.read_csv(data, delimiter=",").rename(columns={"Unnamed: 0":"Instance"})
page_views_df.set_index('Instance', inplace=True)
page_views_transposed = page_views_df.T


#Participation Dataframe 
data = Path("/Users/phoebegunter/Documents/FinTech-Workspace/Project1/Data/participations.csv")
participation_df = pd.read_csv(data, delimiter=",").rename(columns={"Unnamed: 0":"Assignment"})
#Set up series for below average participation and calcualte average. 
below_average_participations = pd.Series()
participation_count_series = participation_df["id"].value_counts(dropna=True) 
average_participations = participation_count_series.mean()
average_participations = round(average_participations)



#First Section with Recommendations 
st.header("Student Performance Analytics")
st.write("There are " + str(col_count) +  " students in this class." ) #Tells the professor how many students are in the class based on number of student ids in assignment df 





#SECTION 1 
#First set of 3 columns 
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Significant Portal Events")
    st.write("Student ID's with below average participation in assignments and projects")
    st.info("The average number of assignment submissions is " + str(average_participations) + ".")
    
    for index, value in participation_count_series.items():
        if value < average_participations:
            s1 = pd.Series({index:value})
            below_average_participations = below_average_participations.append(s1)   
    st.write(below_average_participations)


#Column2 
with col2: 
    st.subheader("Missing Assignments") #subheader 
    st.write("Student ID's with more than 2 missing assignments or projects")

    current_class_progress = assignments_df.iloc[:,1].notnull().count() #counts the number of graded assisgnments so far 
    st.info("Assignments graded: " + str(current_class_progress) ) #Tells the professor how far along in the class they are
    st.info("Max assignment value: " + str(round(max_assignment_value))) #displays the max value a student has achieved by summing all of their assignment values  
    st.info("Avg assignment value: " + str(round(avg_assignment_value)))
    

        
    behind_in_class_assignments_value = .8*(current_class_progress * 100) #Calculates the threshold that someone is falling behind 


    missing_assignments_series = pd.Series() #needed to set series outside of for loop 
    more_than_two_missing_assignments = pd.Series() #needed to set series outside of loop

    for i in assignments_df:
        #gets the end of the assignments dataframe to iterate through. 
        end_of_df = len(assignments_df)
        end_of_df = int(end_of_df)-1
       
        #getting the students average grade 
        col_number = assignments_df.columns.get_loc(i)
        student_cumulative_grade = assignments_df.iat[end_of_df, col_number]

        student_id = str(i)
        #st.write(student_cumulative_grade)

        #Counts the number of times a student has recieved a 0 grade 
        count = int((assignments_df[i] == 0).sum())
        
        s1 = pd.Series([count], index = [student_id])
        missing_assignments_series = missing_assignments_series.append(s1)
        
        

    for index, value in missing_assignments_series.items():
        if value > 2:
            s1 = pd.Series({index:value})
            more_than_two_missing_assignments = more_than_two_missing_assignments.append(s1)   
  
    more_than_two_missing_assignments = more_than_two_missing_assignments.sort_values(ascending=True)
    st.write(more_than_two_missing_assignments)


with col3: 
    st.subheader("Page Views")
    page_views_summary_series = pd.Series()

    row_count_page_views_df = len(page_views_transposed.columns)
    page_views_df.loc[row_count_page_views_df,:]= page_views_df.sum(axis=0)
    max_page_views = page_views_df.loc[row_count_page_views_df,:].max()
    avg_page_views = page_views_df.loc[row_count_page_views_df,:].mean()

    st.info("Max page views: " + str(round(max_page_views)))
    st.info("Avg page views: " + str(round(avg_page_views)))

    total_page_views_series = pd.Series()
    less_than_average_pv = pd.Series()
    #idea is to show students with below average page views 
    for i in page_views_df:
        #gets the end of the page_view dataframe to iterate through. 
        end_of_df = len(page_views_df)
        end_of_df = int(end_of_df)-1
        #getting the students page vews 
        col_number = page_views_df.columns.get_loc(i)

        #page_view_total = page_views_df.loc[row_count_page_views_df,i]

        

        student_cumulative_page_views = page_views_df.iat[end_of_df, col_number]
        #st.write(student_cumulative_page_views)

        student_id = str(i)
        

        s1 = pd.Series([student_cumulative_page_views], index = [student_id])
        #st.write(s1)
        total_page_views_series = total_page_views_series.append(s1)

    for index, value in total_page_views_series.items():
        if value < avg_page_views:
            s1 = pd.Series({index:value})
            less_than_average_pv = less_than_average_pv.append(s1)   


    #st.write(total_page_views_series) #used for testing 
    less_than_average_pv = less_than_average_pv.sort_values(ascending=False)
    st.write(less_than_average_pv)





# SECTION 1.5 
#Notes for section below : 4 series using 
#below_average_participations 
#more_than_two_missing_assignments 
#intersection1 
#difference 

#Moves all the index's into floats 
student_ids = student_ids.map(float).map(int)
below_average_participations.index = below_average_participations.index.map(int)
more_than_two_missing_assignments.index = more_than_two_missing_assignments.index.map(float).map(int)
less_than_average_pv = less_than_average_pv.index.map(float).map(int)

#Calculation of students to reach out out 
# Intersection 1 is a list of students in both the below average participation group and that have more than two missing assignments 
intersection_1 = below_average_participations.index.intersection(more_than_two_missing_assignments.index) 
#Intersection 2 is all student IDs who are in the intersection list about as well as students who have less than average page views. 
intersection_2 = intersection_1.intersection(less_than_average_pv)
#Different calculates sudents that have more than two missing assignments but are not in the below average participation or less than average page views list.
difference = more_than_two_missing_assignments.index.difference(intersection_2)


st.subheader("Recommended Students to Help")

col111, col222 = st.columns(2)
with col111:
    st.write("Highest Priority Students to reach out to")
    st.dataframe(difference)

with col222:
    st.write("Additional Students to reach out to")
    remaining_students = more_than_two_missing_assignments.index.difference(difference)
    st.dataframe(remaining_students)










#SECTION 2 
#Getting list of Assignments to use for Select Box 
st.header("Search for Specific Student ID or Module")
assignments = assignments_df.index

#2 column set 
col11, col22 = st.columns(2)

with col11:
    st.subheader("Module Level Data")
    selected_assignment = st.selectbox('Select Assignment', assignments)
        
    st.dataframe(assignments_transposed[selected_assignment].describe())

with col22:
    st.subheader("Student Level Data")
    #st.info("Drill down into the data for a specific student")
    student_ids = assignments_transposed.index
    selected_student_id = st.selectbox('Select student ID:', student_ids)
    st.dataframe(assignments_df[selected_student_id])













#SECTION 3 
#For the User to see all the data 
st.header("View All Data ")

#button to allow users to view the raw data 
if st.button('View Raw Data'):
    st.subheader("Assigment Grades by Student ID")
    st.dataframe(assignments_df)
    st.subheader("Page Views by Student ID")
    st.dataframe(page_views_df)
    #st.dataframe(page_views_transposed)
   
    st.subheader("Significant Participation by Student ID (WIP)")
    st.dataframe(participation_count_series)
    #st.dataframe(participation_df)

    st.subheader("List of all student ids in course")
   
    st.write(student_ids)
