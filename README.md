#Django, SSO, SSP, WP
This documentation is about a configuration setup between SSP (SimpleSamlPhp as Identity provider), Wordpress (with SAML 2.0 plugin) and Django 1.6.x (as authenication backend).

To get an overview of this setup, check the Architecture overview in this Readme file.

In this github repository you will also find a configuration for a Django setup to use Django as a service provider. This has not been documented, only code has been provided.

##Django installation
Django has been used for providing user management, authentication and API for checking and validating users.

1. Clone this project
2. Install Django and install the requirements.txt file
3. Configure a database (SQLite, Mysql or other...)
4. Sync the database
```shell
./manage syncdb
```
Create a super user
```shell
./manage createsuperuser
```
Add a token to a certain user
```shell
./manage add_token_user -u a_username
```

SSP will be able to check users through http(s)//django_url/check-user/username/password

Do the following to test the check-user url.
```shell
curl -X GET http(s)://django_url/check-user/username/password -H 'Authorization: Token 1f0c2eeddfee3332e12464fabd6d26bf52124154841bf'
```

##SimpleSamlPhp installation as identity provider
Go to your server
```shell
cd /var/www
```
```shell
mkdir simplesamlphp
```
```shell
git clone https://github.com/simplesamlphp/simplesamlphp.git simplesamlphp
```
```shell
mkdir config
```
```shell
mkdir metadata
```
```shell
cp -R config-templates/* config/
```
```shell
cp -R metadata-templates/* metadata/
```
```shell
```
Install curl -sS https://getcomposer.org/installer | php
```shell
php composer.phar install
```
Fix dependency errors when they occur.

Configure apache
```shell
<VirtualHost *:80>
        ServerName url.domain.com
        DocumentRoot /var/www/simplesamlphp
        Alias /simplesaml /var/www/simplesamlphp/www
</VirtualHost>
```
###Configure SSP as identity provider
Go to your root of the SSP installation
```shell
vim config/config.php
```
Set the following options
```shell
'enable.saml20-idp' => true,
'enable.shib13-idp' => true,
```
####Adding service providers to our Identity Provider
```php
<?php
$metadata['http://sp.example.org/simplesaml/module.php/saml/sp/metadata.php/default-sp'] = array(
    'AssertionConsumerService' => 'http://sp.example.org/simplesaml/module.php/saml/sp/saml2-acs.php/default-sp',
    'SingleLogoutService'      => 'http://sp.example.org/simplesaml/module.php/saml/sp/saml2-logout.php/default-sp',
);
```
###Configure Django as authentication mechanism
See the written [documentation here](https://github.com/siemvaessen/SSO-SAML-PHP/tree/master/djangomodule)

##Configuration Wordpress
*search for plugin and install: Saml 2.0 single sign-on
*activate the plugin
*go to the settings of this plugin
*go to the tab Identity provider, and add http://your-url/simplesaml/saml2/idp/metadata.php to the URL to idP metadata. The plugin will find the right urls and save these settings
*go to the Service provider tab, choose for NameID Policy: urn:oasis:names:tc:SAML:2.0:nameid-format:transient
*Fill in the following attributes in order: uid, givenName, sn, mail, eduPersonAffiliation
*For the groups fill in Administrators group name: manager, Editors group name: employee. According to your group configuration.
*Check the box for allowing Unlisted users
*Go to the main settings page of this plugin and activate SAML authentication

####Enabling SLO
Wordpress with the SAML 2.0 plugin does not function out of the box with SLO (Single Logout).

See the following [documentation](https://github.com/siemvaessen/SSO-SAML-PHP/tree/master/slo_extension_saml_2.0_plugin) to enable this.


##Architecture overview
![Architecture](/docs/architecture_ssp_django_wordpress.png)