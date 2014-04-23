from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.RelatedField(many=True)
    class Meta:
        model = User
        fields = ('id','username', 'first_name', 'last_name', 'email', 'groups')

@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def check_username_password(request, username, password):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':

        if authenticate(username=username, password=password):
            user = User.objects.get(username=username)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        else:
            #User params are not correct, so we return a unauthorized response
            return Response(status=401)