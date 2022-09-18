import os
import logging
import csv
import configparser

# Load global variables from config.ini configuration file
config = configparser.ConfigParser()
config.read('students_folder_checker_config.ini')

FOLDERS_PATH = config['BASIC']['folders_path']
OUTPUT_CSV_PATH = config['BASIC']['output_csv_file']
FILENAMES_YEAR = config['BASIC']['filenames_year']
LOGGING_FILENAME = config['LOGGING']['logging_filename']
FILENAMES_YEAR = config['BASIC']['filenames_year']

# Valid file names for each document type
VALID_DOCUMENT_NAMES = {
    'Documento de seguimiento' : [
        '_Seg_FA_S1_2021_2022',
        '_Seg_FA_S2_2021_2022',
        '_Seg_FA_S1_20212022',
        '_Seg_FA_S2_20212022',
        '_Seg_FA_2021_2022',
        '_Seg_FA_20212022',
    ],
    'Diario de aprendizaje' : [
        '_Diario_Aprendizaje_S1_2021_2022',
        '_Diario_Aprendizaje_S1_20212022',
        '_Diario_Aprendizaje_S2_2021_2022',
        '_Diario_Aprendizaje_S2_20212022',
        '_Diario_Aprendizaje_2021_2022',
        '_Diario_Aprendizaje_20212022',
        'Diario_Aprendizaje_S1'
        'Diario_Aprendizaje_S2'
    ],
    'Evaluación del diario' : [
        '_Ev_Diario_S1',
        '_Ev_Diario_S2',
        'Evaluacion Diario de Aprendizaje_S1',
        'Evaluacion Diario de Aprendizaje_S2',
    ],
    'Evaluación parcial de estancia en empresa' : [
        '_Ev_Empresa_S1_Parcial',
        '_Ev_Empresa_S2_Parcial',
        'Evaluacion Trabajo en Empresa_S1_Parcial',
        'Evaluacion Trabajo en Empresa_S2_Parcial',
    ],
    'Evaluación final de estancia en empresa' : [
        '_Ev_Empresa_S1_Final',
        '_Ev_Empresa_S2_Final',
        'Evaluacion Trabajo en Empresa_S1_Final',
        'Evaluacion Trabajo en Empresa_S2_Final',
    ],
    'PFG' : [
        'Diario_de_aprendizaje_PFG_DUAL'
    ],
}

# Configure the logger
logging.basicConfig(
    filename=LOGGING_FILENAME, filemode='w', encoding='utf-8',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

def isValidName(file_name, valid_document_names):
    """"Checks if the given string is included in any of the patterns (string list).

        Paramenters:
            string (str): string that will be searched.
            patterns (list): string list with all the patterns that will be checked.
        Return
            (bool): True if the given string is included in any of the strings of the list.
    """
    upper_file_name = file_name.upper()    
    for filename in valid_document_names:
        if filename.upper() in upper_file_name:
            return True
    return False

def check_folder_status(filenames, valid_document_names):
    """ Checks all the given filenames looking for filename patterns.

        Parameters:
            filenames (list): list with all the filenames that will be scanned.

        Returns:
            folder_status (dict): dictionary with the result after checking all the filenames
    """

    # Before start checking documents, set all of them to false (not found)
    folder_status = {
        'Documento de seguimiento' : False,
        'Diario de aprendizaje' : False,
        'Evaluación del diario' : False,
        'Evaluación parcial de estancia en empresa' : False,
        'Evaluación final de estancia en empresa' : False
    }
    for filename in filenames:
        for key in folder_status :
            result = isValidName(filename, valid_document_names[key])
            if result:
                folder_status[key] = True
                continue
    logging.info(folder_status)
    return folder_status

def write_result_to_csv(students, output_csv_path):
    with open(output_csv_path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow([
            "Estudiante",
            "Carpeta" ,
            "Archivo",
            "¿Correcto?",
        ])

        rows = []

        # Generate all the rows and append them to the 'data' list
        for student in students:
            for folder in student['Folders']:
                for file in folder['Files']:
                    row = [
                        student['Name'],
                        folder['Foldername'],
                        file,
                        folder['Files'][file]
                    ]
                    rows.append(row)
        # write the data
        writer.writerows(rows)


logging.info('Starting script...')
logging.info(f'Patrones aceptados: {VALID_DOCUMENT_NAMES}')

students = []
students_folders = [name for name in os.listdir(FOLDERS_PATH) if os.path.isdir(os.path.join(FOLDERS_PATH, name))]
for folder in students_folders:
    # For each student...
    logging.info(f'---> {folder}')
    student_folders_names = os.listdir(FOLDERS_PATH+folder)
    student = {
        'Name' : folder,
        'Folders' : []
    }
    for f in student_folders_names:
        student_folder = {
            'Foldername' : f,
            'Files' : []
        }
        full_path = os.path.join(FOLDERS_PATH+folder, f)
        if os.path.isdir(full_path) and '2021.22' in f:
            logging.info(f'---------> {f}')
            files = os.listdir(full_path)
            folder_status = check_folder_status(files, VALID_DOCUMENT_NAMES)
            student_folder['Files'] = folder_status
            student['Folders'].append(student_folder)
    students.append(student)

write_result_to_csv(students, OUTPUT_CSV_PATH)

logging.info('Script successfully finished!')



