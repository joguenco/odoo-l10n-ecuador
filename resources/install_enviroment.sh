#!/bin/bash
#Send odoo version and the parameter that contain the name of the folder where the odoo will be installed

if [[ -z $1 ]]; then
  echo "No parameter passed with the Odoo version."
  exit 1
else
  echo "Parameter for Odoo version is: $1"
fi


if [[ -z $2 ]];
then
  echo "No parameter passed with the name of folder."
  exit 1
else
  echo "Parameter for folder name and database name is: $2"
fi

read -p "Press enter to continue ... " -n 1

git clone https://github.com/odoo/odoo.git -b $1 --depth=1

mv odoo $2

cd $2

python3.12 -m venv venv

source ./venv/bin/activate

python --version

pip install -U pip

pip install --upgrade wheel

pip install --upgrade setuptools

pip install -r requirements.txt

# For reports
pip install rlpycairo
pip install phonenumbers

# For hot reload
pip install watchdog

pip install -e ./

odoo --version

# odoo -d $2 -r $2 -w o --stop-after-init
# odoo -d $2 -r $2 -w o --without-demo=all --stop-after-init

odoo -c odoo.conf --save --stop

mkdir custom_addons

