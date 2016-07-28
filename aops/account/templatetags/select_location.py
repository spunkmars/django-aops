from django import template
from datetime import datetime

register = template.Library()
def select_filter(value,arg=None):
    location=arg.strip('/').split('/')
    if not value or not location:
       return ""

    v = []
    if 'origin_location' in value:
        v = value['origin_location'].strip('/').split('/')
    else:
        v = [value['name'],value['fun'],value['location']]
    for i in range(len(location)):
        if v[i] != location[i] :
           return ""
    return "active"
    
register.filter('select', select_filter)
