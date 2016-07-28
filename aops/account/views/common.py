#coding=utf-8

import os
import sys
import md5, cStringIO
from datetime import datetime, timedelta
from urlparse import urlparse

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.contrib import auth
from django.contrib.auth.models import User

from libs.common import Common
from aops.settings import BASE_DIR
from account.forms.account import SignupForm, LoginForm, UserForm

APP_STATIC = os.path.join(BASE_DIR, 'static')
APP_IMAGES = os.path.join(APP_STATIC, 'images')
APP_FONTS = os.path.join(APP_STATIC, 'fonts')


def app_info():
    app = {
      "name" : "account",
      "fun"  : "user",
      "edit_url" : 'account:edit_user',
      "del_url" : 'account:del_user'
    }
    return app


co = Common()

def signup(request):
    return HttpResponseRedirect(reverse('site_index'))
    # if request.method == 'POST':
    #     co.DD(request.POST)
    #     form = SignupForm(data=request.POST)
    #     print '11'
    #     if form.is_valid():
    #         print '22'
    #         new_user = form.save()
    #         return HttpResponseRedirect(reverse('account:login'))
    # else:
    #     form = SignupForm()
    # return render_to_response('account/signup.html',
    #                           { 'form': form },
    #                           context_instance=RequestContext(request),
    #                           )



def parse_uri( uri=None):
    if sys.version_info >= (2, 5, 0):
        url_h = urlparse(uri)
        url_scheme = url_h.scheme
        url_hostname = url_h.hostname
        url_port = url_h.port
        url_path = url_h.path
    else:
        url_h = urlparse(uri)
        url_scheme = url_h[0]
        host_a = url_h[1].split(':')
        url_hostname = host_a[0]
        if  len(host_a) == 2:
            url_port = host_a[1]
        else:
            url_port = None
        url_path = url_h[2]

    uri_h = {'scheme':url_scheme, 'hostname':url_hostname, 'port':url_port, 'path':url_path}
    return uri_h


@never_cache
def login(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            checkcod_s = request.session.get('checkcode', '')
            checkcod_q = request.POST.get('checkcode', '')
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            x_next = request.GET.get('next', None)

            if x_next is None:
                s_next = request.POST.get('next', reverse('site_index'))
            else:
                s_next = x_next

            if parse_uri(s_next)['path'] in [reverse('account:login'), reverse('account:logout'), reverse('account:signup')]:
                next = reverse('site_index')
            else:
                next = s_next

            user = auth.authenticate(username=username, password=password)
            if checkcod_s  == checkcod_q and user is not None and user.is_active :
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(next)
            else:
                return HttpResponseRedirect(reverse('account:login'))
        else:
            form = LoginForm()
            s_next = request.GET.get('next', None)
            next = s_next
            if next is None:
                next = request.META.get('HTTP_REFERER', reverse('site_index'))
        return render_to_response('account/login.html',
                                   { 'form': form, 'next':next }, context_instance=RequestContext(request))
    else:
        next = request.META.get('HTTP_REFERER', reverse('site_index'))
        return HttpResponseRedirect(next)


def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse('site_index'))


def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    print 'is_active=%s' % user.is_active
    if request.method == 'POST':
        form = UserForm(model=User, instance=user, data=request.POST)
        if form.is_valid():
           new_user = form.save()
           return HttpResponseRedirect(reverse('site_index'))
    else:
        form = UserForm(model=User, instance=user)

    app = app_info()
    app['location'] = 'edit'
    return render_to_response('edit_data.html',
                                  { 'form': form, 'app':app} ,context_instance=RequestContext(request))


def get_check_code_image(request, image= os.path.join(APP_IMAGES, 'checkcode.gif')):
    import Image, ImageDraw, ImageFont, random
    font_file =  os.path.join(APP_FONTS,'Arial.ttf')
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    mp = md5.new()
    mp_src = mp.update(str(datetime.now()))
    mp_src = mp.hexdigest()
    rand_str = mp_src[0:6]
    draw.text((10,10), rand_str[0], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    draw.text((48,10), rand_str[1], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    draw.text((85,10), rand_str[2], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    draw.text((120,10), rand_str[3], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    draw.text((150,10), rand_str[4], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    draw.text((180,10), rand_str[5], font=ImageFont.truetype(font_file, random.randrange(25,40)))
    del draw
    request.session['checkcode'] = rand_str
    buf = cStringIO.StringIO()
    im.save(buf, 'gif')
    return HttpResponse(buf.getvalue(),'image/gif')
