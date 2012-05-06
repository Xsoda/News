# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1336302257.726
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
        xsrf = context.get('xsrf', UNDEFINED)
        def navigation():
            return render_navigation(context.locals_(__M_locals))
        def extra():
            return render_extra(context.locals_(__M_locals))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer('\r\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra'):
            context['self'].extra(**pageargs)
        

        # SOURCE LINE 77
        __M_writer('\r\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'navigation'):
            context['self'].navigation(**pageargs)
        

        # SOURCE LINE 83
        __M_writer('\r\n<div class="grid_16">\r\n  <h2>添加新闻</h2>\r\n</div>\r\n<form method="POST" action="/~/addNews" id="newsform">\r\n  <div class="grid_5">\r\n    <p>\r\n      <label for="title">标题<small>请为新闻设定一个合适的标题.</small></label>\r\n      <input type="text" name="title" />\r\n    </p>\r\n  </div>\r\n  <div class="grid_5">\r\n    <p>\r\n      <label for="title">新闻来源<small></small></label>\r\n      <input type="text" name="source" />\r\n    </p>\r\n                                                \r\n  </div>\r\n  <div class="grid_6">\r\n    <p>\r\n      <label for="title">新闻类别</label>\r\n      <select name="category">\r\n')
        # SOURCE LINE 105
        for c in category:
            # SOURCE LINE 106
            __M_writer('        <option value="')
            __M_writer(str(c['id']))
            __M_writer('">')
            __M_writer(str(c['name']))
            __M_writer('</option>\r\n')
            pass
        # SOURCE LINE 108
        __M_writer('      </select>\r\n    </p>\r\n  </div>\r\n  <div class="grid_16">\r\n    <p>\r\n      <label>新闻概要<small>将在新闻列表中显示.</small></label>\r\n      <textarea name="summary"></textarea>\r\n    </p>\r\n  </div>\r\n  <div class="grid_3" id="dropbox">\r\n      <p>请将图片拖到此处上传</p>\r\n  </div>\r\n  <div class="grid_12" id="preview">\r\n </div>\r\n  <div class="grid_16">\r\n    <p>\r\n      <label>新闻内容<small>Markdown 语法.</small></label>\r\n      <textarea name="content" class="big"></textarea>\r\n    </p>\r\n    <p class="submit">\r\n      ')
        # SOURCE LINE 128
        __M_writer(str(xsrf))
        __M_writer('\r\n      <input type="reset" value="重置" />\r\n      <input type="submit" value="发布新闻" />\r\n      <a class="fancybox" href="#inline" title="新闻预览" id="newspreview">预览</a>\r\n    </p>\r\n  </div>\r\n</div>\r\n<div id="inline" style="width:800px;display: none;">\r\n</div>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_navigation(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        def navigation():
            return render_navigation(context)
        __M_writer = context.writer()
        # SOURCE LINE 78
        __M_writer('\r\n<ul id="navigation">\r\n  <li><a href="/~/" class="active">新闻管理</a></li>\r\n  <li><a href="/~/user">用户管理</a></li>\r\n</ul>\r\n')
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
        __M_writer('\r\n<script src="../../static/javascripts/admin-js/ajaxupload.js" type="text/javascript"></script>\r\n<script src="../../static/javascripts/jquery.fancybox.js" type="text/javascript"></script>\r\n<script src="../../static/javascripts/ajax.js" type="text/javascript"></script>\r\n<link rel="stylesheet" type="text/css" href="../../static/stylesheets/jquery.fancybox.css" media="screen" />\r\n<style type="text/css">\r\n#preview{\r\n        float:right;\r\n        width: 100%;\r\n        height: 120px;\r\n        border: 3px dashed silver;\r\n}\r\n#preview li{\r\n        margin-top:10px;\r\n}\r\n#preview img{\r\n        width:100px;\r\n        height:100px;\r\n        border:1px soild #ccc;}\r\n#dropbox{\r\n        width: 100%;\r\n        font-size:10px;\r\n        margin-bottom: 10px;\r\n        line-height:15px;\r\n        height:120px;\r\n        border:3px dashed silver;\r\n        font-weight:bold;\r\n}\r\n</style>\r\n<script type="text/javascript">\r\n  function addNews(form) {\r\n  var args = form.formToDict($("#newsform"));\r\n  $.postJSON($("#newsform").attr("action"), args, function(response){\r\n  if(response==\'done\'){displayMessage("新闻添加成功");}\r\n  else{dispalyMessage("新闻添加失败");}\r\n  });\r\n  }\r\n  $(document).ready(function(){\r\n  $(\'.fancybox\').fancybox();\r\n  $(\'#newsform\').live("submit", function(){\r\n  addNews($(this));\r\n  return false;\r\n  });\r\n       var button = $(\'#dropbox\'), interval;\r\n       new AjaxUpload(button, {\r\n            action: \'/data/imgpost\', \r\n            name: \'myfile\',\r\n            onSubmit : function(file, ext){\r\n            button.text(\'正在上传\');                                                           \r\n            this.disable();\r\n            interval = window.setInterval(function(){\r\n                var text = button.text();\r\n                if (text.length < 13){\r\n                    button.text(text + \'.\');                                    \r\n                } else {\r\n                    button.text(\'正在上传\');                           \r\n                }\r\n           }, 200);\r\n           },\r\n           onComplete: function(file, response){\r\n                                button.text(\'请将图片拖到此处上传\');                                                  \r\n                                window.clearInterval(interval);\r\n                                this.enable();\r\n                                $("#preview").append(\'<div><img height="50" src="\' + response +\'">\'+ response + \'</div>\');                                           \r\n                        }\r\n                });\r\n                                  $("#newspreview").live(\'click\', function() {\r\n                                  var args=$("#newsform").formToDict();\r\n                                  $.postJSON("/~/preview", args, function(response) {\r\n                                  $("#inline").empty();\r\n                                  $("#inline").append(response);\r\n                                  })\r\n                                  });\r\n  });\r\n</script>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


