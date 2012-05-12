# *_* code: utf-8 *_*

from app.controller.Base import BaseHandler, admin
import time

class ShowNews(BaseHandler):
    def get(self, id):
        news = self.db.get("select news.id, news.title, news.content, news.postedat, news.commentnum, usr.name as author, category.name as category, news.doc as doc, news.categoryid from news left join usr on news.author=usr.id left join category on news.categoryid=category.id where news.id=%s;" % id)
        if news:
            news['content'] = self.DocParise(news['doc'], news['content'])
            self.write(self.serve_template("news.html", **{'news':news}))
        else:
            self.write("get news fail. news id is %s." % id)

class Preview(BaseHandler):
    @admin
    def post(self):
        doc = self.get_argument('doc', None)
        content = self.get_argument('content', None)
        self.write(self.DocParise(doc, content))

class AddNews(BaseHandler):
    @admin
    def get(self):
        category = self.db.query("select * from category where parentid=0;")
        self.write(self.serve_template("admin/addnews.html", **{'category': category, 'xsrf': self.xsrf_form_html()}))
        self.flush()

    @admin
    def post(self):
        title = self.get_argument('title', None)
        categoryid = self.get_argument('category', None)
        summary = self.get_argument('summary', None)
        content = self.get_argument('content', None)
        source = self.get_argument('source', None)
        doc = self.get_argument('doc', None)
        if self.db.execute_rowcount("insert into news(categoryid, title, content, source, author, postedat, commentnum, summary, doc) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);", *(categoryid, title, self.JsEscape(content), source, self.current_user['id'], time.ctime(), 0, self.JsEscape(summary), doc)):
            self.write('done')
        else:
            self.write('undone')
        self.flush()

class EditNews(BaseHandler):
   @admin
   def get(self, id):
       news = self.db.get("select * from news where id=%s;", *(id,))
       category = self.db.query("select * from category;")
       self.write(self.serve_template("admin/editNews.html", **{'news': news, 'category': category, 'xsrf':self.xsrf_form_html()}))
       
   @admin
   def post(self, id):
       title = self.get_argument('title', None)
       categoryid = self.get_argument('category', None)
       summary = self.get_argument('summary', None)
       content = self.get_argument('content', None)
       source = self.get_argument('source', None)
       doc = self.get_argument('doc', None)
       if self.db.execute_rowcount("update news set categoryid=%s, title=%s, content=%s, source=%s, summary=%s, doc=%s where id=%s;", *(categoryid, title, self.JsEscape(content), source, self.JsEscape(summary), doc, id)):
           self.write('done')
       else:
           self.write('undone')
       self.finish()

class DelNews(BaseHandler):
    @admin
    def get(self, id):
        self.db.execute("delete from comment where newsid=%s;", *(id,))
        if self.db.execute_rowcount("delete from news where id=%s;", *(id,)):
            self.write("done")
        else:
            self.write("undone")
        
class NewsList(BaseHandler):
    @admin
    def get(self, id):
        news = self.db.query("select news.id, usr.name as author, postedat, news.title from news left join usr on news.author=usr.id where categoryid=%s", *(id,))
        if news:
            response = ['<tr><td><a href="/news_{id}">{title}</a></td><td>{author}</td><td>{postedat}</td><td><a href="javascript: delNews({id});" class="delete">删除</a></td><td><a href="/~/editNews_{id}" class="edit">修改</a></td></tr>'.format(**n) for n in news]
            self.write(''.join(response))
        else:
            self.write('当前分类下没有任何新闻')
        self.finish()

class SearchNews(BaseHandler):
    def post(self):
        search = self.get_argument("search",None)
        news = self.db.query("select * from searchNews('search', %s);fetch all from search;", *(search,))
        self.write(self.serve_template("index.html", **{'newses': news, 'position': '搜索结果', 'xsrf': self.xsrf_form_html()}))

class AdminSearch(BaseHandler):
    @admin
    def post(self):
        keyword = self.get_argument("keyword", None)
        news = self.db.query("select * from searchNews('search', %s);fetch all from search;", *(keyword,))
        if news:
            response = ['''<tr><td><a href="/news_{id}"><strong>[{category}]</strong> {title}</a></td><td>{author}</td><td>{postedat}</td><td><a href="javascript: delNews({id});" class="delete">删除</a></td><td><a href="/~/editNews_{id}" class="edit">修改</a></td></tr>'''.format(**n) for n in news]
            self.write(''.join(response))
        else:
            self.write('该关键词无法搜索到任何新闻')
        self.flush()
