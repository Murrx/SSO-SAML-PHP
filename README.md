#Django, SSO, SSP, WP
This documentation is about a configuration setup between SSP (SimpleSamlPhp as Identity provider), Wordpress (with SAML 2.0 plugin) and Django 1.6.x (as authenication backend).

To get an overview of this setup, check the Architecture overview in this Readme file.

In this github repository you will also find a configuration for a Django setup to use Django as a service provider. This has not been documented, only code has been provided.

##Django
Django has been used for providing user management, authentication and API for checking and validating users.

1. Clone this project
2. Install Django and install the requirements.txt file
3. Configure a database (SQLite, Mysql or other...)
4. Sync the database
```shell
./manage syncdb
```
5. Create a super user
```shell
./manage createsuperuser
```
6. Add a token to a certain user
```shell
./manage add_token_user -u a_username
```

##Architecture overview
![Architecture](/docs/architecture_ssp_django_wordpress.png)