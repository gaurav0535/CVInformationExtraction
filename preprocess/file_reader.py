#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 17:19:23 2020

@author: Ritesh Tiwary
"""
import re
import io
import docx2txt
import textract
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.pdfparser import PDFSyntaxError
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager


class FileReader:
    def __init__(self, filename):
        self.filepath = '../data/' + filename

    def extract_text_from_pdf(self):
        with open(self.filepath, 'rb') as fh:
            try:
                for page in PDFPage.get_pages(
                        fh,
                        caching=True,
                        check_extractable=True
                ):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(
                        resource_manager,
                        fake_file_handle,
                        codec='utf-8',
                        laparams=LAParams()
                    )
                    page_interpreter = PDFPageInterpreter(
                        resource_manager,
                        converter
                    )
                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()
                    yield text

                    # close open handles
                    converter.close()
                    fake_file_handle.close()
            except PDFSyntaxError:
                return

    def extract_text_from_docx(self):
        temp = docx2txt.process(self.filepath)
        text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
        return ' '.join(text)
        #return re.sub(' +', ' ', ' '.join(text))




    def extract_text_from_doc(self):
        text = textract.process(self.filepath)
        text = text.decode("utf-8")
        return text

    def extract_text_from_txt(self):
        with open(self.filepath, mode="r", encoding="ISO-8859-15") as f:
            text = f.read()

        return text
