# *_* coding: utf-8 *_*

from app.controller.Base import BaseHandler

class GetCategory(BaseHandler):
    def get(self, selected):
        category = self.db.query("select * from category where parentId = 0;")
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
    @admin
    def get(self):
        pass

    @admin
    def post(self):
        pass

class DelCategory(BaseHandler):
    @admin
    def get(self, id):
        pass

class EditCategory(BaseHandler):
    @admin
    def get(self, id):
        pass

    @admin
    def post(self, id):
        pass
