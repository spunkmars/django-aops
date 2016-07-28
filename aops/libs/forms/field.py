# -*- coding:utf-8 -*-

from itertools import chain

from django.core.urlresolvers import reverse
from django.forms import Select
from django.utils.encoding import  force_unicode
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.forms.utils import flatatt, to_current_timezone
from django.utils.html import escape, conditional_escape, format_html
from django import forms
from django.conf import settings
from django.contrib.admin.templatetags.admin_static import static
from django.utils.translation import ugettext
from django.utils.safestring import mark_safe
from django.forms.widgets import TextInput

from libs.common import Common
from libs.data_serialize import DataSerialize

co = Common()


class newSelect(Select):

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select{0}>', flatatt(final_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</select>')
        if hasattr(self, 'd_class') and hasattr(self.d_class, 'get_add_url'):
            related_url = self.d_class.get_add_url()
            url_params = '?_to_field=id'
            output.append('<a href="%s%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> '
                          % (related_url, url_params, name))
            output.append('<img src="%s" width="10" height="10" alt="%s"/></a>'
                          % (static('admin/img/icon_addlink.gif'), ugettext('Add Another')))
        return mark_safe('\n'.join(output))


#class TreeSelect(Select):
class TreeSelect(newSelect):
    def __init__(self, d_class=None, attrs=None, choices=()):
        self.d_class = d_class
        #super(TreeSelect, self).__init__(attrs=attrs, choices=choices)
        super(TreeSelect, self).__init__(attrs)


    def fill_topic_tree(self, deep = 0, parent_id = 0, choices = []):
        if parent_id == 0:
            ts = self.d_class.objects.filter(parent = None)
            choices[0] += (('', '-------'),)
            for t in ts:
                tmp = [()]
                self.fill_topic_tree(4, t.id, tmp)
                choices[0] += ((t.id, ' ' * deep + t.title,),)
                for tt in tmp[0]:
                    choices[0] += (tt,)
        else:
            ts = self.d_class.objects.filter(parent__id = parent_id)
            for t in ts:
                choices[0] += ((t.id,' ' * deep + t.title, ),)
                self.fill_topic_tree(deep + 4, t.id, choices)


    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        if option_value in selected_choices:
            selected_html = u' selected="selected"'
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return u'<option value="%s"%s>%s</option>' % (
            escape(option_value), selected_html,
            conditional_escape(force_unicode(option_label)).replace(' ', '&nbsp'))


    def render_options(self, choices, selected_choices):
        ch = [()]
        self.fill_topic_tree(choices = ch)
        self.choices = ch[0]
        output = []
        choi = None
        if hasattr(self, 's_choices'): #newModelForm hack
            choi = chain(self.choices)
            if isinstance(selected_choices, (list, tuple)):
                selected_choices.extend(self.s_choices)
            else:
                selected_choices = self.s_choices
        else:
            choi = chain(self.choices, choices)

        selected_choices = set(force_unicode(v) for v in selected_choices)

        #for option_value, option_label in chain(self.choices, choices):
        for option_value, option_label in choi:
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)).replace(' ', '&nbsp'))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)




class newDateTimeInput(TextInput):

    def __init__(self, attrs=None, d_type='normal'):
        self.d_type = d_type
        super(newDateTimeInput, self).__init__(attrs)


    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        if self.d_type == 'normal':
            v_str = 'SelectDate(this,\'%s\')' % 'yyyy-MM-dd hh:mm:ss'
        elif self.d_type == 'onlydate':
            v_str = 'SelectDate(this,\'%s\')' % 'yyyy-MM-dd'
        else:
            v_str = 'SelectDate(this,\'%s\')' % self.d_type
        final_attrs['onclick'] = force_text(v_str)
        return format_html('<input{0} />', flatatt(final_attrs))



class AutoGetVal(TextInput):

    def __init__(self, attrs=None, g_url=None, d_type=None):
        self.d_type = d_type
        self.g_url = g_url
        super(AutoGetVal, self).__init__(attrs)


    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        js_str1 = 'getAutoVal(\'%s\', \'%s\', \'%s\');' % (final_attrs['id'], reverse(self.g_url), self.d_type)
        js_str = '<a onclick="javascript:%s" title="Get Val"><i class="fa fa-plus-square-o fa-fw"></i></a>' % js_str1
        return format_html('<input{0} />%s' % js_str, flatatt(final_attrs))