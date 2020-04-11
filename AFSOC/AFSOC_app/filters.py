from django_filters import FilterSet, CharFilter

from .models import CrashFile
from .models import Task
from .models import Developer


class CrashFileFilter(FilterSet):
    class Meta:
        model = CrashFile
        fields = {"software_version": ["contains"], "error_type": ["contains"], "occur_time": ["contains"],
                  "user": ["contains"], "os_information": ["contains"], "opengl_version": ["contains"], "solved": ["exact"]}


class TaskFilter(FilterSet):
    assignee = CharFilter(field_name='assignee__name', lookup_expr='contains')
    supervisor = CharFilter(field_name='supervisor__name', lookup_expr='contains')
    class Meta:
        model = Task
        fields = {"title": ["contains"], "state": ["exact"], "priority": ["exact"], "create_time": ["contains"]}


class DeveloperFilter(FilterSet):
    class Meta:
        model = Developer
        fields = {"name": ["contains"], "permission": ["exact"]}
