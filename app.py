import os, sys
from flask import Flask
from src.logger import logging
from src.exception import CustomException

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
    try:
        raise Exception("We are testing our custom file")
        
    except Exception as e:
        abc = CustomException(e, sys)
        logging.info(abc.error_message)
        return "welcome  Amit"

if __name__ == "__main__":
    app.run(debug=True)