# Documentation for GNU/LINUX
## Requirements
* PostgreSQL
* Git
* Python 3.12

## Installation
### Configure UTC
* Ubuntu
```commandline
sudo dpkg-reconfigure tzdata
```
### [PostgreSQL](./POSTGRESQL.md)
### [Dependencies](./DEPENDENCIES.md)
### Run Odoo
* Check version
```
odoo --version
```
* Create database

Use this command only in first time for create the database, the parameters are:

    -d: database name
    -r: username
    -w: password
```
odoo -d odoo17 -r odoo17 -w o --stop-after-init
```
or without demonstration data
```
odoo -d odoo17 -r odoo17 -w o --without-demo=all --stop-after-init
```
### Configuring the Odoo server options
* To see all the available options
```
odoo --help
```
* Creates a new **odoo.conf** configuration file
```
odoo -c odoo.conf --save --stop
```
* Edit **odoo.conf**
  * db_name = odoo17
  * db_password = o
  * db_user = odoo17
### Run odoo server
```
odoo -c odoo.conf
```
### Access to server default URL
* HTTP service (werkzeug) running on http://localhost:8069
* Default username and password is: admin admin
### Odoo commands quick reference

    -c,--conf=my.conf: Sets the configuration file to use.
    --save: Saves the config file.
    --stop,--stop-after-init: Stops after module loading.
    -d,--database=mydb: Uses this database.
    --db-filter=^mydb$: Filters the databases that are available using a regular expression.
    -p,--http-port=8069: The database port to use for HTTP.
    -i,--init=MODULES: Installs the modules in a comma-separated list.
    -u,--update=MODULES: Updates the modules in a comma-separated list.
    --log-level=debug: The log level. Examples include debug, debug_sql, debug_rpc, debug_rpc_answer, and warn. Alternatives for debugging specific core components are as follows:
        --log-sql: Debugs SQL calls
        --log-request: Debugs HTTP request calls
        --log-response: Debugs responses to HTTP calls
        --log-web: Debugs HTTP request responses
    --log-handler=MODULE:LEVEL: Sets the log level for a specific module. The following are examples:
        --log-handler=werkzeug:WARN
        --log-handler=odoo.addons:DEBUG
    --logfile=<filepath>: Sends the log to a file.
    --dev=OPTIONS: Options include all, [pudb|wdb|ipdb|pdb], reload, qweb, werkzeug, and xml.
