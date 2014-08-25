from optparse import make_option
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Enter the user who needs to get a token'
    option_list = BaseCommand.option_list + (
        make_option(
            "-u",
            "--username",
            dest = "username",
            help = "supply username for adding a token",
            metavar = "USER"
        ),
    )


    def handle(self, *args, **options):
        if options['username']:
            user = options['username']
            print 'We will create a token for user %s' % user
            print 'Finding user %s' % user
            User = get_user_model()
            try:
                user_obj = User.objects.get(username=user)
                token, _ = Token.objects.get_or_create(user=user_obj)
                print 'We have found this user and created the following token \n'
                print '%s has now the following key: %s' % (user, token.key)

            except User.DoesNotExist:
                print 'Oeps... we did not find this user'

        else:
            raise CommandError('You need to supply a --username=example_user argument')

