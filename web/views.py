from django.shortcuts import render
from repository import models
from django.http import JsonResponse

# Create your views here.

def server(request):
    return render(request,'server.html')

def server_json(request):
    table_config = [
        {
            'q': None,
            'title': '选择',
            'display': True,
            'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
        },
        {
            'q': 'id',
            'title': 'ID',
            'display': False,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}},
        },
        {
            'q': 'hostname',
            'title': '主机名',
            'display': True,
            'text': {'tpl': '{a1}-{a2}', 'kwargs': {'a1': '@hostname', 'a2': '666'}},
        },
        {
            'q': 'sn',
            'title': '序列号',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@sn'}},
        },
        {
            'q': 'os_platform',
            'title': '系统',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@os_platform'}},
        },
        {
            'q': 'os_version',
            'title': '系统版本',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@os_version'}},
        },
        {
            'q': 'business_unit__name',
            'title': '业务线',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@business_unit__name'}},
        },
        {
            'q': None,
            'title': '操作',
            'display': True,
            'text': {'tpl': '<a href="/edit/{nid}/">编辑</a> | <a href="/del/{uid}/">删除</a> ',
                     'kwargs': {'nid': '@id', 'uid': '@id'}},
        },
    ]

    values = []
    for item in table_config:
        if item['q']:
            values.append(item['q'])

    server_list = models.Server.objects.values(*values)

    response = {
        'data_list':list(server_list),
        'table_config':table_config
    }
    return JsonResponse(response)



def disk(request):
    return render(request,'disk.html')

def disk_json(request):
    table_config = [
        {
            'q': None,
            'title': '选择',
            'display':True,
            'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
        },
        {
            'q': 'id',
            'title': 'ID',
            'display': False,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}},
        },
        {
            'q': 'slot',
            'title': '卡槽',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@slot'}},
        },
        {
            'q': 'model',
            'title': '磁盘型号',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@model'}},
        },

        {
            'q': 'capacity',
            'title': '磁盘容量GB',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@capacity'}},
        },
        {
            'q': 'pd_type',
            'title': '磁盘类型',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@pd_type'}},
        },
        {
            'q': None,
            'title': '操作',
            'display': True,
            'text': {'tpl': '<a href="/edit/{nid}/">编辑</a> | <a href="/del/{uid}/">删除</a> ',
                     'kwargs': {'nid': '@id', 'uid': '@id'}},
        },
    ]


    values = []
    for item in table_config:
        if item['q']:
            values.append(item['q'])

    disk_list = models.Disk.objects.values(*values)

    response = {
        'data_list':list(disk_list),
        'table_config':table_config
    }
    return JsonResponse(response)


# def test(request):
#     server_list = models.Server.objects.all()
#     for row in server_list:
#         print(row.id,row.hostname,row.business_unit.name,'====',row.server_status_id,row.get_server_status_id_display())
#
#     return render(request,'test.html',{''})