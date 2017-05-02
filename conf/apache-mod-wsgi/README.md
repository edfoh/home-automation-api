## Setup on Apache2 with mod-wsgi

This setup is based on debian jessie lite running on a raspberry pi. There's already a user named `pi` that has the appropriate read permissions on the application folder, `/var/app/home-automation-api`

### Folder permissions (not the best approach but good enough for home use)

set `pi` as owner

    sudo chown -R pi /var/app/home-automation-api

set folder permissions

    sudo chmod 755 /var/app/home-automation-api

### Install Apache2

    sudo apt-get install apache2 apache2-doc apache2-utils

### Install MOD WSGI

    apt-get install libapache2-mod-wsgi

### Running Flask app on apache2 with mod WSGI

- see this [article](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/)

##### Check if mod wsgi is enabled

    ls /etc/apache2/mods-enabled/

Should see `wsgi.conf` and `wsgi.load`. If not copy the `wsgi` files from `/etc/apache2/mods-available`

    cp /etc/apache2/mods-available/wsgi* /etc/apache2/mods-enabled/

#### apache site configuration

see `/etc/apache2/sites-enabled/000-default.conf`

Update that file using [site.conf](site.conf) file as a guide.

#### apache configuration

see `/etc/apache2/apache2.conf`

Add this section into configuration

```
    <Directory />
        #Options FollowSymLinks
        Options Indexes FollowSymLinks Includes ExecCGI
        AllowOverride All
        Order deny,allow
        Allow from all
    </Directory>

    <Directory "/var/app/home-automation-api">
    Options Indexes FollowSymLinks Includes ExecCGI
    AllowOverride All
    Order deny,allow
    Allow from all
    </Directory>
```

#### update ports.conf

update `/etc/apache2/ports.conf` to include `Listen 5000`

#### restart and test

    sudo service apache2 restart

you should not see any errors. To troubleshoot, `cat /var/log/apache2/error.log` to see errors.
