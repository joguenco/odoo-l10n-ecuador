## Ubuntu 24.04
* Git
```
sudo apt install git
```
* Python
```
sudo apt install python3-dev python3-pip python3-wheel python3-venv python3-virtualenv
```
```
sudo apt install build-essential libpq-dev libxslt-dev libzip-dev libldap2-dev libsasl2-dev libssl-dev
```
* CSS processor
```
sudo apt install npm
```
```
sudo npm install -g less less-plugin-clean-css
```
* wkhtmltopdf HTML to PDF

Go to wkhtmltopdf.org and download your compatible version
```
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.jammy_amd64.deb
```
```
sudo apt install ./wkhtmltox_0.12.6.1-3.jammy_amd64.deb
```
* Get odoo source code
```
git clone https://github.com/odoo/odoo.git -b 17.0 --depth=1
```
* Create python virtual environment
```
cd odoo
```
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
* Activate python virtual environment
```
source venv/bin/activate
```
* Update pip and tools
```
pip install -U pip
pip install --upgrade wheel
pip install --upgrade setuptools
```
* Install requirements
```
pip install -r requirements.txt
```
* Install source code files
```
pip install -e ./
```
* Additional dependencies
```
pip install phonenumbers
```
