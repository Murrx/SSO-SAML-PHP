from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import CustomUser, CallLog

import datetime

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.RelatedField(many=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'groups', 'auth_token')

@api_view(['GET'])
#@authentication_classes((TokenAuthentication,))
#@permission_classes((IsAuthenticated,))
def check_username_password(request, username, password):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        if authenticate(username=username, password=password):
            user = CustomUser.objects.get(username=username)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        else:
            #User params are not correct, so we return a unauthorized response
            return Response(status=401)

@api_view(['POST'])
def validate_token(request):
    resp = Response()
    if request.method == "POST":
        token = request.DATA.get('token', '')

        try:
            CustomUser.objects.get(auth_token=token)
        except CustomUser.DoesNotExist:
            resp.status_code = 401
    else:
        resp.status_code = 405
    return resp

@api_view(['POST'])
def authorize_call(request):
    """
    Authorizes calls. At the moment all calls are authorized.
    In the future a more complex method of authorization can be implemented here
    For now this only logs the calls that are made as a proof of concept.
    """
    token = request.DATA.get('token', '')
    api_request = request.DATA.get('request', '')
    method = request.DATA.get('method', '')

    user = CustomUser.objects.get(auth_token=token)
    log = CallLog(user=user, request=api_request, HttpMethod=method, datetime=datetime.datetime.now())
    log.save()

    return Response()
        

class Home(TemplateView):
    template_name = 'home.html'
