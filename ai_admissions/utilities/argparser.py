# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('--TranscriptDir',
                required=True,
                type=str,
                help='Directory path to PDF transcripts (default: Transcripts)')

    parser.add_argument('--preprocess',
                action='store_true',
                help='Save processed images from PDFs',
                dest='preprocess')
    
    parser.add_argument('--train',
            type=str,
            help='Path to true recommendation scores files')
        
    return parser.parse_args()