# *-* coding: utf-8 *-*
__author__ = 'Xsoda'

from mako.template import Template
from mako.lookup import TemplateLookup

mylookup = TemplateLookup(directories=['app/view'], module_directory='app/view/mako_modules', output_encoding='utf-8', encoding_errors='replace')

def serve_template(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs).decode('utf-8')
