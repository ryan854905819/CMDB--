
search_config = [

            {'name': 'model__contains','title':'型号','type':'input'},
            {'name': 'capacity', 'title': "容量", 'type': 'input'},
        ]

table_config = [
            {
                'q': None,
                "display": True,
                'title': '选择',
                'text': {'tpl':'<input type="checkbox" value="{nid}" />','kwargs':{'nid': '@id' }},
                'attr':{'class':'c1','nid':'@id'},

            },
            {
                'q': 'id',
                "display": False,
                'title': 'ID',
                'text': {'tpl': '{a1}', 'kwargs': {'a1': '@id'}},
                'attr': {},
            },
            {
                'q': 'slot',
                "display": True,
                'title': '槽位',
                'text': {'tpl': '{a1}','kwargs':{'a1': '@slot'}},
                'attr': {},
            },
            {
                'q': 'model',
                'title': '型号',
                "display": True,
                'text': {'tpl': '{a1}','kwargs':{'a1': '@model'}},
                'attr': {'class': 'c1','edit':'true','origin':"@model",'name':'model'},
            },
            {
                'q': 'pd_type',
                'title': '磁盘类型',
                "display": True,
                'text': {'tpl': '{a1}','kwargs':{'a1': '@pd_type'}},
                'attr': {'class': 'c1','edit':'true','origin':'@pd_type','name':'pd_type'},
            }
        ]