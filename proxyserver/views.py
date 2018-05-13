from time import time
from revproxy.views import ProxyView
from django.shortcuts import redirect
from revproxy.response import get_django_response
from rest_framework.views import APIView
from django.conf import settings
import requests
import json
import os
from rest_framework_jwt.settings import api_settings
from ratelimit.decorators import ratelimit
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

decoder = api_settings.JWT_DECODE_HANDLER


def handle_jwt_refresh(request):
    jwt = None
    try:
        jwt = request.COOKIES['JWT']
        exp = decoder(jwt)['exp']
        now = int(time())
        if exp - now < settings.JWT_REFRESH_THRESHOLD:
            response = requests.post(
                settings.URLS['authserver'] + 'refresh_jwt/',
                data={
                    'token': jwt
                })
            if response.status_code == 200:
                jwt = json.loads(response.text)['token']
    except Exception as e:
        logger.error('Fail to refresh jwt: {0}'.format(str(e)))
    return jwt


class Proxy(ProxyView):

    # @ratelimit(key='post:username', rate='1/s', block=True)
    # @ratelimit(key='post:password', rate='1/s', block=True)
    @ratelimit(key='ip', rate='10/s', block=True)
    def dispatch(self, request, path=''):
        redirect_to = self._format_path_to_redirect(request)
        if redirect_to:
            return redirect(redirect_to)

        self.request_headers = self.get_proxy_request_headers(request)
        proxy_response = self._created_proxy_response(request, path)

        self._replace_host_on_redirect_location(request, proxy_response)
        self._set_content_type(request, proxy_response)

        response = get_django_response(proxy_response)

        self.log.debug("RESPONSE RETURNED: %s", response)
        return response


class AuthProxy(APIView, Proxy):

    def dispatch(self, request, path=''):
        request = self.initialize_request(request, path=path)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?
        jwt = None
        try:
            self.initial(request, path=path)
            jwt = handle_jwt_refresh(request)
            request.META['HTTP_COOKIE'] = 'uid=' + str(request.user.id)
            response = super(APIView, self).dispatch(request, path)
        except Exception as exc:
            logger.debug('AuthProxy error {0}'.format(str(exc)))
            response = self.handle_exception(exc)
        self.response = self.finalize_response(request, response, path=path)
        if jwt is not None:
            self.response.set_cookie('JWT', jwt)
        if 'staging' in os.environ['DJANGO_SETTINGS_MODULE'] \
                and 'HTTP_ORIGIN' in request.META \
                and 'localhost' in request.META['HTTP_ORIGIN']:
            self.response['Access-Control-Allow-Origin'] = request.META['HTTP_ORIGIN']
            self.response['Access-Control-Allow-Credentials'] = 'true'
            self.response['Access-Control-Allow-Headers'] = 'Content-Type'
            if request.method == 'OPTIONS':
                self.response.status_code = 200
        return self.response
