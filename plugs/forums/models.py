#! /usr/bin/env python
#coding=utf-8
from uliweb.orm import *
from uliweb.utils.common import get_var

def get_modified_user():
    from uliweb import request
    
    return request.user.id

class ForumCategory(Model):#板块
    name = Field(str, verbose_name='板块名称', max_length=100)
    description = Field(TEXT, verbose_name='板块描述')
    ordering = Field(int, verbose_name='排序',default = 1)
    created_on = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    updated_on = Field(datetime.datetime, verbose_name='修改时间', auto_now_add=True, auto_now=True)

    def __unicode__(self):
        return self.name
    
    class AddForm:
        fields = ['name', 'ordering']
        
    class EditForm:
        fields = ['name', 'ordering']

    class Table:
        fields = [
            {'name':'name', 'width':100},
            {'name':'ordering', 'width':40},
            {'name':'action', 'verbose_name':'操作', 'width':100},
        ]

class Forum(Model):#论坛
    name = Field(str, verbose_name='论坛名称', max_length=100, required=True)
#    slug = models.SlugField(max_length = 110)#标签
    description = Field(TEXT, verbose_name='论坛描述')
    ordering = Field(int, verbose_name='排序',default = 1)
    category = Reference('forumcategory', verbose_name='所属板块', collection_name='forums', required=True)
    created_on = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    updated_on = Field(datetime.datetime, verbose_name='修改时间', auto_now_add=True, auto_now=True)
    num_topics = Field(int, verbose_name='主题总数')
    num_posts = Field(int, verbose_name='文章总数')
#    attachments = Field(FILE, verbose_name='附件', hint='文件大小不能超过2M，请注意文件大小')

    last_reply_on = Field(datetime.datetime, verbose_name='最新回复时间')
    last_post_user = Reference('user', verbose_name='最后回复人', collection_name="last_post_user_forums")
    managers = ManyToMany('user', verbose_name='管理员')
    
    def __unicode__(self):
        return self.name
    
    class AddForm:
        fields = ['category', 'name', 'description', 'ordering', 'managers']
        
    class EditForm:
        fields = ['category', 'name', 'description', 'ordering', 'managers']
    
    class Table:
        fields = [
            {'name':'name', 'width':200},
            {'name':'description', 'width':200},
            {'name':'category', 'width':100},
            {'name':'ordering', 'width':40},
            {'name':'managers', 'width':100},
            {'name':'action', 'verbose_name':'操作', 'width':100},
        ]
    

class ForumTopicType(Model):
    forum = Reference('forum', verbose_name='所属论坛', collection_name='forum_topictype', required=True)
    name = Field(str, verbose_name='主题分类名称', max_length=100, required=True)
#    slug = models.SlugField(max_length = 100)#标签
    description = Field(TEXT, verbose_name='主题分类描述')
    
    def __unicode__(self):
        return self.name
    
    class AddForm:
        fields = ['forum', 'name', 'description']
        
    class EditForm:
        fields = ['forum', 'name', 'description']
    
    class Table:
        fields = [
            {'name':'name', 'width':100},
            {'name':'description', 'width':200},
            {'name':'forum', 'width':100},
            {'name':'action', 'verbose_name':'操作', 'width':100},
        ]

class ForumTopic(Model):#主题
    forum = Reference('forum', verbose_name='所属主题', collection_name='forum_topics', required=True)
    topic_type = Reference('forumtopictype', verbose_name='主题类型', collection_name='topic_topictype')
    posted_by = Reference('user', verbose_name='发贴人', default=get_modified_user, auto_add=True, collection_name="user_topics")
    
    subject = Field(str, verbose_name='标题', max_length=999, required=True)
    num_views = Field(int, verbose_name='浏览次数',default = 1)
    num_replies = Field(int, verbose_name='回复总数',default = 1)#posts...
    created_on = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    updated_on = Field(datetime.datetime, verbose_name='修改时间')
    last_reply_on = Field(datetime.datetime, verbose_name='最新回复时间')
    last_post_user = Reference('user', verbose_name='最后回复人', collection_name="last_post_user_topics")
    modified_user = Reference('user', verbose_name='最后修改人', default=get_modified_user, auto=True, collection_name="last_modified_user_topics")
    slug = Field(CHAR, max_length=32, verbose_name='唯一识别串')
    
    #Moderation features
    closed = Field(bool, verbose_name='是否关闭', default=False)
    sticky = Field(bool, verbose_name='是否置顶', default=False)
    hidden = Field(bool, verbose_name='是否隐藏', default=False)
    essence = Field(bool, verbose_name='是否精华贴')
    
    class AddForm:
        fields = ['topic_type', 'subject', 'content', 'slug']
        
    class EditForm:
        fields = ['topic_type', 'subject', 'content', 'slug']
    
class ForumAttachment(Model):
    slug = Field(CHAR, max_length=32, verbose_name='唯一识别串')
    file_name = Field(FILE, verbose_name='附件', hint='文件大小不能超过2M，请注意文件大小')
    name  = Field(str, verbose_name='文件显示名称', max_length=255)
    enabled = Field(bool, verbose_name='提交是否成功', default=False)
    created_on = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)

# Create Replies for a topic
class ForumPost(Model):#can't edit...回复
    topic = Reference('forumtopic', verbose_name='所属主题', collection_name='topic_posts')
    posted_by = Reference('user', verbose_name='回复人', default=get_modified_user, auto_add=True, collection_name='user_posts')
    created_on = Field(datetime.datetime, verbose_name='创建时间', auto_now_add=True)
    content = Field(TEXT, verbose_name='文章信息')
    updated_on = Field(datetime.datetime, verbose_name='修改时间')
    floor = Field(int, verbose_name='楼层', required=True)
    deleted = Field(bool, verbose_name='删除标志', default=False)
    slug = Field(CHAR, max_length=32, verbose_name='唯一识别串')
    modified_by = Reference('user', verbose_name='修改人', collection_name='user_modified_posts')
    deleted_by = Reference('user', verbose_name='删除人', collection_name='user_deleted_posts')
    deleted_on = Field(datetime.datetime, verbose_name='删除时间')

    @classmethod
    def OnInit(cls):
        Index('fpost_indx', cls.c.topic, cls.c.floor, unique=True)
    
    class AddForm:
        fields = ['content', 'slug']
    