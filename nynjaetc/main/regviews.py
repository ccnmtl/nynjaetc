"""
We need to pull in and override a bunch of stuff here to
get registration to work with our app's approach of
storing emails encrypted on the profile object rather than
just directly on the User
"""

from django.template import RequestContext, TemplateDoesNotExist
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration.models import RegistrationProfile
from registration import signals

from registration.backends.default.views import RegistrationView \
    as BaseRegistrationView


def ccnmtl_send_activation_email(profile, site, request=None):
    """
    Send an activation email to the user associated with this
    ``RegistrationProfile``.

    The activation email will make use of two templates:

    ``registration/activation_email_subject.txt``
        This template will be used for the subject line of the
        email. Because it is used as the subject line of an email,
        this template's output **must** be only a single line of
        text; output longer than one line will be forcibly joined
        into only a single line.

    ``registration/activation_email.txt``
        This template will be used for the text body of the email.

    ``registration/activation_email.html``
        This template will be used for the html body of the email.

    These templates will each receive the following context
    variables:

    ``user``
        The new user account

    ``activation_key``
        The activation key for the new account.

    ``expiration_days``
        The number of days remaining during which the account may
        be activated.

    ``site``
        An object representing the site on which the user
        registered; depending on whether ``django.contrib.sites``
        is installed, this may be an instance of either
        ``django.contrib.sites.models.Site`` (if the sites
        application is installed) or
        ``django.contrib.sites.models.RequestSite`` (if
        not). Consult the documentation for the Django sites
        framework for details regarding these objects' interfaces.

    ``request``
        Optional Django's ``HttpRequest`` object from view.
        If supplied will be passed to the template for better
        flexibility via ``RequestContext``.
    """
    ctx_dict = {}
    if request is not None:
        ctx_dict = RequestContext(request, ctx_dict)
    # update ctx_dict after RequestContext is created
    # because template context processors
    # can overwrite some of the values like user
    # if django.contrib.auth.context_processors.auth is used
    ctx_dict.update({
        'user': profile.user,
        'activation_key': profile.activation_key,
        'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
        'site': site,
    })
    subject = getattr(
        settings,
        'REGISTRATION_EMAIL_SUBJECT_PREFIX', '') + \
        render_to_string(
            'registration/activation_email_subject.txt',
            ctx_dict)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    message_txt = render_to_string(
        'registration/activation_email.txt', ctx_dict)
    email_message = EmailMultiAlternatives(
        subject, message_txt, settings.DEFAULT_FROM_EMAIL,
        [profile.user.userprofile.encrypted_email])

    try:
        message_html = render_to_string(
            'registration/activation_email.html', ctx_dict)
    except TemplateDoesNotExist:
        message_html = None

    if message_html:
        email_message.attach_alternative(message_html, 'text/html')

    email_message.send()


class RegistrationView(BaseRegistrationView):
    def register(self, request, **cleaned_data):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        username, email, password = (cleaned_data['username'],
                                     cleaned_data['email'],
                                     cleaned_data['password1'])
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        # CCNMTL: first, we have the built-in profile *NOT* send
        # the activation email
        new_user = RegistrationProfile.objects.create_inactive_user(
            username, email, password, site,
            send_email=False,
            request=request,
        )
        # CCNMTL: then we do it ourselves
        rp = RegistrationProfile.objects.get(user=new_user)
        ccnmtl_send_activation_email(rp, site, request)
        # Now back to your regularly scheduled registration...
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user
