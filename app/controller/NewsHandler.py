# *_* code: utf-8 *_*

from app.controller.Base import BaseHandler, admin
import time

class ShowNews(BaseHandler):
    def get(self, id):
        news = self.db.get("select news.id, news.title, news.content, news.postedat, news.commentnum, usr.name as author, category.name as category, news.categoryid from news left join usr on news.author=usr.id left join category on news.categoryid=category.id where news.id=%s;" % id)
        if news:
            news['content'] = self.markdown.convert(news['content'])
            self.write(self.serve_template("news.html", **{'news':news}))
        else:
            self.write("get news fail. news id is %s." % id)

class Preview(BaseHandler):
    @admin
    def post(self):
        content = self.get_argument('content', None)
        self.write(self.markdown.convert(content))

class AddNews(BaseHandler):
    @admin
    def get(self):
        category = self.db.query("select * from category where parentid=0;")
        self.write(self.serve_template("admin/addnews.html", **{'category': category, 'xsrf': self.xsrf_form_html()}))

    @admin
    def post(self):
        title = self.get_argument('title', None)
        categoryid = self.get_argument('category', None)
        summary = self.get_argument('summary', None)
        content = self.get_argument('content', None)
        source = self.get_argument('source', None)
        if self.db.execute_rowcount("insert into news(categoryid, title, content, source, author, postedat, commentnum) values(%s, %s, %s, %s, %s, %s, %s)", *(categoryid, title, content, source, self.current_user['id'], time.ctime(), 0)):
            self.write('done')
        else:
            self.write('undone')

class EditNews(BaseHandler):
   @admin
   def get(self, id):
       pass

   @admin
   def post(self, id):
       pass

class DelNews(BaseHandler):
    @admin
    def get(self, id):
        pass
