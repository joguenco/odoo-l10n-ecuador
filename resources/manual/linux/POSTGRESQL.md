### Installing the PostgreSQL database
* Install
```commandline
sudo apt install postgresql
```
* Create user
```commandline
sudo su - postgres
```
```commandline
psql
```
```commandline
CREATE ROLE odoo17 WITH LOGIN NOSUPERUSER CREATEDB NOCREATEROLE INHERIT NOREPLICATION CONNECTION LIMIT -1 PASSWORD 'o';
```
* Show **pg_hba.conf** path
```commandline
show hba_file;
```
and Ctrl+D to exit psql and postgres user session
* Update pg_hba.conf

Search line
```
local   all             postgres                                peer
```
Add in the next line
```
local   all             odoo17                                  trust
```
Restart postgresql service
```
sudo systemctl restart postgresql
```
* Test mew odoo17 user
```commandline
psql -d postgres -U odoo17 -W
```
```
pgcli -d postgres -U odoo17 -W
```
### For access to database from remote host 
* Edit **postgresql.conf** file in the same directory of **pg_hba.conf** file
* Enable or add: listen_addresses = 'ip server'
* In **pg_hba.conf** add the next line:
```
host    all             odoo17          remote.host.ip/24.mask.number         trust
```
