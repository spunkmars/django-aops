from django.conf.urls import patterns, include, url

from export.views import export_data


urlpatterns = patterns('',
        url(r'^$',export_data.index, name='index'),
        url(r'export/$',export_data.export, name='export'),
        url(r'get_model_field_list/$',export_data.get_model_field_list, name='get_model_field_list'),
)
