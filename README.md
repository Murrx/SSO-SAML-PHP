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


##Architecture overview
![Architecture](/docs/architecture_ssp_django_wordpress.png)