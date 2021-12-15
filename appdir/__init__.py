from flask import Flask

app = Flask(__name__)

app.config.update(
    HOST = '0.0.0.0'
)

from appdir import routes