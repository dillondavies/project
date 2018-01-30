"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from app.push_to_index import Command
import os
import base64
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from elasticsearch import NotFoundError
from io import BytesIO
from app.forms import FSCrawlerJobForm, ConferenceForm
from app.models import Conference
import pickle
import json

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'NSID IA LTF',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Conference paper search',
            'year':datetime.now().year,
        }
    )

def datasets(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/datasets.html',
        {
            'title':'datasets',
            'message':'View and Modify the datasets of the ElasticSearch',
            'year':datetime.now().year,
        }
    )



@csrf_exempt
def view(request):
    """Renders a document from the index."""
    assert isinstance(request, HttpRequest)
    i = request.GET.get('id')

    if i:

        try :
            res = Command.get_id(i)
            
        except NotFoundError as e:
            return HttpResponse('Document not found')
        
        if 'text/plain; charset=ISO-8859-1' in res['_source']['file']['content_type']:
            my_file = open(res['_source']['path']['real'], 'r')
            response = HttpResponse(my_file.read(), mimetype='text/plain; charset=ISO-8859-1')
            response['Content-Disposition'] = 'inline;filename=' + i + '.txt'
            return response
                
        elif 'application/pdf' in res['_source']['content']['content_type']:

                b64_encode = res['_source']['base64']        
                b64_decode = base64.b64decode(b64_encode)
                with BytesIO(b64_decode) as pdf:
                    response = HttpResponse(pdf.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'inline;filename='+i+'.pdf'
                    return response
                pdf.closed
           
        elif 'text/html' in res['_source']['content']['content_type']:
            return HttpResponse(base64.b64decode(res['_source']['base64']).decode('utf-8'))

        else :
            return HttpResponse('Document not pdf')
            


def search(request):
    """Renders the search page."""
    assert isinstance(request, HttpRequest)
    q = request.GET.get('q')
    if q:

        if q=='*':
            res = Command.match_all()
        else:
            res = Command.search(q)

        paperList = [doc for doc in res['hits']['hits']]

        for x in paperList:
            x['id'] = x.pop('_id')
            x['source'] = x.pop('_source')
            x['score'] = x.pop('_score')
            x['index'] = x.pop('_index')
            x['type'] = x.pop('_type')


        return render(
        request,
        'app/results.html',
        {
            'title':'Search',
            'message':'Conference paper search',
            'search_string': q,
            'year':datetime.now().year,
            'paperList' : paperList
        }
    )


    else :
        return render(
        request,
        'app/search.html',
        {
            'title':'Search',
            'message':'Conference paper search',
            'year':datetime.now().year,
        }
    )

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        # using myfile.read() results in _ingest determining 
        # 'content_type': 'application/octet-stream'
        # with content_length : 0 
        res = Command.ingest_doc(fs.path(filename))

        return render(request, 'app/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'indexed': res['created']
        })
    return render(request, 'app/simple_upload.html')

def conf_id(request):

    if request.method == 'POST':
        
        print(request.POST)
        print(request.POST.get('id'))

        
        conf_form = ConferenceForm(instance=Conference.objects.get(pk=int(request.POST.get('id'))))
    else: 
        conf_form = ConferenceForm()

    #return render(request, 'app/conf_id.html' ,{'conf_form': conf_form})
    return HttpResponse(conf_form.as_table())




def fs_upload(request):

    if request.method == 'POST':
        
        if 'conf-submit' in request.POST:

            conf_form = ConferenceForm(request.POST)
            if conf_form.is_valid():
                conf_instance = conf_form.save()

                fs_form = FSCrawlerJobForm(initial={'job_conference': conf_instance})
                conf_form = ConferenceForm(instance=conf_instance)
            else : 
                fs_form = FSCrawlerJobForm()
                conf_form = ConferenceForm()

            return render(request, 'app/fs_upload.html', 
                  {
                      'conf_form': conf_form,
                      'fs_form' : fs_form
                  })

        elif 'fs-submit' in request.POST:
            
            fs_form = FSCrawlerJobForm(request.POST)

            if fs_form.is_valid():

                print(fs_form.cleaned_data['job_dir'])
                print(fs_form.cleaned_data['job_name'])
                print(fs_form.cleaned_data['job_conference'])

                return HttpResponse(fs_form.cleaned_data['job_dir'])
            else:
                return HttpResponse('FS Form is not valid')

    else:
        fs_form = FSCrawlerJobForm()
        conf_form = ConferenceForm()
    
    return render(request, 'app/fs_upload.html', 
                  {
                      'conf_form': conf_form,
                      'fs_form' : fs_form
                  })

