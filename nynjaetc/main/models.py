from django.db import models
from pagetree.models import Section
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import utc
from Crypto.Cipher import AES
import base64
from django.conf import settings
from django.db.models import signals
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django_fields.fields import EncryptedEmailField, EncryptedCharField




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
        #Preference.objects.get(slug='quiz_sequence').sectionpreference_set.all()
        #[<Section: Telaprevir Path>, <Section: Boceprevir Path>]
        
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


#Note: attempting to use pre-save doesn't work because we want a new 
#EncryptedUserDataField to refer to an already existing User.
# (null value in column "user_id" violates not-null constraint)
# Consider making a new form that saves a new encrypted email for a user.


def my_email_user(self, subject, message, from_email=None):
    """
    Sends an email to this user's encrypted email, if there is one.
    """
    self.email = self.get_profile().encrypted_email
    self.original_email_user(subject, message, from_email)
    self.email = '*****' # note -- this isn't stored.
    
def store_encrypted_email (user):
    """
    Saves the email to an EncryptedUserDataField object, which encrypts it.
    Then replaces it with an arbitrary value.
    Note -- since this triggers a second save, don't call it from signals.post_save.connect
    on an updated object.
    We should probably add a new form somewhere to allow users to change their email.
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
