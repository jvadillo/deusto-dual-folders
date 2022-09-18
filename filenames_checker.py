import os
import logging
import configparser

# Load global variables from config.ini configuration file
config = configparser.ConfigParser()
config.read('filenames_checker_config.ini')

FOLDERS_PATH = config['BASIC']['folders_path']
FILENAMES_YEAR = config['BASIC']['filenames_year']
LOGGING_FILENAME = config['LOGGING']['logging_filename']

VALID_DOCUMENT_NAMES = [
    # Documento de seguimiento
    '_Seg_FA_S1_2021_2022',
    '_Seg_FA_S2_2021_2022',
    '_Seg_FA_S1_20212022',
    '_Seg_FA_S2_20212022',
    '_Seg_FA_2021_2022',
    '_Seg_FA_20212022',
    # Diario de aprendizaje
    '_Diario_Aprendizaje_S1_2021_2022',
    '_Diario_Aprendizaje_S1_20212022',
    '_Diario_Aprendizaje_S2_2021_2022',
    '_Diario_Aprendizaje_S2_20212022',
    '_Diario_Aprendizaje_2021_2022',
    '_Diario_Aprendizaje_20212022',
    'Diario_Aprendizaje_S1'
    'Diario_Aprendizaje_S2'
    # Evaluación del diario
    '_Ev_Diario_S1',
    '_Ev_Diario_S2',
    'Evaluacion Diario de Aprendizaje_S1',
    'Evaluacion Diario de Aprendizaje_S2',
    # Evaluación parcial y final de estancia en empresa
    '_Ev_Empresa_S1_Final',
    '_Ev_Empresa_S1_Parcial',
    '_Ev_Empresa_S2_Final',
    '_Ev_Empresa_S2_Parcial',
    'Evaluacion Trabajo en Empresa_S1_Final',
    'Evaluacion Trabajo en Empresa_S1_Parcial',
    'Evaluacion Trabajo en Empresa_S2_Final',
    'Evaluacion Trabajo en Empresa_S2_Parcial',
    # PFG
    'Diario_de_aprendizaje_PFG_DUAL',
]

# Configure the logger
logging.basicConfig(
    filename=LOGGING_FILENAME, filemode='w', encoding='utf-8',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S'
)

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

def print_to_log(students_filenames_result):
    for student in students_filenames_result:
        logging.info(f'{student}')
        for folder in students_filenames_result[student]:
            logging.info(f'--->{folder}')
            for filename in students_filenames_result[student][folder]:
                logging.info(f'------>{filename}')

subject_folders = []


logging.info('Starting script...')
logging.info(f'Document valid names: {VALID_DOCUMENT_NAMES}')

students_filenames_result = {}
students_folders = [name for name in os.listdir(FOLDERS_PATH) if os.path.isdir(os.path.join(FOLDERS_PATH, name))]
for folder in students_folders:
    # For each student:
    #   Get the subjects foldernames. For each subject folder:
    #       Get file names. Check if each filename follows a valid pattern name

    student_folders = os.listdir(FOLDERS_PATH+folder)
    subject_folders_result = {}
    for subject_folder in student_folders:
        full_path = os.path.join(FOLDERS_PATH+folder, subject_folder)
        
        filenames_result = []
        if os.path.isdir(full_path) and FILENAMES_YEAR in subject_folder:
            subject_folders_result[subject_folder] = []
            files = os.listdir(full_path)
            
            for filename in files:
                is_file_ok = isValidName(filename, VALID_DOCUMENT_NAMES)
                subject_folders_result[subject_folder].append({
                        filename : is_file_ok
                })

    students_filenames_result[folder] = subject_folders_result

print_to_log(students_filenames_result)

logging.info('Script successfully finished!')



