from django.db import models
from pagetree.models import Section
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import utc
from django.conf import settings
from django.db.models import signals
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django_fields.fields import EncryptedEmailField, EncryptedCharField, EncryptedTextField
from quizblock.models import Quiz
from django.contrib.auth.hashers import UNUSABLE_PASSWORD
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm
from registration.forms import RegistrationForm
from django import forms

#"""Let's turn off the ability to change email from the admin tool.
# (We can build a new version of this form later if it's needed.
# note -- if you need a new email address, just re-register.

admin.site.unregister(User)
old_personal_fields = UserAdmin.fieldsets[1][1]['fields']
new_personal_fields = tuple(x for x in old_personal_fields if x != 'email')
UserAdmin.fieldsets[1][1]['fields'] = new_personal_fields
admin.site.register(User, UserAdmin)


class UserProfile(models.Model):
    class Meta:
        app_label = 'main'

    user = models.ForeignKey(User, unique=True)
    encrypted_email = EncryptedEmailField ()
    hrsa_id = EncryptedCharField ()
    
    @staticmethod
    def find_user_profiles_by_plaintext_email(plaintext_email):
        try:
            return [ x for x in UserProfile.objects.all() if x.encrypted_email == plaintext_email ]
        except DjangoUnicodeDecodeError:
            
            raise ImproperlyConfigured ("""Looks like the setting for encryption /decryption doesn't match one of the values in the database.""")
class SectionTimestamp(models.Model):
    """Marks when this section was last visited by a particular user."""
    def __unicode__(self):
        return self.section.get_path()
    
    section = models.ForeignKey(Section, null=False, blank=False)
    timestamp = models.DateTimeField(null=False)
    user = models.ForeignKey(User,blank=False,null=False)
    unique_together = ("user", "section")
    def set_to_now (self):
        the_now = datetime.utcnow().replace(tzinfo=utc)
        self.timestamp = the_now
        self.save()


class SectionQuizAnsweredCorrectly(models.Model):
    """Marks, for nav purposes, when a section has been correctly answered."""
    def __unicode__(self):
        return self.section.get_path()    
    section = models.ForeignKey(Section, null=False, blank=False)
    user = models.ForeignKey(User,blank=False,null=False)
    unique_together = ("user", "section")


class Preference(models.Model):
    def __unicode__(self):
        return self.slug
    """ A way in which a Section can be special.
    Examples: Sections whose back buttons should be hidden.
    Sections whose next buttons should be hidden.
    Sections whose nav entry might be special in some way.
    """
    slug = models.SlugField(unique=True, null=False, blank=False)
    
    def sections(self):
        return [s.section for s in self.sectionpreference_set.all()]


class SectionPreference(models.Model):
    def __unicode__(self):
        return "%s has %s"  % (self.section, self.preference)
    """ A way to mark a section as special in some way."""
    section = models.ForeignKey(Section, null=False, blank=False)
    preference = models.ForeignKey(Preference, null=False, blank=False)
    class Meta:
        ordering = ['section', 'preference']
        unique_together = ("section", "preference")


####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################



def my_email_user(self, subject, message, from_email=None):
    """
    Sends an email to this user's encrypted email, if there is one.
    """
    self.email = self.get_profile().encrypted_email
    self.original_email_user(subject, message, from_email)
    self.email = '*****' # note -- this isn't stored.
    
def store_encrypted_email (user):
    """
    Saves the email to the profile.
    Then replaces it with an arbitrary value.
    Note -- since this triggers a second save, don't call it from signals.post_save.connect
    on an updated object.
    We're NOT allowing people to change their email, but they can
    
    
    reset their passwords at: 
        /accounts/password_change/
    """    
    
    if user == None or user.email == None:
        raise ValueError ('User or email is None.')
    the_profile, created = UserProfile.objects.get_or_create(user=user)
    the_profile.encrypted_email = user.email
    the_profile.save()
    #save dummy value in regular user field:
    user.email = '*****'
    user.save()
    

def steal_email(sender, instance, **kwargs):
    if kwargs['created']:
        store_encrypted_email(instance)
        
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
        

#MONKEY-PATCHERY

User.original_email_user = User.email_user
User.email_user = my_email_user
signals.post_save.connect(steal_email, sender=User)


Quiz.original_submit = Quiz.submit
def my_quiz_submit(self, user, data):
    hrsa_question_id = 17 # get_from_settings ?
    hrsa_question_key = 'question%d'  % hrsa_question_id
    
    try:
        hrsa_id = data[hrsa_question_key]
    except KeyError:
        hrsa_id = None
    
    if hrsa_id != None:   
        hrsa_id = data[hrsa_question_key]
        the_profile, created = UserProfile.objects.get_or_create(user=user)
        the_profile.hrsa_id = hrsa_id
        user.get_profile().save()
        data[hrsa_question_key] = "*****"
    self.original_submit(user, data)
Quiz.submit = my_quiz_submit


PasswordResetForm.original_save        = PasswordResetForm.save
def my_password_reset_form_save (self, domain_override=None,
    subject_template_name='registration/password_reset_subject.txt',
    email_template_name='registration/password_reset_email.html',
    use_https=False, token_generator=default_token_generator,
    from_email=None, request=None):
     
    #unencrypt emails
    for user in self.users_cache:
        user.email = user.get_profile().encrypted_email
    
    #send emails
    self.original_save (domain_override,
        subject_template_name,
        email_template_name,
        use_https, token_generator,
        from_email, request)
    
    #re-encrypt emails
    for user in self.users_cache:
        user.email = "*****"
PasswordResetForm.save = my_password_reset_form_save

def my_password_reset_form_clean_email (self):
    plaintext_email = self.cleaned_data["email"]
    user_profiles = UserProfile.find_user_profiles_by_plaintext_email(plaintext_email)
    self.users_cache = [u.user for u in user_profiles if u.user.is_active]
    if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
    if any((user.password == UNUSABLE_PASSWORD) for user in self.users_cache):
        raise forms.ValidationError(self.error_messages['unusable'])
    return plaintext_email        
PasswordResetForm.clean_email = my_password_reset_form_clean_email

RegistrationForm.original_clean = RegistrationForm.clean
def my_clean(self):
    self.original_clean()
    my_email = self.cleaned_data.get('email', None)
    if my_email:
        if UserProfile.find_user_profiles_by_plaintext_email(my_email):    
            raise forms.ValidationError("That email address is already in use.")
    return self.cleaned_data
    
RegistrationForm.clean = my_clean

####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
####################################
