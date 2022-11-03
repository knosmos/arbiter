'''
Server code and full application flow.
'''

import arc_feedback, distribute, toposort
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

