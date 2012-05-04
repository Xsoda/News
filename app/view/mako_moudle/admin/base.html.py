# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1335942252.444
_template_filename = 'app/view/admin/base.html'
_template_uri = 'admin/base.html'
_source_encoding = 'utf-8'
_exports = ['navigation', 'extra']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        def navigation():
            return render_navigation(context.locals_(__M_locals))
        def extra():
            return render_extra(context.locals_(__M_locals))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\r\n        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\r\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\r\n        <head>\r\n                <meta http-equiv="Content-type" content="text/html; charset=utf-8" />\r\n                <title>PPTM News 管理后台</title>\r\n                <link rel="stylesheet" href="../../static/stylesheets/admin-css/960.css" type="text/css" media="screen" charset="utf-8" />\r\n                <link rel="stylesheet" href="../../static/stylesheets/admin-css/template.css" type="text/css" media="screen" charset="utf-8" />\r\n                <link rel="stylesheet" href="../../static/stylesheets/admin-css/colour.css" type="text/css" media="screen" charset="utf-8" />\r\n                <!--[if IE]><![if gte IE 6]><![endif]-->\r\n                <script src="../../static/javascripts/admin-js/glow/1.7.0/core/core.js" type="text/javascript"></script>\r\n                <script src="../../static/javascripts/jquery-1.7.2.min.js" type="text/javascript"></script>\r\n                <script src="../../static/javascripts/admin-js/glow/1.7.0/widgets/widgets.js" type="text/javascript"></script>\r\n                <script src="../../static/javascripts/displayMessage.js" type="text/javascript"></script>\r\n                <link href="../../static/javascripts/admin-s/glow/1.7.0/widgets/widgets.css" type="text/css" rel="stylesheet" />\r\n                ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra'):
            context['self'].extra(**pageargs)
        

        # SOURCE LINE 16
        __M_writer('\r\n                <script type="text/javascript">\r\n                        glow.ready(function(){\r\n                                new glow.widgets.Sortable(\r\n                                        \'#content .grid_5, #content .grid_6\',\r\n                                        {\r\n                                                draggableOptions : {\r\n                                                        handle : \'h2\'\r\n                                                }\r\n                                        }\r\n                                );\r\n                        });\r\n                </script>\r\n                <!--[if IE]><![endif]><![endif]-->\r\n        </head>\r\n        <body>\r\n\r\n          <h1 id="head">PPTM News 管理后台</h1>\r\n          ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'navigation'):
            context['self'].navigation(**pageargs)
        

        # SOURCE LINE 34
        __M_writer('\r\n          <div id="content" class="container_16 clearfix">\r\n            ')
        # SOURCE LINE 36
        __M_writer(str(self.body()))
        __M_writer('\r\n          </div>\r\n        </body>\r\n</html>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_navigation(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        def navigation():
            return render_navigation(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        def extra():
            return render_extra(context)
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


