import json
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from repository import models
from .service.server import ServerService
from .service.disk import DiskService

# Create your views here.

def server(request):
    return render(request,'server.html')
def server_json(request):

    service = ServerService(request)
    if request.method == "GET":

        response = service.fetch()
        return JsonResponse(response)

    elif request.method == "DELETE":

        response = service.delete()
        return HttpResponse(json.dumps(response))

    elif request.method == "PUT":
        response = service.save()
        return HttpResponse(json.dumps(response))

def disk(request):
    return render(request,'disk.html')

def disk_json(request):
    service = DiskService(request)

    if request.method == "GET":
        response = service.fetch()
        return HttpResponse(json.dumps(response))













#测试使用代码
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