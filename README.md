# Applied-programming
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pyenv.

```bash
pip install pyenv
```
Use the package manager pyenv to install python.

```bash
pyenv install 3.7.4
```
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pipenv.

```bash
pip install --user pipenv
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install flask.

```bash
pip install flask
```
## Usage

```python
from flask import Flask
app = Flask(__name__)

@app.route("/api/v1/hello-world-20")
def index():
    return "Hello World 20"

if __name__ == "__main__":
    app.run()
```
## .gitignore
Added .python-version and .vscode/  to gitignore

## License
[MIT](https://choosealicense.com/licenses/mit/)
