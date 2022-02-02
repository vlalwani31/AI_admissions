# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)
import cv2 as cv
import numpy as np

from pdf2image import convert_from_path
from pytesseract import image_to_string

from .pre_process import process_img
from ..utilities.config import error, TIF
from ..data_extraction.gray_listing import gray_listing
from ..data_extraction.get_features import get_ur, get_cgpa

def pdf2img(pdf_path):
    """ pdf_path: (pathlib posix Path object)
    Converts transcript PDF to image from the PDF file path & returns the image
    """
    transcript_pages = convert_from_path(pdf_path,
										dpi=500,
										fmt='TIF',
										transparent=True,
										use_cropbox=True,
										grayscale=True)
    return transcript_pages

def tesseract_ocr(transcript, ocr_config, parser, train=False, preprocess=False):
    # handler to set errors in the transcript
    se = transcript.set_error

    try: # Converting PDF to images
        transcript_pages = pdf2img(transcript.tp)
    except Exception:
        se(error['PDF2I'])
        transcript.flag = True
        return transcript

    # Extract Text for each page in transcript: 1)Pre-Process, 2) OCR
    extracted_text = ""
    for page_count, page in enumerate(transcript_pages):
        page_img = cv.cvtColor(np.array(page), cv.COLOR_RGB2BGR)
        if preprocess: # read documentation at ./ocr/pre_processing.py
            # processed_page = page_img if none of the pre-processing works
            r, processed_page = process_img(page_img)
            se(r) # r is a list of errors found in pre-processing
        else:
            processed_page = page_img

        try: # running OCR on pre_processed page images
            extracted_text += image_to_string(processed_page,
                                            config=ocr_config)
            if not extracted_text:
                se(error['EXTF'])
                transcript.flag = True
                return transcript
        except Exception:
            se(error['OCRF'])
            transcript.flag = True
            return transcript
        
        # Set University rating
        transcript.set_feature('UR', get_ur(extracted_text, parser))
        
        # Gray List extracted Text
        r, transcript.text = gray_listing(extracted_text, parser)
        se(r)
        if (r == error['GRAYF']):
            transcript.flag = True
            return transcript
        
        # Set CGPA
        transcript.set_feature('GPA', get_cgpa(transcript.text))

    return transcript

# def main():
#     	tesseract_ocr('/Users/aman/Desktop/aman/git/20-27-admissionAI/ai_admissions/output/519cd7f3-8ee3-4625-9b71-8d9f488e33a7-1.jpg')
# if __name__ == "__main__":
# 	main()
