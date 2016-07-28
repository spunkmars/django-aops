#coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.models.contacts import Contacts
from cmdb.forms.contacts import ContactsForm
from django.views.decorators.csrf import csrf_exempt
import json
from libs.models.common import del_model_data

def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "contacts",
      "edit_url" : 'cmdb:edit_contacts',
      "del_url" : 'cmdb:del_contacts'
    }
    return app

@csrf_exempt #禁用csrf
def add_contacts(request):
    if request.method == 'POST':
        form = ContactsForm(model=Contacts, data=request.POST)
        if form.is_valid():
            new_contacts = form.save()
            #print "url test: %s" % reverse('cmdb:index')
            return HttpResponseRedirect(reverse('cmdb:list_contacts'))
    else:
        form = ContactsForm(model=Contacts)
    
    app = app_info()
    app['location'] = 'add'
    return render_to_response('add_data.html', {'form': form, 'app':app} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def edit_contacts(request, contacts_id):
    contacts = get_object_or_404(Contacts, pk=contacts_id)
    if request.method == 'POST':
        form = ContactsForm(model=Contacts, instance=contacts, data=request.POST)
        if form.is_valid():
           new_contacts = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_contacts'))
    else:
        form = ContactsForm(model=Contacts, instance=contacts)

    app = app_info()
    app['location'] = 'edit'
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_contacts(request):

    model_object = Contacts
    template_file = 'list_data.html'
    show_field_list = [ 'name',
                        'job_titles',
                        'company',
                        'mail',
                        'im_num',
                        'mobile_phone']
    filter_field = 'name'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_contacts(request, contacts_id):
    del_res={}
    if request.method == "POST":
        del_res = del_model_data(model=Contacts, id=contacts_id)

    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


