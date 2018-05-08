from rest_framework.exceptions import APIException, AuthenticationFailed, NotAuthenticated
from rest_framework.views import exception_handler
from django.http import Http404
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.conf import settings


def handle_exception(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    request = context['request']
    if (isinstance(exc, AuthenticationFailed) or
            isinstance(exc, NotAuthenticated)) and \
            request.user_agent.browser.family != 'Other':
        original_path = request._request.path_info
        headers = request.META
        print headers
        if 'HTTP_REFERER' in headers and \
                '/api/' not in headers['HTTP_REFERER'] \
                and '/api/' in headers['PATH_INFO']:
            pass
        else:
            return redirect(settings.URLS['base'] + 'login/' + '?next=' + original_path)
    # elif not (isinstance(exc, APIException) or
    #           isinstance(exc, Http404) or
    #           isinstance(exc, PermissionDenied)):
    #     logger.error('Unhandled Exception: {0}'.format(str(exc)))
    #     exc = APIException('Internal Server Error: '.format(str(exc), code=500))
    response = exception_handler(exc, {})

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
