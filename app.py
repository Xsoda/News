# *-* coding: utf-8 *-*
#! /usr/bin/env python

import os.path
import sys
import re
import core.db.database
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
import app.controller
from app.controller import *
import redis
from core.session.session import RedisSessionStore

from tornado.options import define, options

define("port", default=9000, help="run on the given port", type=int)
define("pg_host", default="127.0.0.1:5432", help="database host")
define("pg_database", default="news", help="database name")
define("pg_user", default="postgres", help="database user")
define("pg_password", default="1989ii24", help="database password")
define("template_directory", default="app/view", help="default mako template directory")
define("mako_moudle_dir", default="app/view/mako_moudle", help="default mako complie template directory")

define('redis_host', default='localhost', help='Redis server host')
define('redis_port', default=6379, help='Redis server port')
define('redis_db', default=0, help='Redis server db')

define('expires_days', default=1, help='cookie and session expire days')

class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            title = "PPTM News",
            template_path = os.path.join(os.path.dirname(__file__), "app/view/"),
            static_path = os.path.join(os.path.dirname(__file__), "app/static/"),
            xsrf_cookies = True,
            cookie_secret = "760f802ae2ea1ca7120b1fee4e9aa16e3ea53698/Vo=",
            login_url = "/auth/login",
        )

        handlers = [
            (r"/", app.controller.HomeHandler.HomeHandler), # 主页
            (r"/news_(\d+)", app.controller.NewsHandler.ShowNews), # news_(新闻编号) -- 显示新闻内容 <GET>
            (r"/comments_(\d+)", app.controller.CommentHandler.ShowComments), # comments_(新闻编号) -- 显示新闻评论 <GET>
            (r"/category_(\d+)_(\d+)", app.controller.CategoryHandler.CategoryNews), # category_(分类编号)_(页码) -- 分页显示分类下的新闻目录 <GET>
            (r"/data/getCategory_(\d+)", app.controller.CategoryHandler.GetCategory),      # 获取分类目录 <GET>
            (r"/data/getComments_(\d+)_(\d+)", app.controller.CommentHandler.GetComments), # getComments_(新闻编号)_(页码) -- 获取新闻评论，分页，前台由ajax显示 <GET>
            (r"/data/addComment", app.controller.CommentHandler.AddComment), # 添加评论，<POST>
            (r"/auth/login", app.controller.AuthorizedHandler.Login), # 用户登录页面(包括管理员登录)
            (r"/auth/register", app.controller.AuthorizedHandler.Register), # 用户注册页面, 管理员也必须由此注册，然后由默认管理员修改其权限
            (r"/auth/getUserInfo", app.controller.AuthorizedHandler.UserInfo), # 获取当前登录的用户信息 ajax
            (r"/auth/logout", app.controller.AuthorizedHandler.Logout), # 注销登录(包括管理员注销)
            (r"/auth/edit", app.controller.AuthorizedHandler.EditPassword), # 修改密码
            (r"/auth/reset", app.controller.AuthorizedHandler.ResetPassword), # 重置密码
            (r"/~/", app.controller.AdminHandler.Home), # 管理员后台管理主页
            (r"/~/getAdmin", app.controller.AdminHandler.GetAdmin), # 获取当前管理员 ajax
            (r"/search", app.controller.NewsHandler.SearchNews), # 搜索新闻 <POST> 前台 ajax
            (r"/data/imgpost", app.controller.AdminHandler.ImgPost), # 图片上传 管理员后台 ajax
            (r"/~/addNews", app.controller.NewsHandler.AddNews), # 添加新闻 <GET> <POST>
            (r"/~/search", app.controller.NewsHandler.AdminSearch), # 搜索新闻 <POST> 后台
            (r"/~/editNews_(\d+)", app.controller.NewsHandler.EditNews), # 新闻修改 <GET> <POST>
            (r"/~/delNews_(\d+)", app.controller.NewsHandler.DelNews), # 删除新闻
            (r"/~/preview", app.controller.NewsHandler.Preview), # 新闻预览
            (r"/~/user", app.controller.UserHandler.UserList),   # 用户列表
            (r"/~/category", app.controller.CategoryHandler.AdminCategory), # 分类列表
            (r"/~/addCategory", app.controller.CategoryHandler.AddCategory), # 分类添加
            (r"/~/delCategory_(\d+)", app.controller.CategoryHandler.DelCategory), # 分类删除
            (r"/~/editCategory_(\d+)", app.controller.CategoryHandler.EditCategory), # 分类编辑
            (r"/~/delUser_(\d+)", app.controller.UserHandler.DelUser), # 用户删除
            (r"/~/editUser_(\d+)", app.controller.UserHandler.EditUser), # 用户编辑
            (r"/~/delComment_(\d+)", app.controller.CommentHandler.DelComment), # 评论删除
            (r"/~/newsList_(\d+)", app.controller.NewsHandler.NewsList), # 新闻列表
        ]
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = core.db.database.Connection(
            host = options.pg_host, database = options.pg_database,
            user = options.pg_user, password = options.pg_password)
        tornado.web.Application.__init__(self, handlers, **settings)
        self.redis = redis.Redis(host = options.redis_host, port = options.redis_port, db = options.redis_db)
        self.session_store = RedisSessionStore(self.redis)

def main():
    tornado.options.parse_command_line()
    if len(sys.argv) >= 2:
        port = sys.argv[1]
    else:
        port = options.port
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop=io_loop, check_time=500)
    io_loop.start()
    
if __name__ == "__main__":
    main()
