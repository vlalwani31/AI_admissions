# Copyright 2020, AI Admissions: Ahmed, Aman, Paschal, Varun (Boston University)
import numpy as np
from pymongo import MongoClient
from ..utilities.config import AAP

class AIAdmissionDB:
    def __init__(self):
        super().__init__()
    
    def initialize(self):
        client = MongoClient(AAP['DATA_BASE_URI'])
        db = client.ai_admission
        tf_tr = db.transcript_tr
        tf_t = db.transcript_features_test
        tp = db.transcript_predictions
        tm = db.trained_models
        ft = db.flagged_transcripts
        return tf_tr, tf_t, tp, tm, ft

    def get_train_data(self, collection):
        X_tr = []
        Y_tr = []
        for document in collection.find({}):
            features = []
            features.append(document['UR'])
            features.append(document['GPA'])
            X_tr.append(np.array(features))
            Y_tr.append(document['RecScore'])
        X_tr = np.array(X_tr)
        Y_tr = np.array(Y_tr)
        return X_tr, Y_tr

    def save_model(self, model_info, collection):
        collection.insert_one(model_info)
        return None
    
    def load_saved_model(self, model_name, collection):
        data = collection.find_one({'name': model_name})
        return data['model']
