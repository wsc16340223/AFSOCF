## 1. 开发环境与工具版本

> - Windows10
> - Python3.8
> - Qt5.9.7
> - Visual Studio 2017
> - PyCharm2019.3.2

## 2. 文件结构说明

```
├─AFSOC                             项目代码
│  │  manage.py                     
│  │          
│  ├─AFSOC
│  │  │  settings.py                项目配置文件
│  │  │  urls.py                    项目路由文件
│  │  │        
│  └─AFSOC_app                      项目中的应用，主要代码
│     │  admin.py
│     │  apps.py
│     │  filters.py                 过滤器类
│     │  forms.py                   表单定义
│     │  models.py                  模型，即本设计中的实体类定义
│     │  tables.py                  表格类定义
│     │  urls.py                    应用中的路由文件
│     │  views.py                   视图文件，主要的逻辑代码，页面模板与模型的交互
│     │  
│     ├─migrations                  将模型移植到MySQL生成的文件
│     │          
│     └─templates
│        └─AFSOC_app                应用中的模板文件
│                  
├─codes
│  │  GenerateDumpFile.cpp          模拟中用来生成一个实验用的dmp文件代码
│  │  zipFiles.py                   将生成的实验用txt文件和dmp文件打包压缩的代码
│  │  
│  └─GenerateTxtFiles               生成模拟用的txt文件代码
│  ngrok-stable-windows-amd64.zip   转发本机网址的程序压缩包
│  standard.dmp                     生成的模拟用dmp文件
│  实验记录与对比.xlsx               模拟实验的结果记录与对比表格
├─images                            本设计中的图所在文件夹
├─handled                           实验用已处理的压缩包文件夹
└─receiveFiles                      实验用未进行处理的压缩包文件夹
```