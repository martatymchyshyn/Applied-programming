from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:garoro43@localhost:3307/My database'
db = SQLAlchemy(app)


@app.route("/api/v1/hello-world-20")
def index():
    return "Hello World 20"

if __name__ == "__main__":
    app.run()