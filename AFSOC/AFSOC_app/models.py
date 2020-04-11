from django.db import models
from django.urls import reverse


# 部门
class Department(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "department"


# 任务完成速度
class WorkSpeed(models.Model):
    task_count = models.IntegerField(default=0)
    finished_count = models.IntegerField(default=0)
    speed = models.FloatField(default=0.5)

    def __str__(self):
        return str(self.speed)

    class Meta:
        db_table = "workspeed"


# 开发者
class Developer(models.Model):

    permission_type = (
        ('administrator', 'administrator'),
        ('manager', 'manager'),
        ('developer', 'developer'))

    name = models.CharField(max_length=32, unique=True, db_index=True)
    password = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    permission = models.CharField(max_length=64, choices=permission_type, default='developer')

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    work_speed = models.ForeignKey(WorkSpeed, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "developer"

    def get_absolute_url(self):
        return reverse("developer_detail", args=(self.pk,))


# 崩溃文件
class CrashFile(models.Model):
    subject = models.CharField(max_length=64, default='subject')
    path = models.CharField(max_length=512, null=True, default='')
    software_version = models.CharField(max_length=64, null=True, default='')
    error_type = models.CharField(max_length=64, null=True, default='')
    occur_time = models.CharField(max_length=64, null=True, default='')
    user = models.CharField(max_length=64, null=True, default='')
    os_information = models.CharField(max_length=64, null=True, default='')
    opengl_version = models.CharField(max_length=64, null=True, default='')
    solved = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

    class Meta:
        db_table = "crashfile"

    def get_absolute_url(self):
        return reverse("crashFile_detail", args=(self.pk,))


# 任务
class Task(models.Model):

    priority_type = (
        ('Low', 'Low'),
        ('Middle', 'Middle'),
        ('High', 'High'),
        ('Special', 'Special'))
    state_type = (
        ('waiting for accepted', 'waiting for accepted'),
        ('accepted', 'accepted'),
        ('coding', 'coding'),
        ('testing', 'testing'),
        ('solved', 'solved'))

    title = models.CharField(max_length=64, unique=True)
    state = models.CharField(max_length=64, choices=state_type, default='waiting for accepted')
    description = models.CharField(max_length=1024)
    priority = models.CharField(max_length=64, choices=priority_type, default='Middle')
    create_time = models.DateTimeField(auto_now_add=True)

    file = models.ForeignKey(CrashFile, on_delete=models.SET_NULL, null=True, related_name='crashfile')
    assignee = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, related_name='assignee')
    supervisor = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, related_name='supervisor')

    def __str__(self):
        return self.title

    class Meta:
        db_table = "task"

    def get_absolute_url(self):
        return reverse("task_detail", args=(self.pk,))
