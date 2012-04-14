-- Up!
create sequence usr_id_seq start 1;
create table usr( -- 用户表
       id bigint not null default nextval('usr_id_seq'), -- Id
       name varchar(255) not null, -- 用户名
       password varchar(255) not null, -- 密码（sha256加密）
       salt varchar(255) not null, -- 随机字符串
       email varchar(255) not null, -- Email
       grade varchar(255) not null, -- 级别
       constraint pk_usr primary key (id)
);
alter sequence usr_id_seq owned by usr.id;

create sequence category_id_seq start 1;
create table category( -- 新闻分类表
       id bigint not null default nextval('category_id_seq'), -- Id
       name varchar(255) not null, -- 分类名
       parentId bigint null, -- 父分类
       constraint pk_category primary key (id)
);
alter sequence category_id_seq owned by category.id;
--alter table category add constraint fk_category_category_1 foreign key (parentId) references  category(id) on delete restrict on update restrict;

create sequence news_id_seq start 1;
create table news( -- 新闻表
       id bigint not null default nextval('news_id_seq'), -- Id
       categoryId bigint not null, -- 分类Id
       title varchar(255) not null, -- 标贴
       content varchar(10000) not null, -- 内容
       source varchar(255) null, -- 来源
       author bigint not null, -- 编辑
       postedAt timestamp not null, -- 发布日期
       constraint pk_news primary key (id)
);
alter sequence news_id_seq owned by news.id;
alter table news add constraint fk_news_usr_1 foreign key (author) references usr(id) on delete restrict on update restrict;
alter table news add constraint fk_news_category_1 foreign key (categoryId) references category(id) on delete restrict on update restrict;
create index ix_news_usr_1 on news(author);
create index ix_news_category_1 on news(categoryId);

create sequence comment_id_seq;
create table comment( -- 用户评论表
       id bigint not null default nextval('comment_id_seq'), -- Id
       authorId bigint not null,  -- 用户编号，非注册用户为0,所以不需要为该字段建立外键
       author varchar(255) not null, -- 评论人姓名
       newsId bigint not null, -- 新闻Id
       content varchar(512) not null, -- 评论内容
       postedAt timestamp not null, -- 评论时间
       commentId bigint null, -- 自反 引用评论
       postId bigint null, -- 自反 回复评论 
       constraint pk_comment primary key (id)
);
alter sequence comment_id_seq owned by comment.id;
-- alter table comment add constraint fk_comment_usr_1 foreign key (authorId) references usr(id) on delete restrict on update restrict;
alter table comment add constraint fk_comment_news_1 foreign key (newsId) references news(id) on delete restrict on update restrict;
--alter table comment add constraint fk_comment_comment_1 foreign key (commentId) references comment(id) on delete restrict on update restrict;
--alter table comment add constraint fk_comment_comment_2 foreign key (postId) references comment(id) on delete restrict on update restrict;
create index ix_comment_usr_1 on comment(authorId);
create index ix_comment_news_1 on comment(newsId);

create sequence tag_id_seq;
create table tag( -- Tag
       id bigint not null default nextval('tag_id_seq'), -- Id
       name varchar(255) not null, -- Tag名
       constraint pk_tag primary key (id)
);
alter sequence tag_id_seq owned by tag.id;

create sequence newstag_id_seq;
create table newstag( -- Tag 与 News 的关系表 * to *
       id bigint not null default nextval('newstag_id_seq'), -- Id
       newsId bigint not null, -- 新闻编号
       tagId bigint not null, -- Tag 编号
       constraint pk_newstag primary key (id)
);
alter sequence newstag_id_seq owned by newstag.id;
alter table newstag add constraint fk_newstag_news_1 foreign key (newsId) references news(id) on delete restrict on update restrict;
alter table newstag add constraint fk_newstag_tag_1 foreign key (tagId) references tag(id) on delete restrict on update restrict;
create index ix_newstag_news_1 on newstag(newsId);
create index ix_newstag_tag_1 on newstag(tagId);

-- Add Data !
insert into category(id, name, parentId) values(100, "国内", 0);
insert into category(id, name, parentId) values(101, "国际", 0);
insert into category(id, name, parentId) values(102, "社会", 0);
insert into category(id, name, parentId) values(103, "评论", 0);
insert into category(id, name, parentId) values(104, "深度", 0);
insert into category(id, name, parentId) values(105, "军事", 0);
insert into category(id, name, parentId) values(106, "历史", 0);
insert into category(id, name, parentId) values(107, "探索", 0);
insert into category(id, name, parentId) values(108, "图片", 0);
insert into category(id, name, parentId) values(109, "博客", 0);
insert into category(id, name, parentId) values(110, "论坛", 0);
insert into category(id, name, parentId) values(111, "公益", 0);
insert into category(id, name, parentId) values(112, "媒体", 0);

-- Down !
drop table usr if exists usr;
drop table news if exists news;
drop table comment if exists comment;

