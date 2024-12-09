## Create python virtual environment
```
virtualenv venv
```
or
```
virtualenv -p python3.12 venv
```
or
```
python3.12 -m venv venv
```
## Activate python virtual environment
```
source venv/bin/activate
```
## Update pip and tools
```
pip install -U pip
pip install --upgrade wheel
pip install --upgrade setuptools
```
## Install linter and code formatter (Ruff)
```
pip install ruff
```
### Check syntax
```
ruff check .
```
### Format
```
ruff format .
```
## Install dependencies
```
pip install git+https://github.com/joguenco/xades-bes-sri@0.1.0
```
```
pip install -r requirements.txt
```
## Run app
```
python src/__main__.py
```
## Generate requirements.txt
```
pip freeze > requirements.txt
```