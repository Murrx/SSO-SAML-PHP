from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import CustomUser

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
def check_token(request):
    resp = Response()
    if request.method == "POST":
        token = request.DATA.get('token', '')
        api_request = request.DATA.get('request', '') #not used yet
        method = request.DATA.get('method', '') #not used yet

        user = None
        try:
            user = CustomUser.objects.get(auth_token=token)
        except CustomUser.DoesNotExist:
            resp.status_code = 401

        serializer = UserSerializer(user, many=False)
        resp.data = serializer.data
    else:
        resp.status_code = 405

    return resp
        

class Home(TemplateView):
    template_name = 'home.html'
