import json
import requests

LOGIN_ENDPOINT = 'https://identitysso.betfair.com/api/login'

class Betfair:    
    
    def __init__(self, api_key: str, session_id: str | None = None, 
                 username: str | None = None, password: str | None = None):
        """The Betfair object provides the login service - the instance object is then used
            for all calls to Betfair API endpoints. The api_key must be provided to be
            used by the API functions. A session_id can be provided directly if
            log on has been done by some other method, in which case username and password
            are ignored. Otherwise, a username and password must be provided and then the
            login method called to obtain a session_id.
            
            Args:
                api_key (str): Betfair api key for authorising api endpoints
                session_id (str): Session ID (usually returned after a successful login)
                    - should only be provided if login has been done by an external function
                username (str): Betfair username - ignored if session_id is provided
                password (str): Betfair password - ignored if session_id is provided

            Returns:
                Betfair object, used for calling API endpoints
        """

        #check that either the session_id has been passed, or password and username are both
        #specified
        if session_id is None and (username is None or password is None):
            return ValueError('Either session_id or both username and password must be provided')

        self.api_key = api_key
        self.username = None

        #if session_id is not provided, use the username and password to attempt to login
        if session_id is None:
            self.username = username
            login_response = self._login(username, password)


    def _login(self, username: str, password: str):
        header = {'X-Application' : self.api_key,'Content-Type' : 'application/x-www-form-urlencoded',
                  'Accept' : 'application/json' }
        #construct the payload
        #TODO expect this doesn't work if password contains certain special characters such as '&' and maybe '='
        payload = 'username=' + username + '&password=' + password + '&'
        payload += 'login=true&redirectMethod=POST&product=home.betfair.int&url=https://www.betfair.com/'

        response = requests.post(LOGIN_ENDPOINT, data=payload, headers=header)
        response_json = json.loads(response.text)
        return response_json