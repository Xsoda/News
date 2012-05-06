# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1336324681.223
_template_filename = 'app/view/admin/user.html'
_template_uri = 'admin/user.html'
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
        int = context.get('int', UNDEFINED)
        userlist = context.get('userlist', UNDEFINED)
        def navigation():
            return render_navigation(context.locals_(__M_locals))
        def extra():
            return render_extra(context.locals_(__M_locals))
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer('\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'extra'):
            context['self'].extra(**pageargs)
        

        # SOURCE LINE 28
        __M_writer('\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'navigation'):
            context['self'].navigation(**pageargs)
        

        # SOURCE LINE 36
        __M_writer('\n                \n<div id="content" class="container_16 clearfix">\n  <div class="grid_4">\n    <p>\n      <label>用户名<small>数字和字母</small></label>\n      <input type="text" />\n    </p>\n  </div>\n  <div class="grid_5">\n    <p>\n      <label>电子邮件</label>\n      <input type="text" />\n    </p>\n  </div>\n  <!--\n  <div class="grid_5">\n    <p>\n      <label>Department</label>\n      <select>\n        <option>Development</option>\n        <option>Marketing</option>\n        <option>Design</option>\n        <option>IT</option>\n      </select>\n    </p>\n  </div>\n  -->\n  <div class="grid_2">\n    <p>\n      <label>&nbsp;</label>\n      <input type="submit" value="搜索" />\n    </p>\n  </div>\n  <div class="grid_16">\n    <table>\n      <thead>\n        <tr>\n          <th>用户名</th>\n          <th>电子邮件</th>\n          <th>用户权限</th>\n          <th colspan="2" width="20%">Actions</th>\n        </tr>\n      </thead>\n      <tfoot>\n        <tr>\n        </tr>\n      </tfoot>\n      <tbody>\n        ')
        # SOURCE LINE 85

        flag = True
                
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['flag'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 87
        __M_writer('\n')
        # SOURCE LINE 88
        for user in userlist:
            # SOURCE LINE 89
            if flag == True:
                # SOURCE LINE 90
                __M_writer('        <tr class="alt">\n')
                # SOURCE LINE 91
            else:
                # SOURCE LINE 92
                __M_writer('        <tr>\n')
                pass
            # SOURCE LINE 94
            __M_writer('          <td>')
            __M_writer(str(user['name']))
            __M_writer('</td>\n          <td>')
            # SOURCE LINE 95
            __M_writer(str(user['email']))
            __M_writer('</td>\n          <td>\n')
            # SOURCE LINE 97
            if int(user['grade']) == 0:
                # SOURCE LINE 98
                __M_writer('                 普通用户\n')
                # SOURCE LINE 99
            else:
                # SOURCE LINE 100
                __M_writer('                 管理员\n')
                pass
            # SOURCE LINE 102
            __M_writer('          </td>\n          <td><a class="fancybox edit" href="#userform" id="editUser_')
            # SOURCE LINE 103
            __M_writer(str(user['id']))
            __M_writer('" title="用户权限修改">编辑</a></td>\n          <td><a href="/~/delUser_')
            # SOURCE LINE 104
            __M_writer(str(user['id']))
            __M_writer('" class="delete">删除</a></td>\n        </tr>\n        ')
            # SOURCE LINE 106

            flag = ~flag
                    
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['flag'] if __M_key in __M_locals_builtin_stored]))
            # SOURCE LINE 108
            __M_writer('\n')
            pass
        # SOURCE LINE 110
        __M_writer('        </tbody>\n      </table>\n    </div>\n  </div>\n\n<div id="foot">\n  <a href="#">Contact Me</a>\n</div>\n<div style="display:none" id="userform"><div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_navigation(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        def navigation():
            return render_navigation(context)
        __M_writer = context.writer()
        # SOURCE LINE 30
        __M_writer('\n<ul id="navigation">\n  <li><a href="/~/">新闻管理</a></li>\n  <li><span class="active">用户管理</span></li>\n  <li><a href="/~/category">分类管理</a></li>\n</ul>\n')
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
        __M_writer('\n<script src="../../static/javascripts/jquery.fancybox.js" type="text/javascript"></script>\n<script src="../../static/javascripts/ajax.js" type="text/javascript"></script>\n<link rel="stylesheet" type="text/css" href="../../static/stylesheets/jquery.fancybox.css" media="screen" />\n<script type="text/javascript">\n  $(document).ready(function(){\n      $(\'.fancybox\').fancybox();\n  $(\'.fancybox\').live("click", function(){\n  var id=$(this).attr("id");\n  var url = "/~/" + id;\n  $.get(url, function(response) {\n  $("#userform").html(response);\n  });\n  });\n  $("#editform").live("submit", function(){editUser($(this));return false;});\n\n   });\n  function editUser(form) {\n  var args=form.formToDict();\n  alert(form.attr("action"));\n  $.postJSON(form.attr("action"), args, function(response){\n  if(response=="done"){displayMessage("用户权限修改成功");}\n  else{displayMessage("用户权限修改失败");}\n  });\n  }\n</script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


