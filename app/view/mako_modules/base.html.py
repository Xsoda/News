# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1333701160.942
_template_filename = 'app/view/base.html'
_template_uri = 'base.html'
_source_encoding = 'ascii'
_exports = ['body', 'header', 'title']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def body():
            return render_body(context.locals_(__M_locals))
        def header():
            return render_header(context.locals_(__M_locals))
        def title():
            return render_title(context.locals_(__M_locals))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\r\n<html xmlns="http://www.w3.org/1999/xhtml">\r\n  <head>\r\n    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />\r\n    <title>')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 5
        __M_writer('</title>\r\n    <link rel="stylesheet" href="../static/stylesheets/main.css" type="text/css" />\r\n    <script type="text/javascript" src="../static/javascript/jquery-1.7.1.min.js"></script>\r\n  </head>\r\n  <body>\r\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'header'):
            context['self'].header(**pageargs)
        

        # SOURCE LINE 10
        __M_writer('\r\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'body'):
            context['self'].body(**pageargs)
        

        # SOURCE LINE 11
        __M_writer('\r\n    <div id="footer">\r\n      "Powered by Xsoda"\r\n    </div>\r\n  </body>\r\n</html>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        def body():
            return render_body(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        def header():
            return render_header(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        def title():
            return render_title(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


