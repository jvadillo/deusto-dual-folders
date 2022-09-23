import os
import logging
import csv
import configparser
import datetime

# Load global variables from config.ini configuration file
config = configparser.ConfigParser()
config.read('config/students_folder_checker_config.ini')

FOLDERS_PATH = config['BASIC']['folders_path']
OUTPUT_CSV_PATH = config['BASIC']['output_csv_file']
FILENAMES_YEAR = config['BASIC']['filenames_year']
MODIFICATION_DATE_STR = config['BASIC']['modified_date_filter']
# Convert date string to datetime object:
MODIFICATION_DATETIME = datetime.datetime.strptime(MODIFICATION_DATE_STR, '%d-%m-%Y')
LOGGING_FILENAME = config['LOGGING']['logging_filename']


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
    


def get_modification_datetime(path):
    try:
        # file modification timestamp of a file
        m_timestamp = os.path.getmtime(path)
        # convert timestamp into DateTime object
        m_datetime = datetime.datetime.fromtimestamp(m_timestamp)
        return m_datetime
    except Exception as e:
        logging.error(e)

def is_newer(file_datetime, limit_datetime):
    try:
        if file_datetime > limit_datetime:
            return True
    except Exception as e:
        logging.error(e)
    return False


def is_valid_name(file_name, valid_document_names):
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

def check_folder_status(path, valid_document_names, modification_date):
    """ Checks all the given filenames looking for filename patterns.

        Parameters:
            path (str): folder path that contains all the files that will be scanned.
            valid_document_names (list): list containing all valid file names.

        Returns:
            folder_status (dict): dictionary with the result after checking all the filenames
    """

    # Before start checking documents, set all of them to False (not found)
    folder_status = {
        'Documento de seguimiento' : False,
        'Diario de aprendizaje' : False,
        'Evaluación del diario' : False,
        'Evaluación parcial de estancia en empresa' : False,
        'Evaluación final de estancia en empresa' : False
    }
    file_names = os.listdir(path)
    for filename in file_names:
        for key in folder_status :
            # Check if the current file has been already found:
            if folder_status[key] == True:
                continue # Continue with the next file
            # Check if the current filename is OK for the current file:
            if (
                is_valid_name(filename, valid_document_names[key]) and
                is_newer(get_modification_datetime(os.path.join(path, filename)), modification_date)
            ):
                folder_status[key] = True
                break
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
logging.info(f'Valid document filenames: {VALID_DOCUMENT_NAMES}')

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
    for folder_name in student_folders_names:
        student_folder = {
            'Foldername' : folder_name,
            'Files' : []
        }
        full_path = os.path.join(FOLDERS_PATH+folder, folder_name)
        if os.path.isdir(full_path) and FILENAMES_YEAR in folder_name:
            logging.info(f'---------> {folder_name}')
            folder_status = check_folder_status(full_path, VALID_DOCUMENT_NAMES, MODIFICATION_DATETIME)
            student_folder['Files'] = folder_status
            student['Folders'].append(student_folder)
    students.append(student)

write_result_to_csv(students, OUTPUT_CSV_PATH)

logging.info('Script successfully finished!')



