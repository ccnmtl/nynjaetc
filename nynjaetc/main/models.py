from django.db import models
from pagetree.models import Section
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import utc

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
    
    
class EncryptedUserData(models.Model):
    """A chunk of private, encrypted data associated with a user."""
    def __unicode__(self):
        return self.field.slug

    which_field = models.ForeignKey(EncryptedUserDataField, null=False, blank=False)
    user = models.ForeignKey(User,blank=False,null=False)
    value = models.TextField(blank=True, help_text = "Value of the data")
    
    unique_together = ("user", "which_field")
    def store_value (self, the_value):
        self.value = the_value
        self.save()
        
    def retrieve_value (self):
        return self.value
