# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler, authenticated, admin
import time
from core.web.helpers import Gravatar
gravatar = Gravatar(size=140, rating='g', default=None, force_default=False, force_lower=True)

class GetComments(BaseHandler):
    # `<div id="commentHolder">
    # `  ..............
    # `  <div class="comment">
    # `    <p class="title">
    # `        <span>{comment time}</span>
    # `             {comment author}
    # `    </p>
    # `----------------------------------------
    # `    <div>
    # `      <div>****</div>
    # `      <span>{comment author}</span>
    # `      <br />
    # `         {comment content}
    # `    </div>
    # `----------------------------------------
    # `    <p>{comment content}</p>
    # `  </div>
    # `</div>

    def get(self, newsid, pageth):
        comments = self.db.query("select comment.id, comment.content, comment.postedat, comment.commentid, usr.email, usr.name from comment left join usr on comment.authorid=usr.id where comment.newsid=%s order by comment.postedat desc;" % newsid)
        if comments and int(pageth) * 10 < (len(comments) + 10):
            self.write(self._parseCommentsToHtml(comments, pageth))
        else:
            self.write('error')
        self.flush()
        
    def _getCommentById(self, comments, cid, id):
        for comment in comments:
            if comment['id'] == cid and comment['id'] != id:
                return comment
        return None

    def _parse(self, comment, comments):
        html = []
        html.append('<div>')
        comment = self._getCommentById(comments, comment['commentid'], comment['id'])
        if comment['commentid'] != 0:        
            if comment:
                html.append(self._parse(comment, comments))
        html.append('''<span>{author}</span><br />{content}</div>'''.format(**{'author': comment['name'], 'content': self.markdown(comment['content'])}))
        return ''.join(html)

    def _parseCommentsToHtml(self, comments, pageth):
        html = []
        for comment in comments[(int(pageth) - 1) * 10 : int(pageth) * 10]:
            html.append('''<div class="comment" id="{id}"><p class="title"><span>{time}</span><img height="50" src="{gravatar}" onerror="this.src=\'/static/image/default.png\'"></img>{author}</p>'''.format(**{'id': comment['id'], 'time': comment['postedat'], 'gravatar': gravatar(comment['email']), 'author': comment['name']}))
            if comment['commentid'] != 0:
                html.append(self._parse(comment, comments))
            html.append('<p>{content}{del}<a class="btn" style="float:right;" href="javascript:addQuote({id})">引用评论</a></p></div>'.format(**{'content': self.markdown(comment['content']), 'id': comment['id'], 'del': '<a class="btn" style="float:right;" href="javascript:delComment(' + str(comment['id']) + ');">删除评论</a>' if self.isAdmin() else ''}))
        return ''.join(html)

class ShowComments(BaseHandler):
    def get(self, id):
        newsinfo = self.db.get("select news.id, news.title, news.postedat, news.commentnum, category.name as category, usr.name as author, usr.email as email from news left join category on news.categoryid=category.id left join usr on news.author=usr.id where news.id=%s;" % id)
        comment_num = self.db.get("select count(*) from comment where comment.newsid=%s;" % id)
        self.write(self.serve_template('comment.html', **{'newsinfo': newsinfo, 'comment_num': comment_num['count'], 'xsrf': self.xsrf_form_html()}))
        self.flush()

class AddComment(BaseHandler):

    @authenticated
    def post(self):
        news_id = self.get_argument('comment_post_id')
        parent_id = self.get_argument('comment_parent')
        comment_content = self.get_argument('comment')
        user = self.get_current_user()
        if self.db.execute_rowcount("insert into comment(authorid, author, newsid, content, postedat, commentid) values('%s', '%s', '%s', '%s', '%s', '%s');" % (user['id'], user['name'], news_id, self.JsEscape(comment_content), time.ctime(), parent_id)):
            self.db.execute_rowcount("update news set commentnum = commentnum + 1 where id='%s';" % news_id)
            self.write('done')
        else:
            self.write('undone')
        self.finish()
        
class DelComment(BaseHandler):
    @admin
    def get(self, id):
        self.db.execute("update comment set commentid=(select commentid from comment where id=%s) where commentid=%s", *(id,id))
        if self.db.execute_rowcount("update news set commentnum = commentnum - 1 where id= (select newsid from comment where id=%s);", *(id,)):
            if self.db.execute_rowcount("delete from comment where id=%s;", *(id,)):
                self.write('done')
        else:
            self.write('undone')
