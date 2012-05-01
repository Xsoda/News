# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 7
_modified_time = 1335885144.39
_template_filename = 'app/view/admin/user.html'
_template_uri = 'admin/user.html'
_source_encoding = 'utf-8'
_exports = ['navigation']


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
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer('\r\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'navigation'):
            context['self'].navigation(**pageargs)
        

        # SOURCE LINE 7
        __M_writer('\r\n                \r\n<div id="content" class="container_16 clearfix">\r\n  <div class="grid_4">\r\n    <p>\r\n      <label>用户名<small>数字和字母</small></label>\r\n      <input type="text" />\r\n    </p>\r\n  </div>\r\n  <div class="grid_5">\r\n    <p>\r\n      <label>电子邮件</label>\r\n      <input type="text" />\r\n    </p>\r\n  </div>\r\n  <!--\r\n  <div class="grid_5">\r\n    <p>\r\n      <label>Department</label>\r\n      <select>\r\n        <option>Development</option>\r\n        <option>Marketing</option>\r\n        <option>Design</option>\r\n        <option>IT</option>\r\n      </select>\r\n    </p>\r\n  </div>\r\n  -->\r\n  <div class="grid_2">\r\n    <p>\r\n      <label>&nbsp;</label>\r\n      <input type="submit" value="搜索" />\r\n    </p>\r\n  </div>\r\n  <div class="grid_16">\r\n    <table>\r\n      <thead>\r\n        <tr>\r\n          <th>用户名</th>\r\n          <th>电子邮件</th>\r\n          <th>用户权限</th>\r\n          <th colspan="2" width="10%">Actions</th>\r\n        </tr>\r\n      </thead>\r\n      <tfoot>\r\n        <tr>\r\n          <td colspan="5" class="pagination">\r\n            <span class="active curved">1</span><a href="#" class="curved">2</a><a href="#" class="curved">3</a><a href="#" class="curved">4</a> ... <a href="#" class="curved">10 million</a>\r\n          </td>\r\n        </tr>\r\n      </tfoot>\r\n      <tbody>\r\n        ')
        # SOURCE LINE 59

        flag = True
                
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['flag'] if __M_key in __M_locals_builtin_stored]))
        # SOURCE LINE 61
        __M_writer('\r\n')
        # SOURCE LINE 62
        for user in userlist:
            # SOURCE LINE 63
            if flag == True:
                # SOURCE LINE 64
                __M_writer('        <tr class="alt">\r\n')
                # SOURCE LINE 65
            else:
                # SOURCE LINE 66
                __M_writer('        <tr>\r\n')
                pass
            # SOURCE LINE 68
            __M_writer('          <td>')
            __M_writer(str(user['name']))
            __M_writer('</td>\r\n          <td>')
            # SOURCE LINE 69
            __M_writer(str(user['email']))
            __M_writer('</td>\r\n          <td>\r\n')
            # SOURCE LINE 71
            if int(user['grade']) == 0:
                # SOURCE LINE 72
                __M_writer('                 普通用户\r\n')
                # SOURCE LINE 73
            else:
                # SOURCE LINE 74
                __M_writer('                 管理员\r\n')
                pass
            # SOURCE LINE 76
            __M_writer('          </td>\r\n          <td><a href="#" class="edit">Edit</a></td>\r\n          <td><a href="/~/deluser_')
            # SOURCE LINE 78
            __M_writer(str(user['id']))
            __M_writer('" class="delete">Delete</a></td>\r\n        </tr>\r\n        ')
            # SOURCE LINE 80

            flag = ~flag
                    
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['flag'] if __M_key in __M_locals_builtin_stored]))
            # SOURCE LINE 82
            __M_writer('\r\n')
            pass
        # SOURCE LINE 84
        __M_writer('        </tbody>\r\n      </table>\r\n    </div>\r\n  </div>\r\n\r\n<div id="foot">\r\n  <a href="#">Contact Me</a>\r\n</div>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_navigation(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        def navigation():
            return render_navigation(context)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer('\r\n<ul id="navigation">\r\n  <li><a href="#">新闻管理</a></li>\r\n  <li><span class="active">用户管理</span></li>\r\n</ul>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


