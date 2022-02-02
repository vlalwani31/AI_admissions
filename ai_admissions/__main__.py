# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)
import glob
import numpy as np

from joblib import load
from pathlib import Path
from cryptography.fernet import Fernet

from .ocr.transcript import Transcript
from .db.database import AIAdmissionDB
from .ml.ai_admission_svr import train_svr
from .utilities.config import error, AAP, PC, OCR_CONFIG
from .data_extraction.parsers import Parser
from .data_extraction.get_features import get_train_labels
from .ocr.tesseract_ocr import tesseract_ocr
from .utilities.argparser import parse_arguments
from .utilities.error_handling import ErrorHandler
# from .db.database import AIAdmissionDB

def main():
    # Command line argument parsing
    args = parse_arguments()

    # Instantiate an error handler
    eh = ErrorHandler()

    # Obtaining input
    transcript_dir = Path(args.TranscriptDir)
    if (error['DDNE'] == eh.handle_directory_error(transcript_dir)):
        exit()

    # Setup cyber security
    # key = Fernet.generate_key()
    cipher_suite = Fernet(AAP['KEY'])
    
    # Setup a database client and collections
    db = AIAdmissionDB()
    tf_tr, tf_t, tp, tm, ft = db.initialize()

    # Load Parser data and initialize parser
    names_file_path = Path(PC['NAMES'])
    university_rank_path = Path(PC['UR'])
    world_cities = Path(PC['CITIES'])
    parser = Parser(names_file_path, university_rank_path, world_cities)

    # Load pre-trained SVM Regression model Trained on UCLA dataset
    svr = load(AAP['MODEL_PATH'])

    # Get training labels if train flag is ON
    if (args.train):
        train_data = get_train_labels(Path(args.train)) if (args.train) else None
        train_model_name = train_data[-1][0]

    # Running OCR
    transcripts = []
    flagged_transcripts = []
    # Read transcripts sorted by name from the transcript directory
    for i, transcript_path in enumerate(sorted(transcript_dir.glob('*.pdf'))):
        transcript = Transcript(transcript_path, cipher_suite)
        if (args.train):
            # add transcript only if it is not already in the training data
            if not tf_tr.find_one({'id' : transcript.tn}):
                transcript = tesseract_ocr(transcript,
                                            ocr_config=OCR_CONFIG,
                                            parser=parser,
                                            train=True,
                                            preprocess=args.preprocess)
                if not (transcript.flag):
                    # add data with labels to training data
                    transcript_data = transcript.get_data()
                    if (train_data[i][0] == transcript.tn):
                        transcript_data['RecScore'] = float(train_data[i][1])
                    else:
                        transcript_data['RecScore'] = None
                    tf_tr.insert_one(transcript_data)
                else:
                    flagged_transcripts.append(transcript)
        else:
            # add only if transcript is not already in test data
            if not tf_t.find_one({'id' : transcript.tn}):
                transcript = tesseract_ocr(transcript,
                                            ocr_config=OCR_CONFIG,
                                            parser=parser,
                                            train=False,
                                            preprocess=args.preprocess)
                if not (transcript.flag):
                    # add data to database
                    transcript_data = transcript.get_data()
                    tf_t.insert_one(transcript_data)

                    # Make SVR prediction on the go
                    test_transcript_features = np.array(list(transcript.features.values()))
                    # reshape needed because test data has a single sample only
                    rec_score = svr.predict(test_transcript_features.reshape(1,-1))[0]
                    tp.insert_one({'id': transcript.tn, 'predicted_score': round(rec_score,3)*100})
                else:
                    flagged_transcripts.append(transcript)

    # add flagged transcripts to the database
    for transcript in flagged_transcripts:
        if not ft.find_one({'id': transcript.tn}):
            ft.insert_one({'id': transcript.tn, 'errors': transcript.errors})
    
    if (args.train):
        model_info = train_svr(db, tf_tr, train_model_name)
        if not tm.find_one({'name': model_info['name']}):
            db.save_model(model_info, tm)
    
    return 0

if __name__ == '__main__':
    main()
