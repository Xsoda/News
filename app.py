# *-* coding: utf-8 *-*
#! /usr/bin/env python

import os.path
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
            (r"/", app.controller.HomeHandler.HomeHandler), 
            (r"/news_(\d+)", app.controller.NewsHandler.ShowNews), # news_(新闻编号) -- 显示新闻内容 <GET>
            (r"/comments_(\d+)", app.controller.CommentHandler.ShowComments), # comments_(新闻编号) -- 显示新闻评论 <GET>
            (r"/category_(\d+)_(\d+)", app.controller.CategoryHandler.CategoryNews), # category_(分类编号)_(页码) -- 分页显示分类下的新闻目录 <GET>
            (r"/data/getCategory_(\d+)", app.controller.CategoryHandler.GetCategory),      # 获取分类目录 <GET>
            (r"/data/getComments_(\d+)_(\d+)", app.controller.CommentHandler.GetComments), # getComments_(新闻编号)_(页码) -- 获取新闻评论，分页，前台由ajax显示 <GET>
            (r"/data/addComment", app.controller.CommentHandler.AddComment), # 添加评论，<POST>
            (r"/auth/login", app.controller.AuthorizedHandler.Login),
            (r"/auth/register", app.controller.AuthorizedHandler.Register),
            (r"/auth/getUserInfo", app.controller.AuthorizedHandler.UserInfo),
            (r"/auth/logout", app.controller.AuthorizedHandler.Logout),
            (r"/auth/edit", app.controller.AuthorizedHandler.EditPassword),
            (r"/auth/reset", app.controller.AuthorizedHandler.ResetPassword),
            (r"/~/", app.controller.AdminHandler.Home),
            (r"/search", app.controller.NewsHandler.SearchNews), # 搜索新闻 <POST>
            (r"/data/imgpost", app.controller.AdminHandler.ImgPost),
            (r"/~/addNews", app.controller.NewsHandler.AddNews),
            (r"/~/editNews_(\d+)", app.controller.NewsHandler.EditNews),
            (r"/~/delNews_(\d+)", app.controller.NewsHandler.DelNews),
            (r"/~/preview", app.controller.NewsHandler.Preview),
            (r"/~/user", app.controller.UserHandler.UserList),
            (r"/~/category", app.controller.CategoryHandler.AdminCategory),
            (r"/~/addCategory", app.controller.CategoryHandler.AddCategory),
            (r"/~/delCategory_(\d+)", app.controller.CategoryHandler.DelCategory),
            (r"/~/editCategory_(\d+)", app.controller.CategoryHandler.EditCategory),
            (r"/~/delUser_(\d+)", app.controller.UserHandler.DelUser),
            (r"/~/editNews_(\d+)", app.controller.NewsHandler.EditNews),
            (r"/~/editUser_(\d+)", app.controller.UserHandler.EditUser),
            (r"/~/delComment_(\d+)", app.controller.CommentHandler.DelComment),
            (r"/~/newsList_(\d+)", app.controller.NewsHandler.NewsList),
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
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop=io_loop, check_time=500)
    io_loop.start()
    
if __name__ == "__main__":
    main()
