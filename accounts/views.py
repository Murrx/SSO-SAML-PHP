from django.contrib.sites.models import Site, RequestSite
from registration import signals

from registration.backends.default.views import RegistrationView as BaseRegistrationView
from registration.models import RegistrationProfile
from rest_framework.serializers import _resolve_model
from django_sso import settings


class RegistrationView(BaseRegistrationView):
    def register(self, request, **cleaned_data):
        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                    password, site, send_email=False)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)

        # create user profile
        user_profile_model = _resolve_model(
            getattr(settings, 'REST_PROFILE_MODULE', None))
        user_profile_model.objects.create(user=new_user)

        return new_user