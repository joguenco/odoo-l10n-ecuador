#!/bin/bash
#Send a parameter that contain the name of the folder where the odoo will be installed

if [[ -z $1 ]];
then
  echo "No parameter passed with the name of folder."
else
  echo "Parameter passed = $1"

  git clone https://github.com/odoo/odoo.git -b 17.0 --depth=1

  mv odoo $1

  cd $1

  python3.12 -m venv venv

  source ./venv/bin/activate

  python --version

  pip install -U pip

  pip install --upgrade wheel

  pip install --upgrade setuptools

  pip install -r requirements.txt

  pip install rlpycairo
  pip install phonenumbers

  pip install -e ./

  odoo --version

  odoo -d $1 -r $1 -w o --without-demo=all --stop-after-init

  odoo -c odoo.conf --save --stop

  mkdir custom_addons
fi
