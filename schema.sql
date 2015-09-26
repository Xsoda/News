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
alter table usr add constraint usr_name_uni unique(name); -- 添加唯一约束
alter table usr add constraint usr_email_uni unique(email);

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
       summary varchar(255) not null, -- 概要
       doc varchar(255) not null default 'Markdown', -- 格式, 预计支持 Markdown, reStructuredText, HTML, Textile四种格式
       source varchar(255) null, -- 来源
       author bigint not null, -- 编辑
       postedAt timestamp not null, -- 发布日期
       commentNum bigint not null, -- 评论数
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


create or replace function delCategory(integer) returns void as $$
declare
    news record;
begin
    for news in (select * from news where categoryid=$1) loop
        delete from comment where newsid=news.id;
    end loop;
    delete from news where categoryid=$1;
    delete from category where id=$1;
    return;
end;
$$ language plpgsql;
-- drop function delCategory(integer);

create or replace function delUser(integer) returns void as $$
begin
    delete from comment where authorId=$1;
    delete from news where author=$1;
    delete from usr where id=$1;
    return;
end;
$$ language plpgsql;
-- drop function delUser(integer);

create or replace function searchNews(refcursor, character varying) returns refcursor as $$
declare
    condition varchar;
begin
    condition := '%' || $2 || '%';
    open $1 for
         select news.id, news.title, news.summary, news.content, news.postedat, news.commentnum, category.name as category, usr.name as author 
         from news
         left join usr on news.author=usr.id
         left join category on news.categoryid=category.id
         where news.title like condition or news.summary like condition or news.content like condition;
    return $1;
end;
$$ language plpgsql;

-- usage: select * from searchNews('search', '1'); fetch all from search;
-- drop function searchNews(refcursor, varchar);

-- Add Data !
insert into category(id, name, parentId) values(100, '国内', 0);
insert into category(id, name, parentId) values(101, '国际', 0);
insert into category(id, name, parentId) values(102, '社会', 0);
insert into category(id, name, parentId) values(103, '评论', 0);
insert into category(id, name, parentId) values(104, '深度', 0);
insert into category(id, name, parentId) values(105, '军事', 0);
insert into category(id, name, parentId) values(106, '历史', 0);
insert into category(id, name, parentId) values(107, '探索', 0);
insert into category(id, name, parentId) values(108, '图片', 0);
insert into category(id, name, parentId) values(109, '博客', 0);
insert into category(id, name, parentId) values(110, '论坛', 0);
insert into category(id, name, parentId) values(111, '公益', 0);
insert into category(id, name, parentId) values(112, '媒体', 0);
insert into usr(name, password, salt, email, grade)
        values ( 'admin', '01e0f1ec36407fd64565484435300a9d62e6e812c52ae03830c4acb9f6b4301e', 'myS%TyWHAeHyGz`2I5}VNWa%', 'xsoda@live.cn', '1');



