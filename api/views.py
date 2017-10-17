from django.shortcuts import render,HttpResponse

from django.views.decorators.csrf import csrf_exempt
import json
from repository import models
from .plugins import PluginManger
import logging
from auto_server import settings
from django.db.models import Q
from datetime import date
import hashlib
import time
#按自己思路写
# @csrf_exempt
# def service(request):
#     server_dict = json.loads(request.body.decode('utf-8'))
#     # print(type(server_dict),server_dict)
#     # 1. 检查server表中是否有当前资产信息【主机名是唯一标识】
#     #先判断主板信息是否采集成功，如果没有采集成功，data里面就不会有数据，也就拿不到主机名
#     if not server_dict['basic']['status']:
#         return HttpResponse('信息采集错误，无法获取主机名')
#     hostname = server_dict['basic']['data']['hostname']
#     # print('hostname--',hostname)
#     server_obj = models.Server.objects.filter(hostname=hostname).first()
#
#     if not server_obj:
#         basic_info = server_dict['basic']['data']
#         board_info = server_dict['board']['data']
#         basic_info.update(board_info)
#         #插入Server表数据
#         models.Server.objects.create(**basic_info)
#         server_obj = models.Server.objects.filter(hostname=hostname).first()
#         #插入Disk表数据
#         for k,disk in server_dict['disk']['data'].items():
#             disk['server_obj'] = server_obj
#             models.Disk.objects.create(**disk)
#         # 插入NIC表数据
#         for k,nic in server_dict['nic']['data'].items():
#             nic['name'] = k
#             nic['server_obj'] = server_obj
#             models.NIC.objects.create(**nic)
#         # 插入Memory表数据
#         for k,memory in server_dict['memory']['data'].items():
#             memory['server_obj'] = server_obj
#             models.Memory.objects.create(**memory)
#
#     else:
#         # 不再创建server对象，新老数据对比
#         # 硬盘
#         new_disk = server_dict['disk']['data']
#         # old_disk = server_obj.disk_set.all().values('slot', 'model', 'capacity', 'pd_type')
#         old_disk = models.Disk.objects.filter(server_obj=server_obj).values('slot', 'model', 'capacity', 'pd_type')
#         # print('old_disk',old_disk)
#         slot_list_new = []
#         slot_list_old = []
#         for slot in new_disk:
#             slot_list_new.append(slot)
#         for item in old_disk:
#             slot_list_old.append(item['slot'])
#         # print( slot_list_new , slot_list_old)
#         #新老数据对比
#
#         #存放数据变更信息
#         log_list = []
#
#         #new_disk有，old_disk没有，差集    create(**dic)
#         ret1 = set(slot_list_new)-set(slot_list_old)
#         if ret1:
#             for i in ret1:
#                 new_disk[i]['server_obj'] = server_obj
#                 models.Disk.objects.create(**new_disk[i])
#                 log = "%s主机%s卡槽添加一块盘"%(server_obj.hostname,i)
#                 print(log)
#                 log_list.append(log)
#
#         #old_disk有，new_disk没有，差集      delete
#         ret2 = set(slot_list_old)-set(slot_list_new)
#         if ret2:
#             for i in ret2:
#                 models.Disk.objects.filter(slot=i).delete()
#                 log = "%s主机%s卡槽移除一块盘" % (server_obj.hostname, i)
#                 print(log)
#                 log_list.append(log)
#         #交集old_disk有，new_disk有，需要update
#         ret3 = set(slot_list_new) & set(slot_list_old)
#         if ret3:
#             for i in ret3:
#                 obj = models.Disk.objects.filter(server_obj_id=server_obj.id,slot=i).first()
#                 if obj.model != new_disk[i]['model']:
#                     log = "%s主机%s卡槽model由%s变更为%s" % (server_obj.hostname,i,obj.model,new_disk[i]['model'])
#                     print(log)
#                     log_list.append(log)
#                     obj.model = new_disk[i]['model']
#                 if obj.capacity != float(new_disk[i]['capacity']):
#                     log = "%s主机%s卡槽capacity由%s变更为%s" % (server_obj.hostname,i,obj.capacity,new_disk[i]['capacity'])
#                     print(log)
#                     log_list.append(log)
#                     obj.capacity = new_disk[i]['capacity']
#                 if obj.pd_type != new_disk[i]['pd_type']:
#                     log = "%s主机%s卡槽pd_type由%s变更为%s" % (server_obj.hostname,i,obj.pd_type,new_disk[i]['pd_type'])
#                     print(log)
#                     log_list.append(log)
#                     obj.pd_type = new_disk[i]['pd_type']
#                 obj.save()
#         print('log','/---分隔记录---/'.join(log_list))
#
#
#     return HttpResponse('已收到')
#

#参考LS思路写


def get_log():  # 日志记录

    logger = logging.getLogger()
    fh = logging.FileHandler(r'%s\test.log' % settings.LOG_PATH)
    ch = logging.StreamHandler()  # 输出到屏幕
    formatter1 = logging.Formatter('%(asctime)s %(funcName)s [line:%(lineno)d] %(message)s')  # 设置一种日志输出格式
    fh.setFormatter(formatter1)  # 文件输出流
    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.setLevel(logging.DEBUG)  # 设置日志等级
    return logger


@csrf_exempt
def server(request):
    if request.method == "GET":
        current_date = date.today()
        # 获取今日未采集的主机列表
        host_list = models.Server.objects.filter(
            Q(Q(latest_date=None) | Q(latest_date__date__lt=current_date)) & Q(server_status_id=2)
        ).values('hostname')
        host_list = list(host_list)
        return HttpResponse(json.dumps(host_list))

    elif request.method == "POST":

        # 客户端提交的最新资产数据
        server_dict = json.loads(request.body.decode('utf-8'))
        # print(type(server_dict),server_dict)
        #获取日志对象
        logger = get_log()


        # 1. 检查server表中是否有当前资产信息【主机名是唯一标识】
        #先判断主板信息是否采集成功，如果没有采集成功，data里面就不会有数据，也就拿不到主机名
        if not server_dict['basic']['status']:
            logger.info("信息采集错误，无法获取主机名")
            return HttpResponse('信息采集错误，无法获取主机名')
        # hostname = server_dict['basic']['data']['hostname']
        # # print('hostname--',hostname)
        # server_obj = models.Server.objects.filter(hostname=hostname).first()
        #
        # if not server_obj:
        #     #创建服务器信息
        #     tmp = { }
        #     tmp.update(server_dict['basic']['data'])
        #     tmp.update(server_dict['board']['data'])
        #     server_obj = models.Server.objects.create(**tmp)
        #     #创建硬盘信息
        #     disk_info_dict = server_dict['disk']['data']
        #     for item in disk_info_dict.values():
        #         item['server_obj'] = server_obj
        #         models.Disk.objects.create(**item)
        #     # 创建内存信息
        #     men_info_dict = server_dict['memory']['data']
        #     for item in men_info_dict.values():
        #         item['server_obj'] = server_obj
        #         models.Memory.objects.create(**item)
        #     # 创建网卡信息
        #     nic_info_dict = server_dict['nic']['data']
        #     for k,v in nic_info_dict.items():
        #         v['server_obj'] = server_obj
        #         v['name'] = k
        #         models.NIC.objects.create(**v)
        # else:
        #     # 更新服务器信息
        #     tmp = {}
        #     tmp.update(server_dict['basic']['data'])
        #     tmp.update(server_dict['board']['data'])
        #     #主机名是唯一的不需要更新，所以去掉
        #     tmp.pop('hostname')
        #     #存储变更记录
        #     record_list = []
        #     for k,new_val in tmp.items():
        #         old_val = getattr(server_obj,k)
        #         if old_val != new_val:
        #             record = "[%s]的[%s]由[%s]变更为[%s]"%(hostname,k,old_val,new_val)
        #             record_list.append(record)
        #             setattr(server_obj,k,new_val)
        #     server_obj.save()
        #     if record_list:
        #         models.ServerRecord.objects.create(server_obj=server_obj,content=';'.join(record_list))
        #
        #     # 硬盘数据更新
        #     new_disk_info_dict = server_dict['disk']['data']
        #     '''
        #     '0': {
        #             'slot': '0',
        #             'pd_type': 'SAS',
        #             'capacity': '279.396',
        #             'model': 'SEAGATEST300MM0006LS08S0K2B5NV'
        #         },
        #     '''
        #     old_disk_info_list = server_obj.disk.all()  #拿到的是一个个对象
        #     new_disk_slot_set = set(new_disk_info_dict.keys())
        #     old_disk_slot_set = { obj.slot for obj in old_disk_info_list }
        #     add_slot_list = new_disk_slot_set.difference(old_disk_slot_set)
        #     del_slot_list = old_disk_slot_set.difference(new_disk_slot_set)
        #     update_slot_list = old_disk_slot_set.intersection(new_disk_slot_set)
        #
        #     #增加
        #     add_record_list = []
        #     for slot in add_slot_list:
        #         value = new_disk_info_dict[slot]
        #         tmp = '[%s]的[%s]增加一块'%(hostname,slot)
        #         add_record_list.append(tmp)
        #         value['server_obj'] = server_obj
        #         models.Disk.objects.create(**value)
        #     #删除
        #     models.Disk.objects.filter(server_obj=server_obj,slot__in=del_slot_list).delete()
        #
        #     #更新
        #     for slot in update_slot_list:
        #         value = new_disk_info_dict[slot]
        #         obj = models.Disk.objects.filter(server_obj=server_obj,slot=slot).first()
        #         for k,new_val in value.items():
        #             old_val = getattr(obj,k)
        #             if old_val != new_val:
        #                 setattr(obj,k,new_val)
        #         obj.save()
        if not server_dict['board']['status']:
            logger.info("主板信息采集错误：%s",server_dict['board']['msg'])
            return HttpResponse('主板信息采集错误')
        if not server_dict['disk']['status']:
            logger.info("disk信息采集错误: %s",server_dict['disk']['msg'])
            return HttpResponse('disk信息采集错误')
        if not server_dict['memory']['status']:
            logger.info("memory信息采集错误: %s",server_dict['memory']['msg'])
            return HttpResponse('memory信息采集错误')
        if not server_dict['nic']['status']:
            logger.info("nic信息采集错误: %s",server_dict['nic']['msg'])
            return HttpResponse('nic信息采集错误')

        manager = PluginManger()
        response = manager.exec(server_dict)

        return HttpResponse(json.dumps(response))


# ############################################## API验证示例 ##############################################
def md5(arg):
    hs = hashlib.md5()
    hs.update(arg.encode('utf-8'))
    return hs.hexdigest()

key = "asdfuasodijfoausfnasdf"
# redis,Memcache
visited_keys = {
    # "841770f74ef3b7867d90be37c5b4adfc":时间,  10
}

def api_auth(func):
    def inner(request,*args,**kwargs):
        server_float_ctime = time.time()
        auth_header_val = request.META.get('HTTP_AUTH_API')
        # 841770f74ef3b7867d90be37c5b4adfc|1506571253.9937866
        client_md5_str, client_ctime = auth_header_val.split('|', maxsplit=1)
        client_float_ctime = float(client_ctime)

        # 第一关
        if (client_float_ctime + 20) < server_float_ctime:
            return HttpResponse('时间太久了，再去买一个吧')

        # 第二关：
        server_md5_str = md5("%s|%s" % (key, client_ctime,))
        if server_md5_str != client_md5_str:
            return HttpResponse('休想')

        # 第三关：
        if visited_keys.get(client_md5_str):
            return HttpResponse('你放弃吧，不要糊弄我')

        visited_keys[client_md5_str] = client_float_ctime
        return func(request,*args,**kwargs)

    return inner


@api_auth
def test(request):
    return HttpResponse('正常用户')





















