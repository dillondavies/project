"""
Definition of forms.
"""

from django import forms
from app.models import FSCrawlerJob, Conference
from django.contrib.auth.forms import *
from django.utils.translation import ugettext_lazy as _


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class FSCrawlerJobForm(forms.ModelForm):
    class Meta:
        model = FSCrawlerJob
        fields = ['job_name', 'job_dir', 
                  'job_conference']
    def __init__(self, *args, **kwds):
        job_conference = kwds.pop('job_conference','')
        super(FSCrawlerJobForm, self).__init__(*args, **kwds)
        self.fields['job_conference']=forms.ModelChoiceField(queryset=Conference.objects.all())

class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = '__all__'
        # TODO: needs date range constraints on datepicker for integrity constraints
        widgets = {
            'from_date': forms.DateInput(attrs={'class':'datepicker'}),
            'to_date': forms.DateInput(attrs={'class':'datepicker'}),
        }
