import json
from repository import models
from utils.page import Pagination
from ..table_config import disk as server_conf
from .base import BaseService


class DiskService(BaseService):

    def __init__(self,request):
        self.request = request
        self.table_config = server_conf.table_config
        self.search_config = server_conf.search_config

    def fetch(self):

        current_page = self.request.GET.get('pageNum')
        total_item_count = models.Disk.objects.filter(self.condition()).count()

        page_obj = Pagination(current_page, total_item_count, per_page_count=2)

        server_list = models.Disk.objects.filter(self.condition()).values(*self.values())[page_obj.start:page_obj.end]

        response = {
            'search_config': server_conf.search_config,
            'data_list': list(server_list),
            'table_config': server_conf.table_config,
            'global_choices_dict': {

            },
            'page_html': page_obj.page_html_js()
        }
        return response

    def delete(self):
        pass

    def save(self):
        pass
