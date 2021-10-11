# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)
import json
import regex
from pathlib import Path
from ..utilities.config import error, PC

def whitelist_grades(text):
    final_text = ""
    start_inserting = False
    for line in text.split("\n"):
        if(start_inserting == True):
            if(regex.search(r'[a-zA-Z][a-zA-Z].+(([0-9/]\.[0-9/])|( [A-F](t|\+|-)? )|( ([0-1])?[0-9][0-9] ))',line)):
                final_text = final_text + line + "\n"
            elif('UR,' == line[:3]):
                final_text = final_text + line + "\n"
        if(regex.search(r'(?i)((course)|(subject)){e<=1}',line)):
            start_inserting = True
    return final_text

def black_list(extracted_text, parser):
    """
    Args:
        extracted_text (string): transcript text
    output:
        text (string): returns text after removing NER Tagging, and dates
    """
    text = ""
    # lines = extracted_text.splitlines()
    # verified = False
    # # check names, university, city, country, sensitive keywords in each line
    # for line in lines:
    #     detected_name, names = parser.find_name(line)
    #     detected_uni, unies, ur = parser.find_university(line)
    #     detected_address, cities = parser.find_addresses(line)
    #     detected_sen_info, sen_info = parser.find_sensitive_info(line)

    #     #verified =  True if (detected_name or detected_uni or detected_address or detected_sen_info) else verified
    #     full_security = ((not detected_name) and (not detected_uni) and
    #                      (not detected_address) and (not detected_sen_info))
    #     if full_security:
    #         text += line + '\n'
    text = parser.remove_ner_tag(extracted_text, PC['INV_LABELS'])
    text = parser.remove_date(text)
    return text

def gray_listing(extracted_text, parser):
    """
    Args:
        extracted_text: (string) Extracted Text from the OCR
        parser: (Parser Class object) the parser instance for first names, UR, and cities
    Output:
        r: error code for gray_lising failure. default: r = error['NONE']
        text: (string) Text obtained after gray_listing extracted text
                See final report for gray_listing pipeline
    """
    # Whitelist grades from extracted text
    text = whitelist_grades(extracted_text)
    text = black_list(text, parser)
    r = error['NONE']
    if not text:
        r = error['GRAYF']
        text = ""
    return r, text
