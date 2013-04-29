from django.db import models
from pagetree.models import Section
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import utc
from Crypto.Cipher import AES
import base64
from django.conf import settings

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
        block_length = 8 # the return value will be an integer multiple of this length
        bytes = bytearray (a_string.encode('utf-8'))
        prefixed_bytes = '%s,%s' % (len (bytes), bytes)
        padding = (len (prefixed_bytes) % block_length) * '#'
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
