<?php
class sspmod_djangomodule_Auth_Source_MyAuth extends sspmod_core_Auth_UserPassBase {
    private $auth_key;
    private $django_url;

    public function __construct($info, $config) {
        parent::__construct($info, $config);
        if (!is_string($config['auth_key'])) {
            throw new Exception('Missing or invalid auth_key option in config. This is a particular token for contacting the Django API authentication function.');
        }
        $this->auth_key = $config['auth_key'];
        if (!is_string($config['django_url'])) {
            throw new Exception('Missing or invalid django_url option in config. We need to know where to contact the Django service for contacting the api. In the demo the url was: "http://sp.zimmermanzimmerman.com/check-user/"');
        }
        $this->django_url = $config['django_url'];
    }

    protected function login($username, $password){
    $ch = curl_init($this->django_url.$username."/".$password);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        'Authorization: Token '.$this->auth_key,
        'Accept: application/json',
        ));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        $response = json_decode(curl_exec($ch), true);
        if ($response['username']){
          $result = array(
            'uid' => array($response['username']),
            'displayName' => array($response['first_name']." ".$response['last_name']),
            'eduPersonAffiliation' => $response['groups'],
            'givenName' => array($response['first_name']),
            'sn' => array($response['last_name']),
            'mail' => array($response['email'])
          );
          return $result;
        }else{
           throw new SimpleSAML_Error_Error('WRONGUSERPASS');

        }
    }

}