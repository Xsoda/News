# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler, authenticated

class UserList(BaseHandler):
    @authenticated("admin")
    def get(self):
        userlist = self.db.query("select * from usr order by grade desc;")
        self.write(self.serve_template("admin/user.html", **{'userlist': userlist}))

class DelUser(BaseHandler):
    @authenticated("admin")
    def get(self, id):
        self.db.execute("select * from delUser(%s);", *(id,))
        self.write('done')

class EditUser(BaseHandler):
    @authenticated("admin")
    def get(self, id):
        user = self.db.get("select * from usr where id=%s;", *(id,))
        user['xsrf'] = self.xsrf_form_html()
        html = '''
        <form method="post" id="editform" action="/~/editUser_{id}">
        <table>
        <tr><td>用户名:</td><td>{name}</td></tr>
        <tr><td>用户权限:</td><td><select name="grade"><option value="0">普通用户</option><option value="1">管理员</option></select></tr>
        <tr><td><input type="submit" value="修改权限" /></tr>
        <input type="hidden" name="userid" value="{id}">{xsrf}
        </table></form>'''.format(**user)
        self.write(html)
        
    @authenticated("admin")
    def post(self,id):
        userid = self.get_argument('userid', None)
        grade = self.get_argument('grade', None)
        if userid and int(userid) != int(self.current_user['id']) and self.db.execute_rowcount("update usr set grade=%s where id=%s;", *(grade, userid)):
            self.write("done")
        else:
            self.write("undone")
