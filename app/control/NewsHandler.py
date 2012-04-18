# *_* code: utf-8 *_*

from app.controller.Base import BaseHandler

class ShowNews(BaseHandler):
    def get(self, id):
        news = self.db.get("select news.id, news.title, news.content, news.postedat, news.commentnum, usr.name as author, category.name as category from news left join usr on news.author=usr.id left join category on news.categoryid=category.id where news.id=%s;" % id)
        if news:
            self.write(self.serve_template("news.html", **{'news':news}))
        else:
            self.write("get news fail. news id is %s." % id)
