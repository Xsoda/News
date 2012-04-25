# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler
import time
from core.web.helpers import gravatar
from tornado.web import authenticated

def getCommentById(comments, cid, id):
    for comment in comments:
        if comment['id'] == cid and comment['id'] != id:
            return comment
    return None

def parse(comment, comments):
    html = []
    html.append('<div>')
    comment = getCommentById(comments, comment['commentid'], comment['id'])
    if comment['commentid'] != 0:        
        if comment:
            html.append(parse(comment, comments))
    html.append('''<span>{author}</span><br />{content}</div>'''.format(**{'author': comment['name'], 'content': comment['content']}))
    return ''.join(html)

def parseCommentsToHtml(comments, pageth):
    html = []
    for comment in comments[(int(pageth) - 1) * 10 : int(pageth) * 10]:
        html.append('''<div class="comment"><p class="title"><span>{time}</span><img height="20" src="{gravatar}"></img>{author}</p>'''.format(**{'time': comment['postedat'], 'gravatar': gravatar(comment['email']), 'author': comment['name']}))
        if comment['commentid'] != 0:
            html.append(parse(comment, comments))
        html.append('<p>{content}<a class="btn" style="float:right;" href="javascript:addQuote({id})">引用评论</a></p></div>'.format(**{'content': comment['content'], 'id': comment['id']}))
    return ''.join(html)

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
            self.write(parseCommentsToHtml(comments, pageth))
        else:
            self.write('error')
        self.flush()

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
        if self.db.execute_rowcount("insert into comment(authorid, author, newsid, content, postedat, commentid) values('%s', '%s', '%s', '%s', '%s', '%s');" % (user['id'], user['name'], news_id, comment_content, time.ctime(), parent_id)):
            self.db.execute_rowcount("update news set commentnum = commentnum + 1 where id='%s';" % news_id)
            self.write('done')
        else:
            self.write('undone')
        self.finish()
        
