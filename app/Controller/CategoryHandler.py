# *_* coding: utf-8 *_*

from app.controller.Base import BaseHandler
printnum = lambda x: str(x) + 'st' if int(x)%10==1 else 'nd' if int(x)%10==2 else 'rd' if int(x)%10==3 else 'th'


class GetCategory(BaseHandler):
    def get(self):
        category = self.db.query("select * from category where parentId = 0;")
        html = ['<li><a class="nav" href="/category_{id}_1">{name}</a></li>'.format(**c) for c in category ]
        self.write(''.join(html))

class CategoryNews(BaseHandler):
    def get(self, id, page=1):
        pages = self.db.get("select count(*) from news where news.categoryid=%s;" % id)
        newses = self.db.query("select news.id, news.title, news.postedat, usr.name as author, category.name as category from news left join usr on news.author=usr.id left join category on news.categoryid=category.id where news.categoryid=%s order by news.postedat desc limit 20 offset %d;" % (id, (int(page) - 1) * 20))
        if newses:
            self.write(self.serve_template("newslist.html", **{'newses': newses, 'position': newses[0]['category'], 'pages': (int(pages['count']) + 20) // 20, 'page':page, 'category': id}))
        else:
            self.write("get {id} category and {page} page error.".format(**{'id': printnum(id), 'page': printnum(page)}))
