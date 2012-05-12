# *_* coding: utf-8 *_*
__author__ = 'Xsoda'

from app.controller.Base import BaseHandler, authenticated
from core.web.encrypt import check_password, encrypt_password, salt_generator
from core.db.database import OperationalError, IntegrityError
from core.web.helpers import Gravatar
from core.web.mail import Mail

gravatar = Gravatar(size=140, rating='g', default='./../static/image/default.png', force_default=False, force_lower=True)
sendmail = Mail(smtpserver="smtp.live.com", smtpport="25", fromAddress="xsoda@live.com", fromPassword="1989ii24", subject="Reset You Password")
class Login(BaseHandler):
    def get(self):
        self.write(self.serve_template("login.html", **{'xsrf': self.xsrf_form_html()}))
        self.flush()

    def post(self):
        user_name = self.get_argument("user_name", None)
        user_password = self.get_argument("user_password", None)
        if user_name and user_password:
            userinfo = self.db.get("select id, name, password, salt, grade, email from usr where name='%s';" % user_name.lower())
            if userinfo and check_password(user_password, userinfo['password'], userinfo['salt']):
                self.session['user'] = userinfo
                self.session.save()
                self.write('done')
            else:
                self.write('user name or password error!')
        else:
            self.write('user name or password is empty!')
        self.flush()

class Register(BaseHandler):
    def get(self):
        self.write(self.serve_template("register.html", **{'xsrf': self.xsrf_form_html()}))
        self.flush()
        
    def post(self):
        user_name = self.get_argument("user_name", None)
        user_password = self.get_argument("user_password", None)
        repeat_password = self.get_argument("repeat_password", None)
        email = self.get_argument('email', None)
        if user_password == repeat_password:
            enc_pwd, salt = encrypt_password(user_password)
            if enc_pwd is not 'error':
                try:
                    self.db.execute("insert into usr(name, password, salt, email, grade) values(%s, %s, %s, %s, 0);", *(user_name.lower(), enc_pwd, salt, email.lower()))
                    self.write('done')
                except IntegrityError:
                    self.write('db error')
            else:
                self.write('operational error')
        else:
            self.write('pwd error')
        self.flush()
                    
class UserInfo(BaseHandler):
    def get(self):
        userinfo = self.get_current_user()
        if userinfo:
            print(userinfo)
            grade = '<a href="/~/">后台管理</a>' if int(userinfo['grade']) else ''
            img = gravatar(userinfo['email'])
            html = '<img height="50" src="' + img + '" onerror="../static/image/default.png"></img>' + '{name} ' + grade + '<a href="/auth/edit">修改密码</a> & <a href="/auth/logout">注销</a>'
            self.write(html.format(**userinfo))
        else:
            self.write('<a href="/auth/login">登录</a> & <a href="/auth/register">注册</a> & <a href="/auth/reset">重置密码</a>')

class Logout(BaseHandler):
    def get(self):
        self.clear_cookie("sid")
        self.session.clear()
        self.redirect("/")

class EditPassword(BaseHandler):
    @authenticated
    def get(self):
        self.write(self.serve_template("editpwd.html", **{'xsrf': self.xsrf_form_html()}))
        self.flush()
        
    @authenticated
    def post(self):
        old_pwd = self.get_argument("old_password", None)
        user_pwd = self.get_argument("user_password", None)
        repet_pwd = self.get_argument("repeat_password", None)
        if user_pwd == repeat_pwd:
            if check_password(old_pwd, self.current_user['password'], self.current_user['salt']):
                pwd, salt = encrypt_password(user_pwd)
                if pwd is not 'error' and self.db.execute_rowcount("update usr set password=%s, salt=%s where id=%s;", *(pwd, salt, self.current_user['id'])):
                    self.clear_cookie("sid")
                    self.session.clear()
                    self.write('done')
            else:
                self.write("olderror")
        else:
            self.write("newerror")
        self.flush()

class ResetPassword(BaseHandler):
    def get(self):
        self.write(self.serve_template("resetpwd.html", **{'xsrf': self.xsrf_form_html()}))
        self.flush()
        
    def post(self):
        user_name = self.get_argument("user_name", None)
        email = self.get_argument("email", None)
        if user_name and email:
            user = self.db.get("select * from usr where name=%s and email=%s;", *(user_name.lower(), email.lower()))
            if user:
                pwd = salt_generator(size=12)
                enc_pwd, salt = encrypt_password(pwd)
                if self.db.execute_rowcount("update usr set password=%s, salt=%s where id=%s;", *(enc_pwd, salt, user['id'])):
                    content= "Yours new password is:\n" + pwd + "\nplease use this password login website, and modify your password."
                    sendmail(email, content)
                    self.write('done')
            else:
                self.write("error")
        else:
            self.write("undone")
        self.flush()
