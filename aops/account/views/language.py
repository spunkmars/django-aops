#coding=utf-8
from datetime import datetime, timedelta
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import check_for_language
from django.utils.translation import get_language
from django.conf.global_settings import LANGUAGE_COOKIE_NAME
from aops.settings import LANGUAGES, LANGUAGE_CODE
import json

#@csrf_exempt
def select_language(request):
    data={}
    if request.method == 'POST':
        lang_code = request.POST.get('language', None)
        if lang_code and check_for_language(lang_code):
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            max_age =  60*60*24*365
            expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")

            data = { 'cookie_name' : LANGUAGE_COOKIE_NAME,
                     'lang_code' : lang_code,
                     'max_age' : max_age,
                     'expires' : expires }
    html = json.dumps(data)
    return HttpResponse(html, content_type="text/HTML")


#@csrf_exempt
def list_language(request):
    lang_dict={}
    for lang_k in LANGUAGES:
       lang_dict[lang_k[0]] = lang_k[1] 

    #lang_code = request.session.get('django_language',LANGUAGE_CODE)
    lang_code = get_language()
    html=json.dumps([lang_dict,lang_code])
    return HttpResponse(html, content_type="text/HTML")

