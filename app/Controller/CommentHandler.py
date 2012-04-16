# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler
import copy

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

def parseCommentsToHtml(comments):
    html = []
    for comment in comments:
        html.append('''<div class="comment"><p class="title"><span>{time}</span>{author}</p>'''.format(**{'time': comment['postedat'], 'author': comment['name']}))
        if comment['commentid'] != 0:
            html.append(parse(comment, comments))
        html.append("<p>{content}</p></div>".format(**{'content': comment['content']}))
    return ''.join(html)

class ShowComments(BaseHandler):
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
        comments = self.db.query("select comment.id, comment.content, comment.postedat, comment.commentid, usr.email, usr.name from comment left join usr on comment.authorid=usr.id where comment.newsid=%s order by comment.postedat asc;" % newsid)
        if comments:
            print(comments)
            self.write(parseCommentsToHtml(comments) + '''<style type="text/css">
*{margin:0;padding:0;}
body{margin:10px;font-size:14px;font-family:宋体}
h1{font-size:26px;margin:10px 0 15px;}
#commentHolder{width:540px;border-bottom:1px solid #aaa;}
.comment{padding:5px 8px;background:#f8fcff;border:1px solid #aaa;font-size:14px;border-bottom:none;}
.comment p{padding:5px 0;}
.comment p.title{color:#1f3a87;font-size:12px;}
.comment p span{float:right;color:#666}
.comment div{background:#ffe;padding:3px;border:1px solid #aaa;line-height:140%;margin-bottom:5px;}
.comment div span{color:#1f3a87;font-size:12px;}
</style>''')
        else:
            self.write('error')
