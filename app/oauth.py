from flask import url_for, redirect, request
from app import app
from rauth import OAuth2Service
# classes for dealing with OAuth sign in

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        '''
        :param provider_name: third party provider
        :return: starts object from config file
        '''
        self.provider_name = provider_name
        credentials = app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        '''
        Deals with redirecting the user to the OAuth provider
        :return:
        '''
        pass

    def callback(self):
        '''
        Deals with the response from OAuth provider
        :return:
        '''
        pass

    def get_callback_url(self):
        '''
        :return: url for callback from the OAuth provider
        '''
        return url_for('oauth_callback', provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(self, provider_name):
        '''
        Create the list of providers and returns the provider provided
        :param provider_name:
        :return:
        '''
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


# OAuth implementation for Facebook
class FacebookOAuthSingIn(OAuthSignIn):

    def __init__(self):
        super(FacebookOAuthSingIn, self).__init__(app.config['FCBK'])
        self.service = OAuth2Service(
            name = app.config['FCBK'],
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            reponse_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        if 'code' not in request.args:          # veritification token for fcbk
            return None, None, None
        oauth_session = self.service.get_auth_session(      #that token allows us to retrieve date from the session
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()}
        )
        me = oauth_session.get('me?fields=id,name,email').json()     #set a json data to access it
        return (
            app.config['FCBK'] + '$' + me['id'],
            me.get('email').split('@')[0],  # get nickname from email
            me.get('email')
        )

''' TO DO
class TwitterOAuthSingIn(OAuthSignIn):
    pass

class GoogleOAuthSingIn(OAuthSignIn):

    # https://developers.google.com/accounts/docs/OAuth2
    pass
'''
