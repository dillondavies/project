"""
Definition of models.
"""

from django.db import models
from app.fscrawler import FSCrawlerWrapper
import datetime
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

YEAR_CHOICES = []
for r in range(1980, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

# TODO: integrity constraints between year, from_date, to_date
class Conference(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=500)
    acronym = models.CharField(max_length=255, blank=True, null=True)
    year = models.IntegerField(_('year'), choices=YEAR_CHOICES, 
                               default=datetime.datetime.now().year, 
                               validators=[
                                    MaxValueValidator(datetime.datetime.now().year+2),
                                    MinValueValidator(1900)
                                ],
                               blank=True, null=True)
    from_date = models.DateField('from date', blank=True, null=True)
    to_date = models.DateField('to date', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(null=True, blank=True)
    def __unicode__(self):
        if self.acronym and self.year:
            return self.acronym + ' ' + str(self.year)
        return self.name
    def __str__(self):              # __unicode__ on Python 2
        if self.acronym and self.year:
            return self.acronym + ' ' + str(self.year)
        return self.name
    class Meta:
        ordering = ['from_date', 'name']

class Connection(models.Model):
    url = models.URLField(default='http://localhost:9200')


class Index(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

class Document(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    index = models.ForeignKey(Index, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=255)
    filename = models.CharField(max_length=255, blank=True, null=True)
    filedir = models.CharField(max_length=255, blank=True, null=True)
    created = models.BooleanField(default=False)
    result = models.CharField(max_length=255, blank=True, null=True)


class FSCrawlerJob(models.Model):
    job_name = models.CharField(max_length=255, default='')
    job_dir = models.CharField(max_length=500, default=r'//dsto/nsid/Task_data/Common/Resources/Conferences')
    job_conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    job_settings_file = models.FilePathField(default=FSCrawlerWrapper.CRAWLER_JOB_DIR)
    job_run = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    class Meta:
        ordering = ['job_name']
