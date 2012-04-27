# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1335499967.176
_template_filename = 'app/view/admin/addnews.html'
_template_uri = 'admin/addnews.html'
_source_encoding = 'utf-8'
_exports = ['navigation', 'extra']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, 'base.html', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        category = context.get('category', UNDEFINED)
        def navigation():
            return render_navigation(context.locals_(__M_locals))
        def extra():
            return render_extra(context.locals_(__M_locals))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer('\r\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra'):
            context['self'].extra(**pageargs)
        

        # SOURCE LINE 6
        __M_writer('\r\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'navigation'):
            context['self'].navigation(**pageargs)
        

        # SOURCE LINE 13
        __M_writer('\r\n<div class="grid_16">\r\n  <h2>添加新闻</h2>\r\n</div>\r\n<form method="POST" action="/~/addNews">\r\n  <div class="grid_5">\r\n    <p>\r\n      <label for="title">标题<small>请为新闻设定一个合适的标题.</small></label>\r\n      <input type="text" name="title" />\r\n    </p>\r\n  </div>\r\n  <!--\r\n  <div class="grid_5">\r\n    <p>\r\n      <label for="title">Slug <small>Must contain alpha-numeric characters.</small></label>\r\n      <input type="text" name="title" />\r\n    </p>\r\n                                                \r\n  </div>\r\n  -->\r\n  <div class="grid_6">\r\n    <p>\r\n      <label for="title">新闻类别</label>\r\n      <select name="category">\r\n')
        # SOURCE LINE 37
        for c in category:
            # SOURCE LINE 38
            __M_writer('        <option value="')
            __M_writer(str(c['id']))
            __M_writer('">')
            __M_writer(str(c['name']))
            __M_writer('</option>\r\n')
            pass
        # SOURCE LINE 40
        __M_writer('      </select>\r\n    </p>\r\n  </div>\r\n  <div class="grid_16">\r\n    <p>\r\n      <label>新闻概要<small>将在新闻列表中显示.</small></label>\r\n      <textarea name="summary"></textarea>\r\n    </p>\r\n  </div>\r\n  <div class="grid_16">\r\n    <div id="dropbox">\r\n      <span class="message">请拖曳新闻图片到此处上传. <br /><i>可以预览</i></span>\r\n    </div>\r\n  </div>\r\n  <div class="grid_16">\r\n    <p>\r\n      <label>新闻内容<small>Markdown 语法.</small></label>\r\n      <textarea class="big"></textarea>\r\n    </p>\r\n    <p class="submit">\r\n      <input type="reset" value="重置" />\r\n      <input type="submit" value="发布新闻" />\r\n    </p>\r\n  </div>\r\n</div>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_navigation(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        def navigation():
            return render_navigation(context)
        __M_writer = context.writer()
        # SOURCE LINE 7
        __M_writer('\r\n<ul id="navigation">\r\n  <li><span class="active">Overview</span></li>\r\n  <li><a href="#">News</a></li>\r\n  <li><a href="#">Users</a></li>\r\n</ul>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_extra(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        def extra():
            return render_extra(context)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer('\r\n<link rel="stylesheet" href="../../static/stylesheets/admin-css/upload.css" type="text/css" media="screen" charset="utf-8" />\r\n<script src="../../static/javascripts/admin-js/upload.js" type="text/javascript"></script>\r\n<script src="../../static/javascripts/admin-js/jquery.filedrop.js" type="text/javascript"></script>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


