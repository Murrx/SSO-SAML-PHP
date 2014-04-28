#Django auth provider SimpleSamlPhp

This module is a php extension for SimpleSamlPhp = SSP. With this module you will be able to use the Django authentication mechanism as backend for a SSP Identiy Provider.

Documentation source for creating extensions see [the documentation](https://simplesamlphp.org/docs/1.11/simplesamlphp-customauth)

##Instructions
1. Go to your root of the SSP installation

```shell
cd modules
```

```shell
mkdir djangomodule
```
```shell
cp ../core/default-enable .
```
Now this module is active

You have to make the directories lib/Auth/Source and add the MyAuth.php file. This is the custom written Django authentication provider.

To enable the module into the SSP identity provider:

Go to your root of the SSP install
```shell
cd config
```
```shell
vim authsources.php
```
Add this to the $config array
```php
'django-module-instance' => array(
                'djangomodule:MyAuth',
                'auth_key' => '1f0c2eee1246ee464fabd6d26bf52124154841bf',
                'django_url' => 'http://sp.zimmermanzimmerman.com/check-user/',
        ),
```
Adjust the auth_key to your auth_key (ask siem@zimmermanzimmerman.com for a token) add the django api URL.

In this $config file you are able to disable other authentication/authorization functions

Go to your root of the SSP install
```shell
cd metadata
```
```shell
vim saml20-idp-hosted.php
```
Here you will able to select the authentication module the IdP needs to use.

Replace the 'auth' key to 'auth' => 'django-module-instance'

Now the SSP IdP will use Django authentication for there authentication source