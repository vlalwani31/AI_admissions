# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)
from .config import error

class ErrorHandler:
    """
    An Error flag handling class
    """
    def __init__(self):
        super().__init__()
    
    def handle_directory_error(self, directory_path):
        """ Input: Path object
            if provided directory path doesn't exist or is not a directory
            Sets error flag (eflags) to -1
        """
        r = error['NONE']
        if ((not directory_path.exists()) or (not directory_path.is_dir())):
            print(f'File/Directory {directory_path.stem} does not exist')
            r = error['DDNE']
        return r
        