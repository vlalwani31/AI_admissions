from flashtext import KeywordProcessor
import csv
import spacy
import math
import regex as re
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = spacy.load("en_core_web_sm")
# pip install spacy
# python -m spacy download en

def create_uni_dict(universities, ur_gran=10):
    """ Input:
        universities- Path object, path to csv file: rank, university
        ur_gran: integer, define the range of university rating: [1,ur_gran]
        Output:
        ur(university ratings)- dictionary, keys(university), value(ur)
    """
    # Count number of universities in the file
    with open(universities, mode='r') as unies:
        num_unies = sum(1 for line in unies)
    
    # create a dictionary and assignn them ratings
    ur = dict()
    with open(universities, mode='r') as ur_csv:
        ur_reader = csv.reader(ur_csv)
        for row in ur_reader:
            rank = int(row[0])  # 1st col has university rank
            uni_name = row[1]   # 2nd col has university name
            ur[uni_name] =  math.ceil((ur_gran - 1) * (math.e ** ((-1 * (rank ** 0.75)) / 60)) + 1)
            #ur[uni_name] = 9 * ur_gran - int((rank/num_unies)*(ur_gran-1))
    return ur

class Parser:
    def __init__(self, names, universities, cities):
        self.sensitive_keywords = [
            'high', 'school', 'academy', 'public', 'private',
            'international', 'global', 'world', 'boarding',
            'university', 'institute', 'college', 'pacific', 'registrar',
            'office', 'name', 'student', 'identification', 'enrollment',
            'date', 'issued', 'state', 'postal', 'avenue', 'road', 'street',
            'alley', 'lane']
        self.names = KeywordProcessor()
        self.cities = KeywordProcessor()
        self.urd = create_uni_dict(universities, 10)
        self.unies = KeywordProcessor()
        self.sen_keys = KeywordProcessor()
        # add keywords to initialize parser keywords
        self.names.add_keyword_from_file(names)
        self.cities.add_keyword_from_file(cities)
        self.unies.add_keywords_from_list(list(self.urd.keys()))
        self.sen_keys.add_keywords_from_list(self.sensitive_keywords)

    def add_sensitive_keyword(self, sensistive_word):
        self.sensitive_keywords.append(sensistive_word)

    def find_name(self, line):
        names = self.names.extract_keywords(line)
        if (names):
            return True,names
        else:
            return False,None
    
    def find_addresses(self, line):
        cities = self.cities.extract_keywords(line)
        if (cities):
            return True,cities
        else:
            return False,None

    def find_university(self, line):
        unies = self.unies.extract_keywords(line)
        ur = []
        for uni in unies:
            ur.append(self.urd[uni])
        # self.urd[unies[0]
        if (unies):
            return True,unies,ur
        else:
            return False,None,None
    
    def find_sensitive_info(self, line):
        sen_info = self.sen_keys.extract_keywords(line)
        if (sen_info):
            return True,sen_info
        else:
            return False,None
    
    def remove_ner_tag(self, line, invalid_labels):
        doc = nlp(line)
        result = line
        for ent in doc.ents:
            if ent.label_ in invalid_labels:
                result = result.replace(ent.text, "")
        return result

    def remove_date(self, text):
        regExpression = r'(\b(0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](0?[1-9]|1[0-2])[^\w\d\r\n:](\d{4}|\d{2})\b)|(\b(0?[1-9]|1[0-2])[^\w\d\r\n:](0?[1-9]|[12]\d|30|31)[^\w\d\r\n:](\d{4}|\d{2})\b)|(\b(\d{4})(0[1-9]|1[0-2])(0[1-9]|[12]\d|30|31)\b)|(^(19|20)\d\d[- \/.](0[1-9]|1[012])[- \/.](0[1-9]|[12][0-9]|3[01])$)'
        return re.sub(regExpression, "", text)
