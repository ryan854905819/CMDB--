from django.shortcuts import render
from repository import models
from django.http import JsonResponse
from utils.page import Pagination
import json
# Create your views here.

def server(request):
    return render(request,'server.html')

def server_json(request):

    search_config = [

        {'name': 'hostname__contains', 'title': '主机名', 'type': 'input'},
        {'name': 'cabinet_num', 'title': "机柜号", 'type': 'input'},
        {'name': 'server_status_id', 'title': '服务器状态', 'type': 'select', 'choice_name': 'status_choices'},

    ]

    table_config = [
        {
            'q': None,
            'title': '选择',
            'display': True,
            'text': {'tpl': '<input type="checkbox" value="{nid}" />', 'kwargs': {'nid': '@id'}},
            'attr':{'class': 'c1','k':'v','edit':'true','od':'@id'},
        },
        {
            'q': 'id',
            'title': 'ID',
            'display': False,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}},
            'attr': {'class': 'c1',},
        },
        {
            'q': 'hostname',
            'title': '主机名',
            'display': True,
            'text': {'tpl': '{a1}-{a2}', 'kwargs': {'a1': '@hostname', 'a2': '666'}},
            'attr': {'class': 'c1',},
        },
        {
            'q': 'sn',
            'title': '序列号',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@sn'}},
            'attr': {'class': 'c1',},
        },
        {
            'q': 'os_platform',
            'title': '系统',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@os_platform'}},
            'attr': {'class': 'c1',},
        },
        {
            'q': 'os_version',
            'title': '系统版本',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@os_version'}},
            'attr': {'class': 'c1',},
        },
        {
            'q': 'business_unit__name',
            'title': '业务线',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@business_unit__name'}},
            'attr': {'class': 'c1',},
        },
        {
            'q': 'server_status_id',
            'title': '服务器状态',
            'display': True,
            'text': {'tpl': '{a1}', 'kwargs': {'a1': '@@status_choices'}},
            'attr': {'class': 'c1',},
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

    # 获取搜索条件
    condition_dict = json.loads(request.GET.get('condition'))
    """
        {
            server_status_id: [1,2],
            hostname: ['c1.com','c2.com']
        }
        """
    from django.db.models import Q
    con = Q()
    #k server_status_id or hostname
    for k,v in condition_dict.items():
        temp = Q()
        temp.connector = 'OR'
        for item in v:
            temp.children.append((k, item,))
        con.add(temp,'AND')

    #获取当前的用户请求页码
    current_page = request.GET.get('pageNum')

    # 计算总显示数据条数
    total_item_count = models.Server.objects.filter(con).count()
    # 创建页码对象
    page_obj = Pagination(current_page,total_item_count,per_page_count=2)
    # 当前页码显示列表
    server_list = models.Server.objects.filter(con).values(*values)[page_obj.start:page_obj.end]

    response = {
        'data_list':list(server_list),
        'table_config':table_config,
        'global_choices_dict':{
            'status_choices':models.Server.server_status_choices
        },
        'page_html':page_obj.page_html_js(),
        'search_config': search_config,
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

def foo1(server_list):
    for row in server_list:
        for item in models.Server.server_status_choices:
            if item[0] == row['server_status_id']:
                row['server_status_id_name'] = item[1]
                break
            yield row

def test(request):
    '''
     server_status_choices = (
        (1, '上架'),
        (2, '在线'),
        (3, '离线'),
        (4, '下架'),
    )

    :param request:
    :return:
    '''
    #第一种方式
    #只要取到的是对象才可以使用row.get_server_status_id_display()这种
    # server_list = models.Server.objects.all()
    # for row in server_list:
    #     print(row.id,row.hostname,row.business_unit.name,'====',row.server_status_id,row.get_server_status_id_display())

    #第二种方式
    # server_list = models.Server.objects.all().values('hostname','server_status_id')
    # for row in server_list:
    #     for item in models.Server.server_status_choices:
    #         if item[0] == row['server_status_id']:
    #             row['server_status_id_name'] = item[1]
    #             break

    #第三种方式 使用yield生成器,推荐使用，执行次数少
    server_list = models.Server.objects.all().values('hostname', 'server_status_id')

    return render(request,'test.html',{'server_list':foo1(server_list)})