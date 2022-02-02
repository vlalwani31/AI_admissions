# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)

def _safe_mkdir(directory, flag):
    if flag and directory is not None:
        if not directory.exists():
            directory.mkdir()

def _safe_join(path1, path2):
    if path1 is not None and path2 is not None:
        return path1 / path2
    else:
        return None
