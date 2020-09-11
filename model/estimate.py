#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 14:19:23 2020

@author: Ritesh Tiwary
"""
import spacy
import re
from preprocess.file_reader import FileReader

nlp_model = spacy.load('../nlp_model')


class Estimate:
    def __init__(self, x_test):
        self.x_test = x_test

    def preprocess(self):
        text = ''
        extension = self.x_test.split('.')[1]
        if extension == 'pdf':
            for page in FileReader(self.x_test).extract_text_from_pdf():
                text += ' ' + page
        elif extension == 'docx':
            text = FileReader(self.x_test).extract_text_from_docx()
        elif extension == 'doc':
            text = FileReader(self.x_test).extract_text_from_doc()
        elif extension == 'txt':
            text = FileReader(self.x_test).extract_text_from_txt()
        # return text # gaurav
        return re.sub('[^@://.,A-Za-z0-9]+', ' ', text).strip()  # gaurav

    def estimate(self):
        label_text = {}
        doc = nlp_model(self.x_test)
        for ent in doc.ents:
            label_text.update({ent.label_.upper(): ent.text})
        return label_text
