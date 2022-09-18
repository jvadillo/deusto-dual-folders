# TODOS:
# 1: From CSV to Dictionary
# 2: How to create a folder
# 3: How to unzip file
# 4: Logger

import os
import csv
import logging
import zipfile


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

# Configure the logger
logging.basicConfig(
    filename='app.log', filemode='w', encoding='utf-8',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')
# Variables for logs
created_students_folders = 0
created_subjects_folders = 0

logging.info('Starting script...')

# Current path
cwd = os.getcwd()
# Destination path
dest_folder = os.path.join(cwd,'dest')

# Open CSV
with open('data.csv', mode='r', encoding='utf8') as file:
   reader = csv.DictReader(file, skipinitialspace=True)
   # Read all the lines one by one
   for line in reader:
       logging.info(f'Reading {line["Apellidos, Nombre"]}')
       # Get the student folder
       # OLD: student_folder = os.path.join(dest_folder, f'{line["Apellidos, Nombre"]} GID SEGUIMIENTO DUAL')
       student_folder_name = line["Carpetas existentes"]
       current_year = line["Curso"]

       if (student_folder_name == ""):
           student_folder_name = line["Propuesta de carpeta"]
       student_folder = os.path.join(dest_folder, student_folder_name)
       
       # Create it if it does not exist
       if not os.path.exists(student_folder):
           os.mkdir(student_folder)
           created_students_folders += 1 # update variable for logging
           logging.info(f'Creada carpeta {student_folder} [curso:{current_year}]')
       # Create folders for dual subjects and extract templates:
       logging.debug(f'Subcarpetas a crear: {course_options[current_year]["folders"]}')
       for folder in course_options[current_year]["folders"]:
           subject_folder = os.path.join(student_folder,folder)
           try:
               logging.debug(f'Extracting: {course_options[current_year]["plantillas"]}')
               created_subjects_folders += 1
               with zipfile.ZipFile(course_options[current_year]["plantillas"]) as z:
                   z.extractall(subject_folder)
                   logging.debug(f'Extracted: {subject_folder}')
           except:
               logging.debug(f'ERROR uncompressing: {subject_folder}')
            
logging.info(f'Created {created_students_folders} folders for new students.')
logging.info(f'Created {created_subjects_folders} subjects folders.')
