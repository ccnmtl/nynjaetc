from django.db.models import signals

#from 


#from nynjaetc.main.models import EncryptedUserDataField

def monkey_patch_user (user_class, eudf_class, eud_class):
    """Monkey patch user class. """
    user_class.original_email_user = user_class.email_user

    def get_real_email_address (user):
        assert user != None
        email_field = eudf_class.objects.get(slug='email')
        assert email_field != None
        try:
            email_data = eud_class.objects.get(user = user, which_field=email_field)
        except eud_class.DoesNotExist:
            return None
        assert email_data != None
        decrypted_email = email_data.retrieve_value()
        assert decrypted_email != None
        assert decrypted_email != ''
        return decrypted_email
    
    def my_email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User. If an encrypted email is available, use that one.
        """
        decrypted_email = get_real_email_address (self)
        if decrypted_email != None:
            self.email = decrypted_email
            #print "found a decrypted email; sending to %s" % self.email
            self.original_email_user(subject, message, from_email)
            self.email = '*****' # note -- this isn't stored.

        else:
            #print "found a regular email; sending to %s" % self.email
            self.original_email_user(subject, message, from_email)
        
        
    def new_store_encrypted_email (user):
        assert user != None
        assert user.email != None
        assert user.email != ''
        
        encrypted_email = EncryptedUserData()
        email_field = EncryptedUserDataField.objects.get(slug='email')
        assert email_field != None
        encrypted_email.which_field = email_field
        encrypted_email.user = user
        encrypted_email.store_value (user.email)
        encrypted_email.save()
        
        #decrypt just to double-check:
        assert encrypted_email.retrieve_value() == user.email
        #save dummy value in regular user field:
        user.email = '*****'
        user.save()

    def do_crazy_stuff(sender, instance, **kwargs):
        if kwargs['created']:
            #print "created -- encrypting %s's email and replacing the original w/ a dummy value." % instance
            if instance.email != '':
                new_store_encrypted_email(instance)
        
        else:
            #print "just a regular save"
            pass
            
    user_class.email_user = my_email_user
    #import pdb
    #pdb.set_trace()
    
    signals.post_save.connect(do_crazy_stuff, sender=user_class)

