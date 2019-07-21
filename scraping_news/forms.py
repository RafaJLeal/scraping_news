from django.contrib.auth.forms import UserChangeForm

class UserDataForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserDataForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
        self.fields.pop('last_login')
        self.fields.pop('is_superuser')
        self.fields.pop('groups')
        self.fields.pop('user_permissions')
        self.fields.pop('username')
        self.fields.pop('is_staff')
        self.fields.pop('is_active')
        self.fields.pop('date_joined')