# *_* coding: utf-8 *_*

from app.controller.Base import BaseHandler
from app.controller.Base import authenticated

class GetCategory(BaseHandler):
    def get(self, selected):
        category = self.db.query("select * from category where parentId = 0 order by id asc;")
        html = []
        html.append('<ul class="menu_tabbed">')
        for c in category:
            if int(c['id']) == int(selected):
                html.append('<li><a href="/category_{id}_1" class="selected">{name}</a></li>'.format(**c))
            else:
                html.append('<li><a href="/category_{id}_1">{name}</a></li>'.format(**c))
        html.append('</ul>')
        self.write(''.join(html))

class CategoryNews(BaseHandler):
    def get(self, id, pageth=1):
        pages = self.db.get("select count(*) from news where news.categoryid=%s;" % id)
        category = self.db.get("select name from category where id=%s;" % id)
        newses = self.db.query("select news.id, news.title, news.postedat, news.commentnum, usr.name as author, category.name as category from news left join usr on news.author=usr.id left join category on news.categoryid=category.id where news.categoryid=%s order by news.postedat desc limit 20 offset %d;" % (id, (int(pageth) - 1) * 20))
        if newses:
            self.write(self.serve_template("newslist.html", **{'newses': newses, 'position': newses[0]['category'], 'pages': int(pages['count']), 'page':pageth, 'categoryid': id}))
        else:
            self.write(self.serve_template("newslist.html", **{'newses': None, 'position': category['name'], 'newses': None, 'pages': None, 'page': None, 'categoryid': id}))

class AddCategory(BaseHandler):
    @authenticated("admin")
    def post(self):
        name = self.get_argument("category_name", None)
        if name:
            if self.db.execute_rowcount("insert into category(name, parentid) values(%s, %s);", *(name, 0)):
                self.write("done")
            else:
                self.write("undone")
        else:
            self.write("undone")
            
class DelCategory(BaseHandler):
    @authenticated("admin")
    def get(self, id):
        self.db.execute("select * from delCategory(%s);", *(id,))
        self.write("done")
    
class EditCategory(BaseHandler):
    @authenticated("admin")
    def get(self, id):
        category = self.db.get("select * from category where id=%s;", *(id,))
        category['xsrf'] = self.xsrf_form_html()
        html = '''
        <form method="post" id="editcategory" action="/~/editCategory_{id}">
          <table>
            <tr><td>分类名称:</td><td><input type="text" name="category_name" value="{name}"/></input></td></tr>
            <tr><td>{xsrf}
            <input type="hidden" value="{id}" name="category_id" />
            </td><td><input type="submit" value="确认修改" /></td></tr>
          </table>
        </form>
        '''.format(**category)
        self.write(html)
        
    @authenticated("admin")
    def post(self, id):
        category_id = self.get_argument("category_id")
        category_name = self.get_argument("category_name")
        if category_name and self.db.execute_rowcount("update category set name=%s where id=%s;", *(category_name, category_id)):
            self.write("done")
        else:
            self.write("undone")
            
class AdminCategory(BaseHandler):
    @authenticated("admin")
    def get(self):
        category = self.db.query("select * from category order by id asc;")
        self.write(self.serve_template("admin/category.html", **{'category': category, 'xsrf': self.xsrf_form_html()}))
