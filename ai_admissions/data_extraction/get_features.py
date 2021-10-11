# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)
import csv
import regex
from ..utilities.config import PC

def get_ur(extracted_text, parser):
    """
    Args:
        transcript (string): transcript text
        parser (Parser class object)
    output:
        rating (int): University rating based on an exponential scale in range
                        [1, UN_gran], and UN_gran+1 if university not in list
    """
    lines = extracted_text.splitlines()
    # Rating is initialized to the value of (variable {ur_gran from function create_uni_dict from parsers.py} + 1)
    rating = PC['UR_GRAN'] + 1
    for line in lines:
        detected_uni, unies, ur = parser.find_university(line)
        if detected_uni:
            rating = list(set(ur))[0]
            break
    return rating

def get_cgpa(text):
    """
    Args:
        text (String): output text from gray_listing
    Returns:
        The CGPA (int), if CGPA found; else returns None
    """
    lines_containing_keywords = regex.findall(r'(?i)cumm?ulative.*\n',text)
    count = 0
    sum = 0
    if not lines_containing_keywords:
        output = regex.findall(r'[0-9]\.[0-9][0-9]',text)
        if not output:
            numbers = regex.findall(r' ([0-1])?[0-9][0-9][ \n]',text)
            if not numbers:
                return None
            else:
                for value in numbers:
                    sum = sum + float(value)
                    count = count + 1
        else:
            for value in output:
                sum = sum + float(value)
                count = count + 1
    else:
        for line in lines_containing_keywords:
            output = regex.findall(r'[0-9]\.[0-9][0-9]',line)
            if output:
                for value in output:
                    sum = sum + float(value)
                    count = count + 1

        if (sum == 0):
            for line in lines_containing_keywords:
                numbers = regex.findall(r' ([0-1])?[0-9][0-9][ \n]',line)
                if numbers:
                    for value in numbers:
                        sum = sum + float(value)
                        count = count + 1
    if (sum == 0):
        return None
    else:
        return sum/count

def get_train_labels(label_file_path):
    """ Assumes mongo db
    label_file_path: (Path object) path to csv file with the format: transcript_file_name, prediction_score
    collection: collection instance in the mongodb
    cipher_suite: cipher instance to encrypt file name
    """
    # Add provided gorund truth labels to the data base
    with open(label_file_path, newline='') as transcript_predictions_tr:
        label_reader = csv.reader(transcript_predictions_tr, delimiter=',')
        labels = list(label_reader)
    return labels
