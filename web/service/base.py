import json
class BaseService(object):
    def values(self):
        values = []
        for item in self.table_config:
            if item['q']:
                values.append(item['q'])
        return values

    def condition(self):
        # 获取搜索条件
        condition_dict = json.loads(self.request.GET.get('condition'))
        """
            {
                server_status_id: [1,2],
                hostname: ['c1.com','c2.com']
            }
            """
        from django.db.models import Q
        con = Q()
        # k server_status_id or hostname
        for k, v in condition_dict.items():
            temp = Q()
            temp.connector = 'OR'
            for item in v:
                temp.children.append((k, item,))
            con.add(temp, 'AND')
        return con