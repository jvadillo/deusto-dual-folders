# The current script tests 'folders_script.py' script.
# It tests if the folders of the subjects for each student exists.
# Steps:
# 1. Iterate student list
# 2. For each of the student subjects check that the folder exists

import os
import csv
import logging

# Configure the logger
logging.basicConfig(
    filename='./logs/test.log', filemode='w', encoding='utf-8',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

year = '2022.23'

s1 = f'{year} Org. de la Emp. Ind'
s2 = f'{year} Sist. y Equip. Ind'
s4 = f'{year} Est. y Tra. dig'
s3 = f'{year} Nue. Tec para la Ind'
s3pfg = f'{year} Nue. Tec para la Ind+PFG'
s5 = f'{year} Plan. y des. de dig. ind'
s5pfg = f'{year} Plan. y des. de dig. ind+PFG'
s6 = f'{year} Ana. Ava de dat para la Ind+Fáb. Int'
s6pfg = f'{year} Ana. Ava de dat para la Ind+Fáb. Int+PFG'
pfg = f'{year} PFG'

folders_path = 'folders'

course_options = {
    '2o curso' : {
        'plantillas' : f'{folders_path}/plantillas_2.zip',
        'folders' : [s1,s2]
    },
    '3er curso' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s3,s4]
    },
    '3o S1 + movilidad S2' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s3]
    },
    '3o solo S2' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s4]
    },
    '3o S1 + movilidad S2' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s3]
    },
    '3o S1 + 4o S2' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s3,s6pfg]
    },
    '3o S1 (pendiente 4o S2)' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s3]
    },
    '3o S1 + 4o S2 (sólo mixtas)' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s3,s6]
    },
    '3o S1 + 4o PFG en S1' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s3pfg]
    },
    '4o curso' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s5,s6pfg]
    },
    '4o S2' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s6pfg]
    },
    '4o S2 (movilidad S1)' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s6pfg]
    },
    '4o S1 + PFG S1' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [s5pfg]
    },
    '4o S1 (sólo PFG)' : {
        'plantillas' : f'{folders_path}/plantillas_3_4.zip',
        'folders' : [pfg]
    }
}

# Current path
cwd = os.getcwd()
# Destination path
dest_folder = os.path.join(cwd,'dest')

# Open CSV
with open('data.csv', mode='r', encoding='utf8') as file:
   reader = csv.DictReader(file, skipinitialspace=True)
   # Read all the lines one by one (student by student)
   for line in reader:

       logging.info(f'Reading {line["Apellidos, Nombre"]}')

       # Get the student folder name
       student_folder_name = line["Carpetas existentes"]
       if (student_folder_name == ""):
           student_folder_name = line["Propuesta de carpeta"]

       # Get the student folder full path
       student_path = os.path.join(dest_folder, student_folder_name)

       current_course = line["Curso"]

       # Check if there is a folder for each subject
       for folder_name in course_options[current_course]["folders"]:
           # Get the full path of the subject folder
           folder_path = os.path.join(student_path, folder_name)
           # Check if it exists
           if not os.path.exists(folder_path):
               logging.warning(f'Folder not found:{folder_path}]')