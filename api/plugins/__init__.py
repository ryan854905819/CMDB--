from django.conf import settings
from repository import models
import importlib
from .server import Server
import logging

class PluginManger(object):

    def __init__(self):
        self.plugin_items = settings.PLUGIN_ITEMS
        self.basic_key = "basic"
        self.board_key = "board"
        self.log = self.get_log()

    def get_log(self):  # 日志记录

        logger = logging.getLogger()
        fh = logging.FileHandler(r'%s\test.log' % settings.LOG_PATH)
        ch = logging.StreamHandler()  # 输出到屏幕
        formatter1 = logging.Formatter('%(asctime)s %(funcName)s [line:%(lineno)d] %(message)s')  # 设置一种日志输出格式
        fh.setFormatter(formatter1)  # 文件输出流
        logger.addHandler(fh)
        logger.addHandler(ch)
        logger.setLevel(logging.DEBUG)  # 设置日志等级
        return logger

    def exec(self,server_dict):
        """

        :param server_dict:
        :return: 1,执行完全成功； 2, 局部失败；3，执行失败;4. 服务器不存在
        """
        ret = {'code': 1,'msg':None}

        hostname = server_dict[self.basic_key]['data']['hostname']
        server_obj = models.Server.objects.filter(hostname=hostname).first()
        if not  server_obj:
            ret['code'] = 4
            self.log('服务器不存在:%s',ret['msg'])
            return ret
        #server单独写，属于不可插拔的插件
        obj = Server(server_obj,server_dict[self.basic_key],server_dict[self.board_key])
        obj.process()

        # 对比更新[硬盘，网卡，内存，可插拔的插件]
        for k,v in self.plugin_items.items():
            try:
                module_path,cls_name = v.rsplit('.',maxsplit=1)

                md = importlib.import_module(module_path)
                cls = getattr(md,cls_name)
                obj = cls(server_obj,server_dict[k])
                obj.process()
            except Exception as e:
                ret['code'] = 2
                self.log('局部失败:%s', ret['msg'])

        return ret

