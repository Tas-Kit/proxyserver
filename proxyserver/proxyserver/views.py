from revproxy.views import ProxyView
from django.shortcuts import redirect
from revproxy.response import get_django_response


class Proxy(ProxyView):

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
