from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import (
    ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken)


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class CafeObtailJSONWebToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response_data.update(status=True, **user.to_json())
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        response_data = serializer.errors
        response_data.update(status=False)
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class CafeRefreshJSONWebToken(RefreshJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response_data.update(status=True, **user.to_json())
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        response_data = serializer.errors
        response_data.update(status=False)
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class CafeVerifyJSONWebToken(VerifyJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response_data.update(status=True, **user.to_json())
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response

        response_data = serializer.errors
        response_data.update(status=False)
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


obtain_jwt_token = CafeObtailJSONWebToken.as_view()
refresh_jwt_token = CafeRefreshJSONWebToken.as_view()
verify_jwt_token = CafeVerifyJSONWebToken.as_view()
