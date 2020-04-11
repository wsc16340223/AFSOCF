# Generated by Django 3.0.4 on 2020-03-19 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrashFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(default='subject', max_length=64)),
                ('path', models.CharField(default='', max_length=512, null=True)),
                ('software_version', models.CharField(default='', max_length=64, null=True)),
                ('error_type', models.CharField(default='', max_length=64, null=True)),
                ('occur_time', models.CharField(default='', max_length=64, null=True)),
                ('user', models.CharField(default='', max_length=64, null=True)),
                ('os_information', models.CharField(default='', max_length=64, null=True)),
                ('opengl_version', models.CharField(default='', max_length=64, null=True)),
                ('solved', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'crashfile',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('permission', models.CharField(choices=[('administrator', 'administrator'), ('manager', 'manager'), ('developer', 'developer')], default='developer', max_length=64)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AFSOC_app.Department')),
            ],
            options={
                'db_table': 'developer',
            },
        ),
        migrations.CreateModel(
            name='WorkSpeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_count', models.IntegerField(default=0)),
                ('finished_count', models.IntegerField(default=0)),
                ('speed', models.FloatField(default=0.5)),
            ],
            options={
                'db_table': 'workspeed',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, unique=True)),
                ('state', models.CharField(choices=[('waiting for accepted', 'waiting for accepted'), ('accepted', 'accepted'), ('coding', 'coding'), ('testing', 'testing'), ('solved', 'solved')], default='waiting for accepted', max_length=64)),
                ('description', models.CharField(max_length=1024)),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Middle', 'Middle'), ('High', 'High'), ('Special', 'Special')], default='Middle', max_length=64)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('assignee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignee', to='AFSOC_app.Developer')),
                ('files', models.ManyToManyField(null=True, related_name='files', to='AFSOC_app.CrashFile')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervisor', to='AFSOC_app.Developer')),
            ],
            options={
                'db_table': 'task',
            },
        ),
        migrations.AddField(
            model_name='developer',
            name='work_speed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='AFSOC_app.WorkSpeed'),
        ),
    ]