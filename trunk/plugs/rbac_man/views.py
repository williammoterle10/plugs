#coding=utf-8
from uliweb import expose
from uliweb.orm import get_model
from uliweb.i18n import ugettext_lazy as _

def __begin__():
    from uliweb.contrib.auth import if_login
    return if_login()

@expose('/config/roles')
class RoleView(object):
    def __init__(self):
        self.model = get_model('role')
        
    def list(self):
        from uliweb.utils.generic import ListView
        
        pageno = int(request.values.get('page', 1)) - 1
        rows_per_page=int(request.values.get('rows', settings.get_var('PARA/ROWS_PER_PAGE', 10)))

        def name(value, obj):
            return '<a href="%s">%s</a>' % (url_for(RoleView.view, id=obj.id), value)
            
        fields = [
            {'name':'name', 'verbose_name':_('Name'), 'width':80},
            {'name':'description', 'verbose_name':_('Description'), 'width':200},
            {'name':'reserve', 'verbose_name':_('Is Reserved'), 'width':80},
        ]
        fields_convert_map = {'name':name}
        view = ListView(self.model, rows_per_page=rows_per_page, pageno=pageno,
            fields=fields, fields_convert_map=fields_convert_map)
        
        if 'data' in request.values:
            return json(view.json())
        else:
            result = view.run(head=True, body=False)
            result.update({'table':view})
            return result

    def view(self, id):
        """
        Role display
        """
        
        from uliweb.utils.generic import DetailView
        
        fields = [
            {'name':'name', 'verbose_name':_('Name')},
            {'name':'description', 'verbose_name':_('Description')},
            {'name':'reserve', 'verbose_name':_('Is Reserved')},
        ]
        
        obj = self.model.get(int(id))
        view = DetailView(self.model, obj=obj, fields=fields)
        return view.run()
        
    def add(self):
        """
        Add new role
        """
        
        from uliweb.utils.generic import AddView
        from functools import partial
        
        url = partial(url_for, RoleView.view)
        
        default_data = {'reverse':False}
        
        fields = [
            {'name':'name', 'verbose_name':_('Name')},
            {'name':'description', 'verbose_name':_('Description')},
        ]

        view = AddView(self.model, url, default_data=default_data, fields=fields)
        return view.run()
    
    def edit(self, id):
        """
        Edit the role
        """
        
        from uliweb.utils.generic import EditView
        from uliweb.orm import get_model
        
        obj = self.model.get(int(id))
        
        fields = [
            {'name':'name', 'verbose_name':_('Name')},
            {'name':'description', 'verbose_name':_('Description')},
            {'name':'reserve', 'verbose_name':_('Is Reserved')},
        ]

        view = EditView(self.model, url_for(RoleView.view, id=int(id)), 
            obj=obj, fields=fields)
        return view.run()
    
    def delete(self, id):
        """
        Delete a role
        """
        
        from uliweb.utils.generic import DeleteView
        
        obj = self.model.get(int(id))
        view = DeleteView(self.model, url_for(RoleView.list), obj=obj)
        return view.run()
    
    def adduser(self):
        User = get_model('user')
        Role = get_model('role')
        
        user_id = request.POST.get('user_id')
        role_id = request.POST.get('role_id')
        user = User.get(int(user_id))
        role = Role.get(int(role_id))
        if not user:
            return json({'success':False, 'message':"Can't find the user id %s" % user_id})
        if not role:
            return json({'success':False, 'message':"Can't find the role id %s" % role_id})
        if role.users.has(user):
            return json({'success':False, 'message':"The user %s has already existed in role %s" % (user.username, role.name)})
        else:
            role.users.add(user)
            return json({'success':True, 'data':{'username':user.username, 'id':user.id}, 'message':"The user %s added to role %s successfully" % (user.username, role.name)})
            
    def deluser(self):
        User = get_model('user')
        Role = get_model('role')
        
        user_id = request.POST.get('user_id')
        role_id = request.POST.get('role_id')
        user = User.get(int(user_id))
        role = Role.get(int(role_id))
        if not user:
            return json({'success':False, 'message':"Can't find the user id %s" % user_id})
        if not role:
            return json({'success':False, 'message':"Can't find the role id %s" % role_id})
        if role.users.has(user):
            role.users.remove(user)
            return json({'success':True, 'message':"The user %s has been delete from role %s successfully." % (user.username, role.name)})
        else:
            return json({'success':False, 'message':"The user %s is not existed in role %s successfully." % (user.username, role.name)})
   
    def addperm(self):
        Perm = get_model('permission')
        Role = get_model('role')
        
        perm_id = request.POST.get('perm_id')
        role_id = request.POST.get('role_id')
        perm = Perm.get(int(perm_id))
        role = Role.get(int(role_id))
        if not perm:
            return json({'success':False, 'message':"Can't find the permission id %s" % perm_id})
        if not role:
            return json({'success':False, 'message':"Can't find the role id %s" % role_id})
        if role.permissions.has(perm):
            return json({'success':False, 'message':"The permission %s has already existed in role %s" % (perm.name, role.name)})
        else:
            role.permissions.add(perm)
            return json({'success':True, 'data':{'name':perm.name, 'id':perm.id}, 'message':"The permission %s added to role %s successfully" % (perm.name, role.name)})
            
    def delperm(self):
        Perm = get_model('permission')
        Role = get_model('role')
        
        perm_id = request.POST.get('perm_id')
        role_id = request.POST.get('role_id')
        perm = Perm.get(int(perm_id))
        role = Role.get(int(role_id))
        if not perm:
            return json({'success':False, 'message':"Can't find the permission id %s" % perm_id})
        if not role:
            return json({'success':False, 'message':"Can't find the role id %s" % role_id})
        if role.permissions.has(perm):
            role.permissions.remove(perm)
            return json({'success':True, 'message':"The permission %s has been delete from role %s successfully." % (perm.name, role.name)})
        else:
            return json({'success':False, 'message':"The permission %s is not existed in role %s successfully." % (perm.name, role.name)})
    
@expose('/config/permissions')
class PermissionView(object):
    def __init__(self):
        self.model = get_model('permission')
        
    def list(self):
        from uliweb.utils.generic import ListView
        
        pageno = int(request.values.get('page', 1)) - 1
        rows_per_page=int(request.values.get('rows', settings.get_var('PARA/ROWS_PER_PAGE', 10)))

        def name(value, obj):
            return '<a href="%s">%s</a>' % (url_for(PermissionView.view, id=obj.id), value)
            
        fields = [
            {'name':'name', 'verbose_name':_('Name'), 'width':80},
            {'name':'description', 'verbose_name':_('Description'), 'width':200},
        ]
        fields_convert_map = {'name':name}
        view = ListView(self.model, rows_per_page=rows_per_page, pageno=pageno,
            fields=fields, fields_convert_map=fields_convert_map)
        
        if 'data' in request.values:
            return json(view.json())
        else:
            result = view.run(head=True, body=False)
            result.update({'table':view})
            return result

    def view(self, id):
        """
        Role display
        """
        
        from uliweb.utils.generic import DetailView
        
        fields = [
            {'name':'name', 'verbose_name':_('Name')},
            {'name':'description', 'verbose_name':_('Description')},
        ]
        
        obj = self.model.get(int(id))
        view = DetailView(self.model, obj=obj, fields=fields)
        return view.run()
        
    def add(self):
        """
        Add new role
        """
        
        from uliweb.utils.generic import AddView
        from functools import partial
        
        url = partial(url_for, PermissionView.view)
        
        default_data = {'reverse':False}
        
        fields = [
            {'name':'name', 'verbose_name':_('Name')},
            {'name':'description', 'verbose_name':_('Description')},
        ]

        view = AddView(self.model, url, default_data=default_data, fields=fields)
        return view.run()
    
    def edit(self, id):
        """
        Edit the role
        """
        
        from uliweb.utils.generic import EditView
        from uliweb.orm import get_model
        
        obj = self.model.get(int(id))
        
#        def get_form_field(name, obj):
#            from uliweb.form import SelectField
#            
#            if name == 'users':
#                choices = [(x.id, x.username) for x in obj.users.all()]
#                return SelectField('用户', name=name, choices=choices, 
#                    multiple=True, html_attrs={'url':'/config/users/search'},
#                    datatype=int)

        fields = [
            {'name':'name', 'verbose_name':_('Name')},
            {'name':'description', 'verbose_name':_('Description')},
        ]

        view = EditView(self.model, url_for(PermissionView.view, id=int(id)), 
            obj=obj, fields=fields)
        return view.run()
    
    def delete(self, id):
        """
        Delete a role
        """
        
        from uliweb.utils.generic import DeleteView
        
        obj = self.model.get(int(id))
        view = DeleteView(self.model, url_for(PermissionView.list), obj=obj)
        return view.run()
    
    def search(self):
        name = request.GET.get('term', '')
        if name:
            result = [{'id':obj.id, 'title':obj.name} for obj in self.model.filter(self.model.c.name.like(name + '%%'))]
        else:
            result = []
        return json(result)
    