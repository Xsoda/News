# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler

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
    for comment in comments[(int(pageth) - 1) * 20 : int(pageth) * 20 + 1]:
        html.append('''<div class="comment"><p class="title"><span>{time}</span>{author}</p>'''.format(**{'time': comment['postedat'], 'author': comment['name']}))
        if comment['commentid'] != 0:
            html.append(parse(comment, comments))
        html.append("<p>{content}</p></div>".format(**{'content': comment['content']}))
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
        if comments and int(pageth) * 20 > len(comments):
            self.write(parseCommentsToHtml(comments, pageth))
        else:
            self.write('error')

class ShowComments(BaseHandler):
    def get(self, id):
        newsinfo = self.db.get("select news.id, news.title, news.postedat, news.commentnum, category.name as category, usr.name as author from news left join category on news.categoryid=category.id left join usr on news.author=usr.id where news.id=%s;" % id)
        self.write(self.serve_template('comment.html', **{'newsinfo': newsinfo}))
