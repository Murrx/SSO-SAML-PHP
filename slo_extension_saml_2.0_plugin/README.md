#Enable SLO for Wordpress
The purpose of this extension is to enable Single logout for wordpress.

Requirement for this extension is that you install the [SAML 2.0 Single Sign-On plugin](http://wordpress.org/plugins/saml-20-single-sign-on/)

##Configuration
1. Install and activate the [SAML 2.0 SSO plugin](http://wordpress.org/plugins/saml-20-single-sign-on/).
2. Go to the root of the Wordpress installation

```shell
cd /wp-content/plugins/saml-20-single-sign-on
```
```shell
vim samlauth.php
```
Add this at the end of the samlauth.php file
```php
function is_user_logged_in() {
        global $as;

        $user = wp_get_current_user();
        if ( $user->ID > 0 ) {
            // User is local authenticated but SP session was closed
            if (!isset($as)) {
                $as = new SimpleSAML_Auth_Simple((string)get_current_blog_id());
            }

            if(!$as->isAuthenticated()) {
                wp_logout();
                return false;
            } else {
                return true;
            }
        }
        return false;
    }
```

This code ensures that a logged in user also needs a SimpleSamlPhp session.
