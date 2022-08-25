from collections import namedtuple
from multiprocessing.dummy import current_process
from tkinter.filedialog import test
import altair as alt
import math
import pandas as pd
import streamlit as st
import pickle 

#from sklearn.model_selection import train_test_split
from pickle import load
from math import log, floor
from pathlib import Path

#from ui_backend import chosen_ticker_func
#from ui_backend import * 

#@st.cache(suppress_st_warning=True)
#def start(): 


#Header information 
st.title("UC Berekeley Student Progress Tracker Tool", anchor=None)
st.subheader("Project 1 by Phoebe Gunter")
st.caption("This Bot allows professors of UC Berkeley courses to see which students are falling behind and not actively participating in class", unsafe_allow_html=False)


#Importing Assignments CSV and creating Assignments Dataframe 
data = Path("/Users/phoebegunter/Documents/FinTech-Workspace/Project1/Data/assignments.csv")
assignments_df = pd.read_csv(data, delimiter=",").rename(columns={"Unnamed: 0":"Assignment"})
assignments_df.set_index('Assignment', inplace=True) #sets the index of the Assignment dataframe 
assignments_transposed = assignments_df.T #Transposed Assignments Dataframe so that the student IDs are on the rows 

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
test_value = participation_df["id"].value_counts(dropna=True) 
average_participations = test_value.mean()
average_participations = round(average_participations)








#First Section with Recommendations 
st.header("Recommended Students to Help")

#Tells the professor how many students are in the class based on number of student ids in assignment df 
col_count = len(assignments_df.columns) #counts the number of student IDs in the class 
st.write("There are " + str(col_count) +  " students in this class." ) #displays the # of students in the class 



#working on calculating students with below average grades across modules 
assignments_df.loc[col_count,:]= assignments_df.sum(axis=0)
#I CANT GET THIS RENAME TO WORK 
assignments_df.loc[col_count,:0]= "Total"
assignments_df.loc[col_count:1] = "sum of student assignment values"
st.dataframe(assignments_df)
max_assignment_value = assignments_df.loc[col_count,:].max()
avg_assignment_value = assignments_df.loc[col_count,:].mean()


#First set of 3 columns 
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Significant Portal Events")
    st.write("Student ID's with below average participation in assignments and projects")
    #HOW DO I ADD TITLES TO THE COLUMNS 
    st.info("The average number of assignment submissions is " + str(average_participations) + ".")
    
    for index, value in test_value.items():
        if value < average_participations:
            s1 = pd.Series({index:value})
            below_average_participations = below_average_participations.append(s1)   
    st.write(below_average_participations)

st.header("Drill down into Specific Data")

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
        #st.dataframe(missing_assignments_series)
        

    for index, value in missing_assignments_series.items():
        if value > 2:
            s1 = pd.Series({index:value})
            more_than_two_missing_assignments = more_than_two_missing_assignments.append(s1)   
  
    more_than_two_missing_assignments = more_than_two_missing_assignments.sort_values(ascending=True)
    st.write(more_than_two_missing_assignments)


with col3: 
    st.subheader("Page Views")
    #idea is to show students with below average page views 




col_count_page_views = len(page_views_df.columns)
page_views_df.loc[col_count_page_views,:]= page_views_df.sum(axis=0)
max_page_views = page_views_df.loc[col_count_page_views,:].max()
avg_page_views = page_views_df.loc[col_count_page_views,:].mean()
st.write(max_page_views)
st.write(avg_page_views)

st.dataframe(page_views_df)




#Getting list of Assignments to use for Select Box 
assignments = assignments_df.index

#2 column set 
col11, col22 = st.columns(2)

with col11:
    st.subheader("Module Level Data")
    selected_assignment = st.selectbox('Select Assignment', assignments)
    if st.button('Select Assignment'):
        st.info("You selected assignemnt " + str(selected_assignment) + ".")
        
    st.dataframe(assignments_transposed[selected_assignment].describe())

with col22:
    st.subheader("Student Level Data")
    #st.info("Drill down into the data for a specific student")
    student_ids = assignments_transposed.index
    selected_student_id = st.selectbox('Select student ID:', student_ids)
    if st.button('Select Student'):
        st.info("You selected student ID" + str(selected_student_id) + ".")
    st.dataframe(assignments_df[selected_student_id])






#Section 3 
#For the User to see all the data 
st.header("View All Data ")

#button to allow users to view the raw data 
if st.button('View Raw Data'):
    st.subheader("Assigment Grades by Student ID")
    st.dataframe(assignments_transposed)
    st.subheader("Page Views by Student ID")
    st.dataframe(page_views_transposed)
    st.subheader("Significant Participation by Student ID (WIP)")
    st.dataframe(test_value)
    #st.dataframe(participation_df)


