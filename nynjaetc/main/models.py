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


#"""Let's turn off the ability to change email from the admin tool.
#(We can build a new version of this form later if it's needed.
admin.site.unregister(User)
old_personal_fields = UserAdmin.fieldsets[1][1]['fields']
new_personal_fields = tuple(x for x in old_personal_fields if x != 'email')
UserAdmin.fieldsets[1][1]['fields'] = new_personal_fields
admin.site.register(User, UserAdmin)


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


class EncryptedUserDataField(models.Model):
    def __unicode__(self):
        return self.slug
    slug = models.SlugField(unique=True, null=False, blank=False)
    #TODO add some methods:
        #get_for_one_user
        #set_for_one_user
        #get_for_all_users field
    
    
class EncryptedUserData(models.Model):
    """A chunk of private, encrypted data associated with a user."""
    def __unicode__(self):
        return 'encrypted %s for %s' %(self.which_field.slug, self.user)

    which_field = models.ForeignKey(EncryptedUserDataField, null=False, blank=False)
    user = models.ForeignKey(User,blank=False,null=False)
    value = models.TextField(blank=True, help_text = "Value of the data")
    unique_together = ("user", "which_field")
    
    the_key = settings.ENCRYPT_KEY
    
    if the_key == None or the_key == '':
        raise RuntimeError ("Can't find the ENCRYPT_KEY, which we need to encrypt and decrypt this data.")
    
    aes = AES.new(the_key, AES.MODE_ECB)
    enc, dec = aes.encrypt, aes.decrypt
    
    def pad (self, a_string):
        """ The encryption algorithm assumes the string length is a multiple of 8.
        Accordingly, this return a padded string, prefixed with its original length"""
        block_length = 16 # the return value will be an integer multiple of this length
        bytes = bytearray (a_string.encode('utf-8'))
        prefixed_bytes = '%s,%s' % (len (bytes), bytes)
        padding_length = 2 * block_length -  len (prefixed_bytes) % block_length
        padding = padding_length * '#'
        assert len (prefixed_bytes + padding) % block_length == 0
        return prefixed_bytes + padding

    def unpad (self, some_bytes):
        """ The reverse operation of pad """
        the_len, comma, the_string = some_bytes.partition (',')
        return unicode(the_string)[0: int(the_len)]
    
    def put (self, plain):
        return base64.b64encode(self.enc(self.pad(plain)))
        
    def get (self, ciph):
        return self.unpad(self.dec(base64.b64decode(ciph)))
    
    def store_value (self, the_value):
        self.value = self.put (the_value)
        self.save()
        
    def retrieve_value (self):
        return self.get(self.value)

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



User.original_email_user = User.email_user

def retrieve_encrypted_email (user):
    assert user != None
    email_field = EncryptedUserDataField.objects.get(slug='email')
    assert email_field != None
    try:
        email_data = EncryptedUserData.objects.get(user = user, which_field=email_field)
    except EncryptedUserData.DoesNotExist:
        return None
    assert email_data != None
    decrypted_email = email_data.retrieve_value()
    assert decrypted_email != None
    assert decrypted_email != ''
    return decrypted_email

def my_email_user(self, subject, message, from_email=None):
    """
    Sends an email to this User. If an encrypted address is available, use that one.
    """
    #print "my_email_user"
    decrypted_email = retrieve_encrypted_email (self)
    if decrypted_email != None:
        self.email = decrypted_email
        #print "found a decrypted email; sending to %s" % self.email
        #print "sent to %s" %  self.email
        self.original_email_user(subject, message, from_email)
        self.email = '*****' # note -- this isn't stored.

    else:
        
        #print "found a regular email; sending to %s" % self.email
        self.original_email_user(subject, message, from_email)
    
    
def store_encrypted_email (user):
    """
    Saves the email to an EncryptedUserDataField object, which encrypts it.
    Then replaces it with an arbitrary value."""
    
    print "storing encrypted"
    assert user != None
    assert user.email != None
    
    email_field = EncryptedUserDataField.objects.get(slug='email')
    assert email_field != None
    
    encrypted_email = EncryptedUserData(which_field = email_field, user = user)
    encrypted_email.store_value (user.email)
    encrypted_email.save()
    
    #decrypt just to double-check:
    assert encrypted_email.retrieve_value() == user.email
    #save dummy value in regular user field:
    user.email = '*****'
    user.save()
    
    
def store_encrypted_email (user):
    """
    Saves the email to an EncryptedUserDataField object, which encrypts it.
    Then replaces it with an arbitrary value.
    Note -- since this triggers a second save, don't call it from signals.post_save.connect
    on an updated object.
    We should probably add a new form somewhere to allow users to change their email.
    """
    
    #print "storing encrypted"
    assert user != None
    assert user.email != None
    
    email_field = EncryptedUserDataField.objects.get(slug='email')
    assert email_field != None
    
    encrypted_email = EncryptedUserData(which_field = email_field, user = user)
    encrypted_email.store_value (user.email)
    encrypted_email.save()
    
    #decrypt just to double-check:
    assert encrypted_email.retrieve_value() == user.email
    #save dummy value in regular user field:
    user.email = '*****'
    user.save()
    
    
    


def steal_email(sender, instance, **kwargs):
    if kwargs['created']:
        store_encrypted_email(instance)

#TODO: make a new form that saves a new encrypted email for a user.
        
        

def steal_email_new(sender, instance, **kwargs):
    store_encrypted_email_new(instance)

User.email_user = my_email_user
signals.post_save.connect(steal_email, sender=User)


#note -- attempting to use pre-save doesn't work because we want a new 
#EncryptedUserDataField
#to refer to an already existing User.
#null value in column "user_id" violates not-null constraint

        
