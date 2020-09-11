#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 12:19:23 2020

@author: Ritesh Tiwary
"""
import os
from flask import Flask
from flask_cors import CORS
from flask_restplus import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
from model.estimate import Estimate


app = Flask(__name__)
CORS(app)
api = Api(app,
          version='1.0',
          title='Resume Parser',
          description='Resume Parser Api(s) is designed for extracting information from resume(s).',
          default='Resume Parser Api',
          default_label='Api(s) for Resume Parser'
          )

upload_parser = reqparse.RequestParser(bundle_errors=True)
upload_parser.add_argument('resume', location='files', type=FileStorage, required=True)


@api.route('/upload')
class Upload(Resource):
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        uploaded_file = args['resume']
        uploaded_file.save('../data/' + uploaded_file.filename)
        x_test = Estimate(uploaded_file.filename).preprocess()
        data = Estimate(x_test).estimate()
        os.remove('../data/' + uploaded_file.filename)
        return data


if __name__ == '__main__':
    app.run()
