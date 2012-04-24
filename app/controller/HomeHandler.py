# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler

class HomeHandler(BaseHandler):
    def get(self):
        print(self.session)
        print(self.get_current_user())
        newses = self.db.query("select news.id, news.title, news.postedat, news.commentnum, category.name as category, usr.name as author from news left join usr on news.author=usr.id left join category on news.categoryid=category.id order by news.postedat desc limit 20 offset 0;")
        self.write(self.serve_template("index.html", **{'position': '最新新闻', 'newses': newses}))

