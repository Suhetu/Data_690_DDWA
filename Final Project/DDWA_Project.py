import streamlit as st
import requests
from streamlit_extras.add_vertical_space import add_vertical_space
import csv
import sqlite3

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://img.rawpixel.com/s3fs-private/rawpixel_images/website_content/rm373batch15-bg-11.jpg?w=1200&h=1200&dpr=1&fit=clip&crop=default&fm=jpg&q=75&vib=3&con=3&usm=15&cs=srgb&bg=F4F4F3&ixlib=js-2.2.1&s=330dde5a4191a3d87204a2f9b040e3fe");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

st.header('DDWA Final Project✨')

add_vertical_space(3)
st.subheader('A Predictive Disease Project')

st.write("This machine learning system can diagnose two acute inflammations of bladder: 'Inflammation of Urinary Bladder' and 'Nephritis of Renal Pelvis Origin'. This medical dataset truly needs privacy! Hence a user can access this service and get preemptive disease diagnostics rather than disclosing this private information with anyone else, even a doctor.")

add_vertical_space(3)
st.subheader('Welcome, user!')
st.write('Please fill in the details asked for below!')

disease = st.selectbox("Select the disease for which you want prediction:", ["Inflammation of Urinary Bladder", 'Nephritis of Renal Pelvis Origin'])
temperature = st.number_input('Body Temperature (in Celcius):', value=0)
nausea = st.radio("Occurence of Nausea:", options=["No", "Yes"])
lumbar_pain = st.radio("Presence of Lumbar Pain:", options=["No", "Yes"])
urine_pushing = st.radio("Presence of Urine Pushing:", options=["No", "Yes"])
micturition_pain = st.radio("Presence of Micturition Pains:", options=["No", "Yes"])
burning = st.radio("Burning of Urethra/Itch/Swelling of Urethra Outlet:", options=["No", "Yes"])

data_list = []

if disease == 'Inflammation of Urinary Bladder':
    data_list.append('IUB')
elif disease == 'Nephritis of Renal Pelvis Origin':
    data_list.append('NRP')

data_list.append(temperature)

if nausea == 'Yes':
    data_list.append(1)
else:
    data_list.append(0)

if lumbar_pain == 'Yes':
    data_list.append(1)
else:
    data_list.append(0)

if urine_pushing == 'Yes':
    data_list.append(1)
else:
    data_list.append(0)

if micturition_pain == 'Yes':
    data_list.append(1)
else:
    data_list.append(0)

if burning == 'Yes':
    data_list.append(1)
else:
    data_list.append(0)

if st.button('Get Result!'):
    resp = requests.post('http://127.0.0.1:5000/predict', json={'data':data_list})

    add_vertical_space(3)
    num = resp.json()['prediction']*100
    result = 'Your chances of ' + disease + ' are ' + str(num)[:4] + ' %.'
    st.warning(result)

# Connecting to the geeks database
connection = sqlite3.connect('ddwa.db')
 
# Creating a cursor object to execute
# SQL queries on a database table
cursor = connection.cursor()
 
# # Table Definition
# create_table = '''CREATE TABLE patient_records7(
#                 temperature INTEGER NOT NULL,
#                 nausea TEXT NOT NULL,
#                 lumbar_pain TEXT NOT NULL,
#                 urine_pushing TEXT NOT NULL,
#                 micturition_pain TEXT NOT NULL,
#                 burning TEXT NOT NULL,
#                 iub TEXT NOT NULL,
#                 NRP TEXT NOT NULL);
#                 '''
 
# # Creating the table into our
# # database
# cursor.execute(create_table)
 
# Opening the diagnostics.csv file
file = open('diagnostics.csv')
 
# Reading the contents of the
# person-records.csv file
contents = csv.reader(file)
 
# SQL query to insert data into the
# patient_records table
insert_records = "INSERT INTO patient_records7 (temperature, nausea, lumbar_pain, urine_pushing, micturition_pain, burning, iub, nrp) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
 
# Importing the contents of the file
# into our person table
cursor.executemany(insert_records, contents)

# connection.execute("INSERT INTO patient_records4 (temperature, nausea, lumbar_pain, urine_pushing, micturition_pain, burning) VALUES (%d, %s, %s, %s, %s, %s)"%(temperature, nausea, lumbar_pain, urine_pushing, micturition_pain, burning))

# select_all = "SELECT * FROM patient_records"

# connection.execute('DROP TABLE patient_records')

# Committing the changes
connection.commit()
 
# closing the database connection
connection.close()