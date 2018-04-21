from revproxy.views import ProxyView
from django.shortcuts import redirect
from revproxy.response import get_django_response
from django.views.generic import View
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


# def jwt_require(func):
# 	def wrapper(self, request, path):
# 		pass

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


class APIProxy(Proxy):

    def dispatch(self, request, path=''):
        return super(Proxy, self).dispatch(request, path)

# class APIProxy(APIView):

#     def get(self, request, path):
#         print request.COOKIES
#         jwt = request.COOKIES.get('JWT')
#         payload = jwt_decode_handler(jwt)
#         print 'payload', payload
#         return HttpResponse('success')

#     def post(self, request, path):
#         print request.META
#         return HttpResponse('success')

# http POST http://localhost:8006/get_jwt/ username="root" password="abc12315"
# http POST http://localhost:8001/api/ username="root" password="abc12315"
# http http://localhost:8001/api/person/192 "Authorization: JWT eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvb3QiLCJ1c2VyX2lkIjoxLCJlbWFpbCI6Inp6aG9uZ0B0YXNraXQuY29tIiwiZXhwIjoxNTI0MDEwMDQ3fQ.kSnOv-haWaEAm_ke6ss8rSOTJyY6hFX1scqdFPS3-SAOAciVbJ8qi70Tg7ajZEzie5Iq0y8vlOZPzcD-DrqCOBYXUWROl4S4em05po7139x0cyJW8cYJBc1uGqPnfXgfALXj3wR6sah0JE-ymym4CpWK-WxArpfn7Poq48GRfBoXkEfSSpWFg9nVJHXaD855KNZX8do3dPiTEl0rXOFxb9RXJGJv44WV4FccoVamg_blohltZYRnfphMWf30RcXsq2ePVlsghsdsEAIZKooL6hM1NnjE1OyxosLdcrF_zeb0xaKvAYQOuBzBA3d9cRdh-gi-UytDpz0X1huNofDkB2p0x45fRUwBqsx7oWIg4ljKflRAExsqv0p98-IjuhI3aNhZF40KwJinusYPrHE0NySA_65f1Gccpg4n43QScWh2Fw8KTyS2-kQSAfZJ629rL8yF6v4mPPOjaM4H3YxNq1qPnL9gyp7h-pRLGG1ftEfIwjTZxu8gBUJjhFUDWKcX48GzHGnipmBjqVBNP5IrzoDFcasVyNbIiANaOt7ssVMyw_Xzu-IjRYZJPIdELWGvX2_cwsnMNCUoPnLeQ3N5wFdaYJxrj_yYDh7D88hnDIcznmXB39E0XVena0xsIrrewn8iCZK_1UxywpQLU_knsFdVFCt9xrqd29iwvO1TCMU"
# http POST http://localhost:8006/verify_jwt/ token="eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJvb3QiLCJ1c2VyX2lkIjoxLCJlbWFpbCI6Inp6aG9uZ0B0YXNraXQuY29tIiwiZXhwIjoxNTI0MDA5NjM2fQ.pcDiIwovDXxJhtmh2zWgdzMueWL20TJ8kD7HUA1qLpvaJanmcWUHPEChwIYdd-59TnDpXf79v04msTm_eduPb4D4kp-j7-35RZ1vQyoDzf1yoJ2k2IWOM12ModmPQkNWrkb5zjn6ErQ4EyXFxW-rYEjoaPnI5CUrPdYekaojkmoYOQuHOmGYupEKNO9eJVqqWvpIyKeXNpkgP_kloMq97TUrWED0vloIZ06Wv8eC3T3kIKyRnBVG2VOa-C6x_f5EzM4rrzMPmrKEaZtwKFk_Jyeyb-HsiJSqj0GNtFepi9YGBHU-Rpyx0vJ2fIaPYNythxmt-WBF7CJ4CL-M3sR6Qdju4euJbyUXW4BFTBbIzdC3NOUQwjvyvIG8zpet49K4Avrmhvog_deQbYXNXuzE33GZOHeZCTNAjKvJU8YoqMlbLS0hrrNKNt79hJARj18Q0JtIc0LXPvVWxv84JIU2R2X8d1J6irDoByaBab6D8372FG0staYmiJnQvMRKBEFtn-08zSJkNWw7an3UWD655oEw_-rzi2NLUwKqFuKl3H79hGcW9iP1VdLOUfIsYgkVSc3VA8e9_LijCUfo7rJEmO9QNjZaNbTiTkScXQbOdu-utdb1-H63J8VpScEqFuatcbTw_FmEJxtb3jWLDZQ71Pi3Zu5pP0h390kCezcMFmI"
