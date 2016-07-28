from django import template
from datetime import datetime
register = template.Library()
def date_filter(value,arg=None):
    t = value[:19]
    if not t:
       return 
    try :
        deal_time = datetime.strptime(t,'%Y-%m-%dT%H:%M:%S.%f')
    except ValueError ,e :
        deal_time = datetime.strptime(t,'%Y-%m-%dT%H:%M:%S')
    
    res_time = deal_time.strftime('%Y-%m-%d/%H:%M:%S')
    return res_time
register.filter('deal_time', date_filter)
