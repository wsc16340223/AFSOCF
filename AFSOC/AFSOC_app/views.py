from django_tables2 import RequestConfig, SingleTableMixin
from django_tables2.export.views import ExportMixin
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.views import FilterView
from django.db.models import Q
from django.http import FileResponse
from . import models
from . import tables
from .forms import (
    LoginForm,
    CreateUserForm,
    UpdatePasswordForm,
    CreateTaskForm,
    DeveloperInfoForm,
    CreateDepartmentForm,
    TaskInfoForm)
from .filters import (
    CrashFileFilter,
    TaskFilter,
    DeveloperFilter
)
import os
import shutil
import zipfile


# 主页
def index(request):
    pass
    return render(request, 'AFSOC_app/index.html')


# 登录
def login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.Developer.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['email'] = user.email
                    request.session['permission'] = user.permission
                    request.session['department'] = user.department.name
                    if user.permission == 'administrator':
                        return redirect('/AFSOC_app/taskCenter_admin')
                    else:
                        return redirect('/AFSOC_app/taskCenter')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
    login_form = LoginForm(request.GET)
    return render(request, 'AFSOC_app/login.html', locals())


# 退出登录
def logout(request):
    if request.session.get('is_login'):
        request.session.flush()
    return redirect('/AFSOC_app/index')


# 任务中心
def taskCenter(request):
    task_table = tables.TaskTable(models.Task.objects.all())
    # 开发者只能看见分配给自己的任务
    if request.session.get('permission') == 'developer':
        user_id = request.session.get('user_id')
        task_table = tables.TaskTable(models.Task.objects.filter(assignee=user_id))
        task_assigned = len(models.Task.objects.filter(assignee_id=user_id))
        task_solved = len(models.Task.objects.filter(assignee_id=user_id, state='solved'))
        if request.method == "POST":
            if 'show' in request.POST:
                qs = models.Task.objects.filter(assignee=user_id)
            else:
                qs = models.Task.objects.filter(~Q(state='solved') & Q(assignee=user_id))
            task_table = tables.TaskTable(qs)
        # 限定每页显示数据数
        RequestConfig(request, paginate={'per_page': 20}).configure(task_table)
        return render(request, 'AFSOC_app/TaskCenter.html', {'table': task_table,
                                                             'task_assigned': task_assigned,
                                                             'task_solved': task_solved})
    # 经理只能看见本部门的任务
    elif request.session.get('permission') == 'manager':
        department = models.Department.objects.get(name=request.session.get('department'))
        developers = models.Developer.objects.filter(department=department)
        task_table = tables.TaskTable(models.Task.objects.filter(assignee__in=developers))
        if request.method == "POST":
            if 'show' in request.POST:
                qs = models.Task.objects.filter(assignee__in=developers)
            else:
                qs = models.Task.objects.filter(~Q(state='solved') & Q(assignee__in=developers))
            task_table = tables.TaskTable(qs)
        # 限定每页显示数据数
        RequestConfig(request, paginate={'per_page': 20}).configure(task_table)
        return render(request, 'AFSOC_app/TaskCenter.html', {'table': task_table})
    """   
    # 管理员可以看见所有任务
    else:
        task_table = tables.TaskTable(models.Task.objects.all())
        # 限定每页显示数据数
        RequestConfig(request, paginate={'per_page': 20}).configure(task_table)
        return render(request, 'AFSOC_app/TaskCenter.html', {'table': task_table})
    """


# 创建新任务
def createTask(request):
    if request.method == "POST":
        createTask_form = CreateTaskForm(request.POST)
        message = "请检查填写的内容！"
        if createTask_form.is_valid():
            title = createTask_form.cleaned_data['title']
            # title唯一
            same_title = models.Task.objects.filter(title=title)
            if same_title:
                message = "Title重复！"
                return render(request, 'AFSOC_app/CreateTask.html', locals())
            # 开发者需存在
            assignee = createTask_form.cleaned_data['assignee']
            try:
                assignee = models.Developer.objects.get(name=assignee)
            except:
                message = "请重新输入开发者！"
                return render(request, 'AFSOC_app/CreateTask.html', locals())
            # CrashFile的id需存在
            fileList = createTask_form.cleaned_data['includeFileId']
            fileList = fileList.split(',')
            for fileid in fileList:
                if not models.CrashFile.objects.filter(id=fileid):
                    message = "请重新输入CrashFile Id！"
                    return render(request, 'AFSOC_app/CreateTask.html', locals())
            # 创建新的数据
            new_Task = models.Task.objects.create(title=title)
            new_Task.state = createTask_form.cleaned_data['state']
            new_Task.description = createTask_form.cleaned_data['description']
            new_Task.priority = createTask_form.cleaned_data['priority']
            new_Task.files.set(fileList)
            new_Task.assignee = assignee
            new_Task.supervisor_id = request.session.get('user_id')
            new_Task.save()
            message = "创建新任务成功！"
            return redirect('/AFSOC_app/taskCenter')
    createTask_form = CreateTaskForm(request.GET)
    return render(request, 'AFSOC_app/CreateTask.html', locals())


"""
# 报告处理页面,改用FilteredCrashFileListView显示可过滤的页面，暂停使用
def reportHandle(request):
    if request.method == "POST":
        getCrashFiles(request.session.get('user_id'))

    crashFile_table = tables.CrashFileTable(models.CrashFile.objects.all())
    RequestConfig(request, paginate={'per_page': 20}).configure(crashFile_table)
    return render(request, 'AFSOC_app/ReportHandle.html', {'table': crashFile_table})
"""


# 自动读取文件进行分析，并分配任务
def autoAnalyzeFiles(request):
    getCrashFiles(request.session.get('user_id'))
    return redirect('/AFSOC_app/reportHandle')


"""
# 用户管理页面, 改用FilteredDeveloperListView来显示可过滤的页面，暂停使用
def userManagement(request):
    developer_table = tables.DeveloperTable(models.Developer.objects.all())
    RequestConfig(request, paginate={'per_page': 20}).configure(developer_table)
    return render(request, 'AFSOC_app/UserManagement.html', {'table': developer_table})
"""


# 显示用户个人中心
def userCenter(request):
    task_assigned = len(models.Task.objects.filter(assignee_id=request.session.get('user_id')))
    task_solved = len(models.Task.objects.filter(assignee_id=request.session.get('user_id'), state='solved'))
    return render(request, 'AFSOC_app/UserCenter.html', {'task_assigned': task_assigned, 'task_solved': task_solved})


# 新建用户
def createUser(request):
    if request.method == "POST":
        register_form = CreateUserForm(request.POST)
        message = "请检查填写的内容！"
        # 获取数据
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            permission = register_form.cleaned_data['permission']
            # 用户名唯一
            same_name_user = models.Developer.objects.filter(name=username)
            if same_name_user:
                message = "用户已经存在，请重新选择用户名！"
                return render(request, 'AFSOC_app/CreateUser.html', locals())
            # 邮箱地址唯一
            same_email_user = models.Developer.objects.filter(email=email)
            if same_email_user:
                message = "该邮箱地址已被注册，请使用别的邮箱！"
                return render(request, 'AFSOC_app/CreateUser.html', locals())
            try:
                department = models.Department.objects.get(name=register_form.cleaned_data['department'])
            except:
                message = "部门不存在，请重新填写！"
                return render(request, 'AFSOC_app/CreateUser.html', locals())
            # 所填项都符合要求，创建新用户
            new_user = models.Developer.objects.create(name=username, password=password, email=email,
                                                       permission=permission, department=department)
            message = "创建新用户成功！"
            return redirect('/AFSOC_app/userManagement')
    register_form = CreateUserForm(request.GET)
    return render(request, 'AFSOC_app/CreateUser.html', locals())


# 新建部门
def createDepartment(request):
    if request.method == "POST":
        createDepartment_form = CreateDepartmentForm(request.POST)
        if createDepartment_form.is_valid():
            departname = createDepartment_form.cleaned_data['name']
            same_department = models.Department.objects.filter(name=departname)
            if same_department:
                message = "已存在此部门！请重新输入！"
                return render(request, "AFSOC_app/CreateDepartment.html", locals())
            models.Department.objects.create(name=departname)
            return redirect('/AFSOC_app/userManagement')
    createDepartment_form = CreateDepartmentForm(request.GET)
    return render(request, "AFSOC_app/CreateDepartment.html", locals())


# 修改密码
def updatePassword(request):
    if request.method == "POST":
        updatePassword_form = UpdatePasswordForm(request.POST)
        if updatePassword_form.is_valid():
            password1 = updatePassword_form.cleaned_data['password1']
            password2 = updatePassword_form.cleaned_data['password2']
            if password1 != password2:
                message = "请输入相同的密码！"
                return render(request, 'AFSOC_app/UpdatePassword.html', locals())
            else:
                user = models.Developer.objects.get(name=request.session.get('user_name'))
                user.password = password1
                user.save()
                request.session.flush()
                message = "修改成功！请重新登陆！"
                return redirect('/AFSOC_app/index')
    updatePassword_form = UpdatePasswordForm(request.GET)
    return render(request, 'AFSOC_app/UpdatePassword.html', locals())


# 显示用户详细信息，管理员可修改内容
def developer_detail(request, pk):
    developer = get_object_or_404(models.Developer, pk=pk)
    # 获取信息并显示
    task_assigned = len(models.Task.objects.filter(assignee=developer))
    task_solved = len(models.Task.objects.filter(assignee=developer, state='solved'))
    developerInfo_form = DeveloperInfoForm(request.GET)
    if request.method == "GET":
        developerInfo_form.__init__({'username': developer.name, 'password': developer.password, 'email': developer.email,
                                 'permission': developer.permission, 'department': developer.department,
                                     'task_assigned': task_assigned, 'task_solved': task_solved})
    elif request.method == "POST":
        # 删除当前显示用户
        if 'delete' in request.POST:
            if developer.id == request.session.get('user_id'):
                developer.delete()
                request.session.flush()
                return redirect('/AFSOC_app/index')
            developer.delete()
            return redirect('/AFSOC_app/userManagement')
        # 修改当前用户信息
        elif 'change' in request.POST:
            developerInfo_form = DeveloperInfoForm(request.POST)
            if developerInfo_form.is_valid():
                developer_modify = models.Developer.objects.get(id=developer.id)
                developer_modify.name = developerInfo_form.cleaned_data['username']
                developer_modify.password = developerInfo_form.cleaned_data['password']
                developer_modify.email = developerInfo_form.cleaned_data['email']
                developer_modify.permission = developerInfo_form.cleaned_data['permission']
                developer_modify.department = developerInfo_form.cleaned_data['department']
                developer_modify.save()
                message = "修改成功！"
                return redirect("/AFSOC_app/userManagement")
    return render(request, "AFSOC_app/developer_detail.html", locals())


# 显示任务详细信息，并可修改
def task_detail(request, pk):
    task = get_object_or_404(models.Task, pk=pk)
    taskInfo_form = TaskInfoForm(request.GET)
    # 显示详情
    if request.method == "GET":
        taskInfo_form.__init__({'title': task.title, 'state': task.state, 'description': task.description,
                                'priority': task.priority, 'assignee': task.assignee, 'supervisor': task.supervisor,
                                'includeFile': task.file.subject})
    elif request.method == "POST":
        # 删除任务
        if 'delete' in request.POST:
            task.delete()
            if request.session.get('permission') == 'administrator':
                return redirect("/AFSOC_app/taskCenter_admin")
            else:
                return redirect("/AFSOC_app/taskCenter")
        # 修改任务状态
        elif 'jumpTo' in request.POST:
            taskInfo_form = TaskInfoForm(request.POST)
            if taskInfo_form.is_valid():
                state = taskInfo_form.cleaned_data['state']
                task.state = state
                if state == 'solved':
                    task.file.solved = True
                    task.file.save()
                task.save()
                message = "状态跳转成功！"
                return render(request, "AFSOC_app/task_detail.html", locals())
        # 修改任务信息
        elif 'change' in request.POST:
            taskInfo_form = TaskInfoForm(request.POST)
            if taskInfo_form.is_valid():
                try:
                    assignee = models.Developer.objects.get(name=taskInfo_form.cleaned_data['assignee'])
                    supervisor = models.Developer.objects.get(name=taskInfo_form.cleaned_data['supervisor'])
                    task_modify = models.Task.objects.get(id=task.id)
                    task_modify.title = taskInfo_form.cleaned_data['title']
                    task_modify.state = taskInfo_form.cleaned_data['state']
                    task_modify.description = taskInfo_form.cleaned_data['description']
                    task_modify.priority = taskInfo_form.cleaned_data['priority']
                    task_modify.assignee = assignee
                    task_modify.supervisor = supervisor
                    """TODO: include关系的修改"""
                    task_modify.save()
                except:
                    message = "请检查输入信息！"
                    return render(request, "AFSOC_app/task_detail.html", locals())
                message = "修改成功！"
        # 下载文件
        elif 'download' in request.POST:
            path = task.file.path
            file = open(path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(task.file.subject + ".zip")
            return response
    return render(request, "AFSOC_app/task_detail.html", locals())


# 跳转至崩溃信息详情页
def crashFile_detail(request, pk):
    crashFile = get_object_or_404(models.CrashFile, pk=pk)
    return render(request, "AFSOC_app/crashFile_detail.html", {'crashFile': crashFile})


# 获取崩溃文件信息并写入数据库
def getCrashFiles(current_user):
    dirPath = "D:\\CrashReport\\receiveFiles"
    destPath = "D:\\CrashReport\\handled"
    zipFiles = os.listdir(dirPath)
    # 新生成文件记录的id列表
    file_id_list = []
    for zipFilePath in zipFiles:
        subject = os.path.splitext(zipFilePath)[0]
        newPath = os.path.join(destPath, zipFilePath)
        # 解压压缩包中的txt文件
        zipFilePath = os.path.join(dirPath, zipFilePath)
        zFile = zipfile.ZipFile(zipFilePath, 'r', zipfile.ZIP_DEFLATED)
        fileNames = zFile.namelist()
        txtName = ''
        if len(fileNames):
            for fileName in fileNames:
                if fileName.find(".txt") > -1:
                    txtName = fileName
                    break
        zFile.extract(txtName, dirPath)
        zFile.close()

        txtName = os.path.join(dirPath, txtName)
        # 读取txt文件中的内容
        with open(txtName, 'r') as myFile:
            list1 = myFile.readlines()
            for i in range(0, len(list1)):
                list1[i] = list1[i].rstrip('\n')
        # 删去解压出的txt文件
        os.remove(txtName)
        # 将读取过的压缩包移动至handled文件夹
        shutil.move(zipFilePath, newPath)
        # 去除list中的空值
        list1 = list(filter(None, list1))
        # 在数据库中写入记录
        new_file = models.CrashFile.objects.create()
        new_file.subject = subject
        new_file.path = newPath
        new_file.software_version = list1[1]
        new_file.error_type = list1[3]
        new_file.occur_time = list1[5]
        new_file.user = list1[7]
        new_file.os_information = list1[9]
        new_file.opengl_version = list1[11]
        new_file.save()

        file_id_list.append(new_file.id)
    generateTasksAndAssign(file_id_list, current_user)


# 全局变量，分配顺序
assign_sequence = 1

# 生成任务并进行分配
def generateTasksAndAssign(file_id_list, current_user):
    task_id_list = []
    # 对每个文件都生成一个任务
    for file_id in file_id_list:
        file = models.CrashFile.objects.get(id=file_id)
        task = models.Task.objects.create(title=file.subject)
        task.description = file.software_version + "\n" + file.error_type + "\n" + file.occur_time + "\n"\
                           + file.user + "\n" + file.os_information + "\n" + file.opengl_version
        task.file = models.CrashFile.objects.get(id=file_id)
        task.save()
        task_id_list.append(task.id)
    # 计算每个开发者的任务完成速度
    speed_sum = 0.0
    global assign_sequence
    # 设置开发者排序
    if assign_sequence == 1:
        developers = models.Developer.objects.exclude(permission='administrator')
    else:
        developers = models.Developer.objects.exclude(permission='administrator').order_by('-id')
    assign_sequence = -assign_sequence
    for developer in developers:
        # 如果用户没有任务完成率，则创建一个默认值给他
        workspeed = developer.work_speed
        if not workspeed:
            workspeed = models.WorkSpeed.objects.create()
        # 用户存在任务完成率，重新进行计算
        # 现在被分配到的所有任务数量
        assigned_tasks = models.Task.objects.filter(assignee=developer)
        task_count_now = len(assigned_tasks)
        task_list = []
        for assigned_task in assigned_tasks:
            task_list.append(assigned_task.id)
        # 现在已经完成的任务数量
        finished_count_now = len(models.Task.objects.filter(id__in=task_list, state='solved'))
        # 1. 任务总数不变，完成数量有所变化
        if task_count_now == workspeed.task_count and finished_count_now != workspeed.finished_count:
            workspeed.speed += (finished_count_now - workspeed.finished_count) / workspeed.task_count
        # 2. 完成数量不变，任务总数变化
        elif task_count_now != workspeed.task_count and finished_count_now == workspeed.finished_count:
            workspeed.speed = workspeed.finished_count / task_count_now
        # 3. 任务总数和完成数量都有变化
        elif task_count_now != workspeed.task_count and finished_count_now != workspeed.finished_count:
            workspeed.speed += (finished_count_now - workspeed.finished_count) / (task_count_now - workspeed.task_count)
        # 4. 任务总数和完成数量都不变化，则无需变动

        # 如果完成速度为0 则需要调整，设定为0.1
        if workspeed.speed < 0.1:
            workspeed.speed = 0.1
        # 保存更新的数据
        workspeed.task_count = task_count_now
        workspeed.finished_count = finished_count_now
        workspeed.save()
        developer.work_speed = workspeed
        developer.save()

        speed_sum += workspeed.speed
    # 将新的任务进行分配
    assign_task_count_list = []
    new_task_count = len(task_id_list)
    for developer in developers:
        workspeed = developer.work_speed
        # 用户被分配的任务数
        assign_count = new_task_count * (workspeed.speed / speed_sum) + 1
        assign_task_count_list.append(assign_count)
    # 当任务列表不为空时，进行任务分配
    manager_list = models.Developer.objects.filter(permission='manager')
    pos = 0
    temp_count = 0
    for task_id in task_id_list:
        the_task = models.Task.objects.get(id=task_id)
        # 一个开发者已经获得该分配的任务数之后，换下一个开发者
        if temp_count >= assign_task_count_list[pos]:
            pos += 1
            temp_count = 0
        the_task.assignee = developers[pos]
        the_task.supervisor_id = current_user
        for manager in manager_list:
            if manager.department == developers[pos].department:
                the_task.supervisor = manager
                break
        the_task.save()
        temp_count += 1


# 显示文件处理的过滤页面
class FilteredCrashFileListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = tables.CrashFileTable
    table_pagination = {"per_page": 20}
    model = models.CrashFile
    template_name = "AFSOC_app/ReportHandle.html"
    filterset_class = CrashFileFilter

    export_format = "xls"


# 显示任务的过滤页面，管理员使用
class FilteredTaskListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = tables.TaskTable
    table_pagination = {"per_page": 20}
    model = models.Task
    template_name = "AFSOC_app/TaskCenter_admin.html"
    filterset_class = TaskFilter

    export_format = "xls"


# 显示用户的过滤页面
class FilteredDeveloperListView(ExportMixin, SingleTableMixin, FilterView):
    table_class = tables.DeveloperTable
    table_pagination = {"per_page": 20}
    model = models.Developer
    template_name = "AFSOC_app/UserManagement.html"
    filterset_class = DeveloperFilter

    export_format = "xls"
