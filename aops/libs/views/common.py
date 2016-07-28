#coding=utf-8

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from cmdb.models.common import get_model_all_field_objects, get_model_relate_field, get_model_valid_fields

from libs.common import Common
from libs.data_serialize import DataSerialize

def list_data(**kwargs):

    each_page_items = int( kwargs.get('each_page_items', 10) )
    show_field_list = kwargs.get('show_field_list', [])
    ex_field_list = kwargs.get('ex_field_list', [])
    request =  kwargs.get('request', {})
    page_nav_base_url = kwargs.get('page_nav_base_url', '')
    show_error_url = kwargs.get('show_error_url', '/')
    show_list_uri = kwargs.get('show_list_uri', [])
    nav_uri = kwargs.get('nav_uri', [])
    custom_get_parameter = kwargs.get('custom_get_parameter', {})
    filter_field = kwargs.get('filter_field', 'id')
    template_file = kwargs.get('template_file', '')
    model_object = kwargs.get('model_object', '')
    return_type = kwargs.get('return_type', 'render_to_response')
    app = kwargs.get('app', {})

    #show_field_list = get_model_all_field_objects(model=model_object)

    after_range_num = 5
    bevor_range_num = 4
    page = 1
    sort_by = ''
    url_prefix_base = ''
    url_sort_prefix = ''
    url_prefix = '?page='
    query=''
    if len(custom_get_parameter) < 1 and request.method == 'GET':

        try:
            page = int(request.GET.get("page",1))
            query = request.GET.get('q', '')
            sort_by = request.GET.get('sort_by', '')
            if page < 1:
                page = 1
        except ValueError:
            page = 1

    else:
        query = custom_get_parameter.get('query', [])
        sort_by = custom_get_parameter.get('sort_by', 'id')
        page = custom_get_parameter.get('page', 1)
        if page < 1:
            page = 1
    sorted_by = sort_by
    if  sort_by is not None and sort_by != '':
        url_sort_prefix = '?sort_by='
        url_prefix = "?page="
    else:
        sort_by = '-id'
        url_prefix_base = "?sort_by=%s" % sort_by
        url_sort_prefix =  "?sort_by="
        url_prefix = url_prefix_base + "&page="

    if query is None or query == '':
        if sorted_by is None or sorted_by == '':
            url_sort_prefix = '?sort_by='
            url_prefix = '?page='
        else:
            url_sort_prefix = '?sort_by='
            url_prefix = "?sort_by=%s&page=" % sort_by
        info = model_object.objects.order_by(sort_by).all()
    else:
        if sorted_by is None or sorted_by == '':
            url_prefix_base = "?q=%s" % query
            url_sort_prefix = url_prefix_base + '&sort_by='
            url_prefix = url_prefix_base + '&page='
        else:
            url_prefix_base = "?q=%s" % query
            url_sort_prefix = url_prefix_base + '&sort_by='
            url_prefix = url_prefix_base + "&sort_by=%s&page=" % sort_by

        info = model_object.objects.order_by(sort_by).filter(eval( "Q(%s__contains=\"%s\")" % (filter_field, query) ))
    paginator = Paginator(info, each_page_items)
    try:
        item_list = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        item_list = paginator.page(1)

    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]


    """可以返回三种类型数据： 
       1、 render_to_response 返回一个 Http Response 有http头部（比如Content-Type: xxx xxx)
       2、 render_to_string  只是返回内容的字符串形式，没有http头部（Content-Type: xxx xxx）
       3、 var     则只是返回 内容的变量（比如 locals）
    """

    if return_type == 'render_to_response':
        return render_to_response(template_file, locals(), context_instance=RequestContext(request))
    elif return_type == 'render_to_string':
        return render_to_string(template_file, locals())
    elif return_type == 'var':
        return locals()


def del_model_items( *args, **kwargs ):
    del_model = kwargs.get('del_model', None)
    del_items = kwargs.get('del_items', None)
    if del_items.find(',') != -1:
        mult_ids = []
        mult_ids = del_items.split(',')
        if mult_ids[0] == 'undefined':
            return False
        for p_id in mult_ids:
            del_model_instance = get_object_or_404(del_model, pk=p_id)
            if del_model_instance:
                del_model_instance.delete()
    else:
        del_model_instance = get_object_or_404(del_model, pk=del_items)
        if del_model_instance:
            del_model_instance.delete()


def display_confirm_msg( *args, **kwargs ):

    request = kwargs.get('request', None)
    http_referer = kwargs.get('http_referer', None)
    confirm_back_url = kwargs.get('confirm_back_url', http_referer) 
    confirm_msg = kwargs.get('confirm_msg', None)
    confirm_title = kwargs.get('confirm_title', None)
    #confirm_next_url = kwargs.get('confirm_next_url', "%s?confirm_result=yes&s_url=%s" % (request.path, http_referer) )
    confirm_next_url = kwargs.get('confirm_next_url', "%s?confirm_result=yes" % (request.path) )
    confirm_back_title = kwargs.get('confirm_back_title','Back')
    #logger2.info( "%s, %s, %s, %s, %s, %s" % (http_referer, confirm_back_url, confirm_msg, confirm_title, confirm_next_url, confirm_back_title) )
    return render_to_response('confirm_action.html',
                              { 'confirm_msg':confirm_msg, 'confirm_title':confirm_title, 'confirm_next_url':confirm_next_url, 'confirm_back_title':confirm_back_title, 'confirm_back_url':confirm_back_url }, context_instance=RequestContext(request))



def map_value(value="",map_list=()):
    res=''
    for x in map_list:
        try :
            value=int(value)
        except ValueError,e:
            value=value
        if x[0] == value:
            res= x[1]
    if not res:
        res="none"
    return res



class Ajax(Common):
    def __init__(self, *args, **kwargs):
        self.s_method = kwargs.get('s_method', ['GET', 'POST'])
        self.request = kwargs.get('request', None)
        self.original_data = kwargs.get('original_data', 'form')
        self.is_origin_serial = kwargs.get('is_origin_serial', False)
        ds = kwargs.get('ds', None)
        if isinstance(ds, DataSerialize):
            self.ds = ds
        else:
            self.ds = DataSerialize(format='json', ensure_ascii = False)

        self.error_m =  {'error_code':-1, 'error_msg':'Only support %s method!' % (','.join(self.s_method)),}
        self.response = HttpResponse('')
        self.response['Content-Type'] = "application/json; charset=utf-8"
        self.response['Vary'] = "Accept-Language"
        self.response_content = None

        self.callback(self, *args, **kwargs)


    def callback(self, *args, **kwargs):
        pass


    def load_data(self,content=None):
        self.response_content = content


    def get_ds_input_data(self):
        if self.request.method == 'POST':
            if self.original_data == 'form':
                self.in_data = self.request.POST
            else:
                self.in_data = self.request.body
        elif self.request.method == 'GET':
            self.in_data = self.request.GET
        else:
            self.in_data = {}
        #if self.is_origin_serial: #这里会产生错误。
        #   self.in_data=self.ds.deserialize('{"cc":1}')
        return self.in_data


    def make_response(self, *args, **kwargs):
        if self.request.method  in self.s_method:
            self.response.content = self.ds.serialize(self.response_content)
        else:
            self.response.content = self.ds.serialize(self.error_m)
        return self.response

