#coding=utf-8
from uliweb.form import *
from uliweb.i18n import ugettext as _

class ChangeInfoForm(Form):
    form_buttons = Submit(value=_('Save'), _class="submit")
    form_title = _('Change Basic Information')

    email = StringField(label=_('Email:'))
    image = ImageField(label=_('Portrait:'))
    action = HiddenField(default='changeinfo')
    
class LoginForm(Form):
    form_buttons = Submit(value=_('Login'), _class="button")
    form_title = _('Login')
    
    username = UnicodeField(label=_('Username:'), required=True)
    password = PasswordField(label=_('Password:'), required=True)
    rememberme = BooleanField(label=_('Remember Me'))
    next = HiddenField()
    
    def form_validate(self, all_data):
        from uliweb import settings
        from uliweb.orm import get_model
        
        User = get_model('user')
        user = User.get(User.c.username==all_data['username'])
        if not user:
            return {'username': _('User "%s" does not exist!') % all_data['username']}
        if not user.check_password(all_data['password']):
            return {'password' : _('Password is not right.')}
        if all_data['password'] == settings.USER_CONFIG.DEFAULT_PASSWORD:
            return {'password' : _("Please don't use default password, click <a href=\"%s\">here</a> to change your password.") % url_for(change_password, user.id)}
        
class ChangePasswordForm1(Form):
    form_buttons = Submit(value=_('Save'), _class="button")

    oldpassword = PasswordField(label=_('Old Password:'), required=True)
    password = PasswordField(label=_('Password:'), required=True)
    password1 = PasswordField(label=_('Password again:'), required=True)

    def validate_oldpassword(self, data):
        from uliweb import request
            
        if not request.user.check_password(data):
            raise ValidationError, _('Password is not right.')

class ChangePasswordForm2(Form):
    form_buttons = Submit(value=_('Save'), _class="button")

    username = StringField(label=_('Username:'), required=True)
    oldpassword = PasswordField(label=_('Old Password:'), required=True)
    password = PasswordField(label=_('Password:'), required=True)
    password1 = PasswordField(label=_('Password again:'), required=True)
    
    def form_validate(self, all_data):
        from uliweb.orm import get_model
        error = {}
        
        User = get_model('user')
        user = User.get(User.c.username == data)
        if not user:
            raise ValidationError, _('Username is not existed.')
        
        if all_data.password != all_data.password1:
            error['password1'] = _('Passwords are not the same between two types.')
            
        if not user.check_password(data):
            raise ValidationError, _('Password is not right.')
        
        return error
    
class AddUserForm(Form):
    def validate_username(self, data):
        from uliweb.orm import get_model
                 
        User = get_model('user')
        user = User.get(User.c.username == data)
        if (not self.user and user) or (user and self.user and self.user.id != user.id):
            raise ValidationError, _('The username is already existed! Please change another one.')
    
