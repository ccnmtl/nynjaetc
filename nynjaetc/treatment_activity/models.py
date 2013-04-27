from django.db import models
from django.contrib.contenttypes import generic
from pagetree.models import PageBlock
from django import forms


class TreatmentActivityBlock(models.Model):
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "treatment_activity/treatment_activity.html"
    js_template_file = "treatment_activity/block_js.html"
    css_template_file = "treatment_activity/block_css.html"
    display_name = "Response Guided Treatment Activity"

    def pageblock(self):
        return self.pageblocks.all()[0]

    def __unicode__(self):
        return unicode(self.pageblock())

    def needs_submit(self):
        return False

    @classmethod
    def add_form(self):
        return TreatmentActivityBlockForm()

    def edit_form(self):
        return TreatmentActivityBlockForm(instance=self)

    @classmethod
    def create(self, request):
        form = TreatmentActivityBlockForm(request.POST)
        return form.save()

    def edit(self, vals, files):
        form = TreatmentActivityBlockForm(data=vals,
                                     files=files,
                                     instance=self)
        if form.is_valid():
            form.save()

    def unlocked(self, user):
        '''
            This view is unlocked if:
        '''
        return True


class TreatmentActivityBlockForm(forms.ModelForm):
    class Meta:
        model = TreatmentActivityBlock
