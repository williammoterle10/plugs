#coding=utf-8
from __future__ import with_statement

from uliweb import expose
from uliweb.contrib.auth import require_login
import plugs.generic.views as g_views

get_url = g_views.get_model_url('/users')

@require_login
@expose('/user/view')
def user_view():
    return users_view(request.user.id)

@require_login
@expose('/user/edit')
def user_edit():
    from plugs.generic.base import EditView
    
    view = EditView('user', condition=request.user.id, ok_url=url_for(user_view))
    return view.run()
    
@expose('/user/change_password')
def user_change_password():
    from uliweb.orm import get_model
    
    User = get_model('user')
    user_id = request.GET.get('user_id', None)
    data = {}
    if user_id:
        user = User.get(int(user_id))
        if user:
            data = {'username':user.username}
    from forms import ChangePasswordForm1, ChangePasswordForm2
    if request.user:
        form = ChangePasswordForm1()
    else:
        form = ChangePasswordForm2(data=data)
    if request.method == 'GET':
        return {'form':form, 'ok':False}
    if request.method == 'POST':
        flag = form.validate(request.POST)
        if flag:
            User = get_model('user')
            if user_id:
                user = User.get(User.c.username == form.username.data)
                user.set_password(form.password.data)
                flash(_('Password saved successfully.'))
                return redirect('/login?next=/')
            else:
                request.user.set_password(form.password.data)
                flash(_('Password saved successfully.'))
                return {'form':form, 'ok':True}
        else:
            if '_' in form.errors:
                message = form.errors['_']
            else:
                message = _('There are something wrong, please fix them.')
            flash(message, 'error')
            return {'form':form, 'ok':False}
    
def get_users_list_view(c):
    from plugs.generic.base import ListView
    from uliweb.orm import get_model
    from uliweb import request
    from uliweb.core.html import Tag
    from uliweb import orm
    
    def username(value, obj):
        return str(Tag('a', value, href='/users/%d' % obj.id))
    
    def boolean_convert(b, obj):
        if b:
            return '<div class="ui-icon ui-icon-check"></div>'
        else:
            return '<div class="ui-icon ui-icon-closethick"></div>'
    
    pageno = int(request.GET.get('pageno', 0))
    
    User = get_model('user')
    query = None
    condition = None
    if c.get('username'):
        condition = (User.c.username.like(c['username'])) & condition
    
    fields_convert_map = {'username':username}
    view =  ListView(User, condition=condition, query=query,
        rows_per_page=settings.get_var('PARA/ROWS_PER_PAGE', 10), pageno=pageno, 
        fields_convert_map=fields_convert_map, id='users_table')
    view.types_convert_map = {orm.BooleanProperty:boolean_convert}
    return view

def create_user_query(url):
    from plugs.generic.base import QueryView
    
    fields = ('username',) 
    query = QueryView('user', ok_url=url, fields=fields)
    return query

@require_login
@expose('/users/list')
def users_list():
    query_view = create_user_query(url_for(users_list))
    c = query_view.run()

    view = get_users_list_view(c)
    if 'data' in request.GET:
        result = view.run(head=False, body=True)
        return json(result)
    else:
        result = view.run(head=True, body=False)
        result.update({'query_form':query_view.form})
        return result
    
@require_login
@expose('/users/add')
def users_add():
    from plugs.generic.base import AddView
    from uliweb.orm import get_model
    from forms import AddUserForm
    
    
    def post_save(obj, data):
        obj.set_password(settings.USER_ADMIN.DEFAULT_PASSWORD)
        
    if request.user.is_superuser:
        view = AddView('user', get_url('view'), post_save=post_save, form_cls=AddUserForm)
        return view.run()
    else:
        flash(_('You have no previlege to create user.'), 'error')
        return redirect(url_for(config_users_list))
    
@require_login
@expose('/users/<int:id>')
def users_view(id):
    from plugs.generic.base import DetailView
    from uliweb import orm
    
    def boolean_convert(b, obj):
        if b:
            return '<div class="ui-icon ui-icon-check"></div>'
        else:
            return '<div class="ui-icon ui-icon-closethick"></div>'
    
    view = DetailView('user', int(id))
    view.types_convert_map = {orm.BooleanProperty:boolean_convert}
    return view.run()
    
@require_login
@expose('/users/<int:id>/edit')
def users_edit(id):
    from plugs.generic.base import EditView
    from forms import EditUserForm

    if request.user.is_superuser:
        view = EditView('user', condition=int(id), ok_url=get_url('view'),
            form_cls=EditUserForm)
        return view.run()
    else:
        flash(_('You have no previlege to edit user.'), 'error')
        return redirect(request.referrer)
    
@require_login
@expose('/users/<int:id>/delete')
def users_delete(id):
    from plugs.generic.base import DeleteView
    
    if request.user.is_superuser:
        view = DeleteView('user', condition=int(id), ok_url=url_for(users_list))
        return view.run()
    else:
        flash(_('You have no previlege to delete user.'), 'error')
        return redirect(url_for(users_view, id=id))
    
@require_login
#@expose('/users/<int:id>/reset')
def users_reset(id):
    from uliweb.orm import get_model
    
    User = get_model('user')
    if request.user.is_superuser:
        user = User.get(int(id))
        user.set_password(settings.PARA.DEFAULT_PASSWORD)
        flash(_('Password reset successfully.'))
        return redirect(request.referrer)
    else:
        flash(_('You have no previlege to reset user password.'), 'error')
        return redirect(url_for(users_view, id=id))
        
