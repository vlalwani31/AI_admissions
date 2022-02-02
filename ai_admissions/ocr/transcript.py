# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)
import datetime
from ..utilities.config import AAP

class Transcript:
    def __init__(self, transcript_path, cipher_suite):
        """ transcript_path is a pathlib posix Path object to the transcript PDF
        """
        super().__init__()
        self.tp = transcript_path   # Path to Transcript PDF
        self.id = cipher_suite.encrypt(bytes(str(self.tp.stem), AAP['ENCODING']))
        self.tn = str(self.tp.stem) # Transcript name
        self.text = ""              # Validated Text
        self.features = dict()      # key: Transcript features-'UR','GPA',..
        self.errors = []            # A list of all errors encountered
        self.flag = False           # True if transcript is flagged by the ErrorHandler class

    def get_data(self):
        transcript_data = {}
        transcript_data['id'] = self.tn
        transcript_data['date'] = datetime.datetime.utcnow()
        transcript_data.update(self.features)
        return transcript_data

    # Setter functions ()
    def set_feature(self, feature, value):
        """ feature: (string) feature name. For eg, 'UR', 'GPA', ...
            value: (~) the extracted feature value
            sets the feature value obtained from validated text
        """
        self.features[feature] = value;
        return None
    
    def set_error(self, error_code):
        """ error_code: see ./utilities/config.py for error codes
        appends error code to the list
        """
        if type(error_code) is list:
            self.errors += error_code
        else:
            self.errors.append(error_code)
        return None
