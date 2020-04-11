from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CreateUserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    permission_type = (
        ('administrator', 'administrator'),
        ('manager', 'manager'),
        ('developer', 'developer'))
    permission = forms.ChoiceField(label="用户角色", choices=permission_type)
    department = forms.CharField(label="部门", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))


class UpdatePasswordForm(forms.Form):
    password1 = forms.CharField(label="新密码", max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CreateTaskForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state_type = (
        ('waiting for accepted', 'waiting for accepted'),
        ('accepted', 'accepted'),
        ('coding', 'coding'),
        ('testing', 'testing'),
        ('solved', 'solved'))
    state = forms.ChoiceField(label="State", choices=state_type)
    description = forms.CharField(label="Description", max_length=1024, widget=forms.Textarea(attrs={'class': 'form-control'}))
    priority_type = (
        ('Low', 'Low'),
        ('Middle', 'Middle'),
        ('High', 'High'),
        ('Special', 'Special'))
    priority = forms.ChoiceField(label="Priority", choices=priority_type)
    includeFileId = forms.CharField(label="Include id of files", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    assignee = forms.CharField(label="Assignee", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))


class DeveloperInfoForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    permission_type = (
        ('administrator', 'administrator'),
        ('manager', 'manager'),
        ('developer', 'developer'))
    permission = forms.ChoiceField(label="用户角色", choices=permission_type)
    department = forms.CharField(label="部门", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    task_assigned = forms.CharField(label="分配任务数", max_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))
    task_solved = forms.CharField(label="完成任务数", max_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))


class CreateDepartmentForm(forms.Form):
    name = forms.CharField(label="部门", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))


class TaskInfoForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state_type = (
        ('waiting for accepted', 'waiting for accepted'),
        ('accepted', 'accepted'),
        ('coding', 'coding'),
        ('testing', 'testing'),
        ('solved', 'solved'))
    state = forms.ChoiceField(label="State", choices=state_type)
    description = forms.CharField(label="Description", max_length=1024,
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))
    priority_type = (
        ('Low', 'Low'),
        ('Middle', 'Middle'),
        ('High', 'High'),
        ('Special', 'Special'))
    priority = forms.ChoiceField(label="Priority", choices=priority_type)
    assignee = forms.CharField(label="Assignee", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    supervisor = forms.CharField(label="Supervisor", max_length=32, widget=forms.TextInput(attrs={'class': 'form-control'}))
    includeFile = forms.CharField(label="Attach file", max_length=1024, widget=forms.TextInput(attrs={'class': 'form-control'}))
    # includeFileId = forms.FileField(label="Attach files")


