#coding=utf-8
from django import template
from django.core.urlresolvers import reverse

from django.shortcuts import render_to_response, get_object_or_404

register = template.Library()

def do_get_sort_by_url(parser, token):

    try:
        tag_name, current_sort_by, target_sort_by = token.split_contents()
    except:
        raise template.TemplateSyntaxError, "%r tags error" % token.split_contents[0]

    #另一种取得模板变量值方法 步骤1
    #current_sort_by = parser.compile_filter(current_sort_by)
    #target_sort_by = parser.compile_filter(target_sort_by)

    #logger2.info("hhh%shhh, vvv%svvv,  ddd%sddd" % (tag_name, current_sort_by, target_sort_by) )


    return SortNode(current_sort_by, target_sort_by)


class SortNode(template.Node):

    def __init__(self, current_sort_by, target_sort_by):
        #另一种取得模板变量值方法 步骤2
        #self.current_sort_by = current_sort_by
        #self.target_sort_by = target_sort_by
        self.current_sort_by = template.Variable(current_sort_by)
        self.target_sort_by = template.Variable(target_sort_by)

    def render(self, context):

        #另一种取得模板变量值方法 步骤3
        #sort_by = self.current_sort_by.resolve(context, True)
        #target_sort_by = self.target_sort_by.resolve(context, True)

        sort_by = self.current_sort_by.resolve(context)
        target_sort_by = self.target_sort_by.resolve(context)
        if  (sort_by == target_sort_by):
            output_sort_by = '-' + target_sort_by
        else:
            output_sort_by = target_sort_by

        return output_sort_by


register.tag('get_sort_by_url', do_get_sort_by_url)
