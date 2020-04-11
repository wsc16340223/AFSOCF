import django_tables2 as tables
from .models import CrashFile
from .models import Task
from .models import Developer


class CrashFileTable(tables.Table):
    id = tables.Column(linkify=True)

    class Meta:
        model = CrashFile
        template_name = 'django_tables2/bootstrap.html'


class TaskTable(tables.Table):
    id = tables.Column(linkify=True)

    class Meta:
        model = Task
        template_name = 'django_tables2/bootstrap.html'


class DeveloperTable(tables.Table):
    id = tables.Column(linkify=True)

    class Meta:
        model = Developer
        template_name = 'django_tables2/bootstrap.html'
