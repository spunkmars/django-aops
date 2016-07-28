#coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q

from libs.views.common import list_data, del_model_items, display_confirm_msg

from cmdb.models.cabinet_seat import CabinetSeat
from cmdb.forms.cabinet_seat import CabinetSeatForm
from django.views.decorators.csrf import csrf_exempt
import json
from libs.models.common import del_model_data

def app_info():
    app = {
      "name" : "cmdb",
      "fun"  : "cabinet_seat",
      "edit_url" : 'cmdb:edit_cabinet_seat',
      "del_url" : 'cmdb:del_cabinet_seat'
    }
    return app

@csrf_exempt #禁用csrf
def add_cabinet_seat(request):
    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST.update({
            'status':1,
        })
        form = CabinetSeatForm(model=CabinetSeat, data=request.POST)
        if form.is_valid():
            new_cabinet_seat = form.save()
            return HttpResponseRedirect(reverse('cmdb:list_cabinet_seat'))
    else:
        form = CabinetSeatForm(model=CabinetSeat)
    app = app_info()
    app['location'] = 'add'
    return render_to_response('add_data.html', {'form': form, 'app':app} ,context_instance=RequestContext(request))


@csrf_exempt #禁用csrf
def edit_cabinet_seat(request, cabinet_seat_id):
    cabinet_seat = get_object_or_404(CabinetSeat, pk=cabinet_seat_id)
    if request.method == 'POST':
        form = CabinetSeatForm(model=CabinetSeat, instance=cabinet_seat, data=request.POST)
        if form.is_valid():
           new_cabinet_seat = form.save()
           return HttpResponseRedirect(reverse('cmdb:list_cabinet_seat'))
    else:
        form = CabinetSeatForm(model=CabinetSeat, instance=cabinet_seat)

    app = app_info()
    app['location'] = 'edit'
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app} ,context_instance=RequestContext(request))

@csrf_exempt #禁用csrf
def list_cabinet_seat(request):
    model_object = CabinetSeat
    template_file = 'list_data.html'
    show_field_list = [ 'cabinet',
                        'cabinet_seat_location',
                         'status']
    filter_field = 'cabinet_seat_location'
    each_page_items = 10
    custom_get_parameter = {}
    app = app_info()
    app['location'] = 'list'

    render_context = list_data(app=app, request=request,  model_object=model_object, each_page_items = each_page_items, filter_field = filter_field, template_file = template_file, show_field_list = show_field_list)
    return render_context


@csrf_exempt #禁用csrf
def del_cabinet_seat(request, cabinet_seat_id):
    del_res={}
    if request.method == "POST":
        del_res = del_model_data(model=CabinetSeat, id=cabinet_seat_id)

    html=json.dumps(del_res)
    return HttpResponse(html, content_type="text/HTML")


