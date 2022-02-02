# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)
# AI Admission Params
AAP = {} # pronounced as app
AAP['MODEL_PATH'] = './ai_admissions/ml/models/svm.joblib'
# AAP['DATA_BASE_URI'] = 'mongodb+srv://aman:aiadmission@cluster0-sbqeo.mongodb.net/test?retryWrites=true&w=majority'
AAP['DATA_BASE_URI'] = 'mongodb://localhost:27017/'
AAP['ENCODING'] = 'utf-8'
AAP['KEY'] = b'HaHLKga169b8-K4fwCCyGPCZoyGWO5j-nE7EXz5Exzw='

# Error Codes
error = {}
error['NONE'] = 0           # No Errors found
error['DDNE'] = -1          # Directory does not exist
error['PDF2I'] = -2         # PDF to Image conversion Failure
error['PP_DSKF'] = -3.1     # Pre-Processing Deskewing Failure
error['PP_BRF'] = -3.2      # Pre-Processing Border removal Failure
error['PP_DNF'] = -3.3      # Pre-Processing Image de-noising Failure
error['OCRF'] = -4.1        # Optical Character Recognition Failure
error['EXTF'] = -4.2        # Extracted text by OCR is empty
error['GRAYF'] = -5         # Gray Listing Failure

# PARSER CONFIGURATION
PC = {}
# App Data File Paths
PC['NAMES'] = './app_data/first_names.txt'
PC['UR'] = './app_data/university_rankings_2019.csv'
PC['CITIES'] = './app_data/cities.txt'
PC['UR_GRAN'] = 10
PC['INV_LABELS'] = ['PERSON', 'GPE', 'LOC']

# Output File Paths
OFP = {}
OFP['GRAY'] = './validated_transcripts'
OFP['OCR_IN'] = './tessinput.tif'

# OCR configuration
OCR_CONFIG = '-l eng --oem 3 --psm 1 --dpi 600 -c tessedit_write_images='

# File Formats
PNG = '.png'
TIF = '.tif'
