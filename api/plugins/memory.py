from repository import models

class Memory(object):
    def __init__(self,server_obj,info):
        self.server_obj = server_obj
        self.memory_dict = info


    def process(self):
        # 内存
        new_memory_info_dict =  self.memory_dict['data']
        """
        {
            'DIMM#0': {
                'capacity': 1024,
                'slot': 'DIMM#0',
                'model': 'DRAM',
                'speed': '667MHz',
                'manufacturer': 'NotSpecified',
                'sn': 'NotSpecified'
            },
            'DIMM#1': {
                'capacity': 0,
                'slot': 'DIMM#1',
                'model': 'DRAM',
                'speed': '667MHz',
                'manufacturer': 'NotSpecified',
                'sn': 'NotSpecified'
            },
       """
        new_memory_info_list = self.server_obj.memory.all()
        """
        [
            obj,
            obj,
            obj,
        ]
        """
        new_memory_slot_set = set(new_memory_info_dict.keys())
        old_memory_slot_set = {obj.slot for obj in new_memory_info_list}
        # add_slot_list = new_disk_slot_set - old_disk_slot_set
        add_slot_list = new_memory_slot_set.difference(old_memory_slot_set)
        del_slot_list = old_memory_slot_set.difference(new_memory_slot_set)
        update_slot_list = old_memory_slot_set.intersection(new_memory_slot_set)
        record_list = []
        if add_slot_list:
            self.add_memory(record_list,new_memory_info_dict,add_slot_list)
        if del_slot_list:
            self.del_memory(record_list,del_slot_list)
        if update_slot_list:
            self.update_memory(record_list,new_memory_info_dict,update_slot_list)

        if record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(record_list))


    def add_memory(self,record_list,new_memory_info_dict,add_slot_list):
        # 增加 [2,5]
        for slot in add_slot_list:
            value = new_memory_info_dict[slot]
            tmp = "[%s]添加[%s]卡槽内存:%s;%s;%s;%s;%s"%(self.server_obj.hostname,value['slot'],value['capacity'],value['model'],value['speed'],value['manufacturer'],value['sn'])
            record_list.append(tmp)
            value['server_obj'] = self.server_obj
            models.Memory.objects.create(**value)

    def del_memory(self,record_list,del_slot_list):
        # 删除 [4,6]
        tmp = "[%s]移除[%s]卡槽内存" % (self.server_obj.hostname,del_slot_list)
        record_list.append(tmp)
        models.Memory.objects.filter(server_obj=self.server_obj, slot__in=del_slot_list).delete()

    def update_memory(self,record_list,new_memory_info_dict,update_slot_list):
        # 更新 [7,8]
        for slot in update_slot_list:
            value = new_memory_info_dict[slot]
            '''
            {
                'capacity': 1024,
                'slot': 'DIMM#0',
                'model': 'DRAM',
                'speed': '667MHz',
                'manufacturer': 'NotSpecified',
                'sn': 'NotSpecified'
            }
            '''
            obj = models.Memory.objects.filter(server_obj=self.server_obj, slot=slot).first()
            for k,new_val in value.items():
                if k == 'capacity':
                    new_val=int(new_val)
                old_val = getattr(obj,k)
                if old_val != new_val:
                    record = "[%s]的[%s]卡槽内存的[%s]由[%s]变更为[%s]" % (self.server_obj.hostname,slot,k,old_val,new_val)
                    record_list.append(record)
                    setattr(obj,k,new_val)
            obj.save()