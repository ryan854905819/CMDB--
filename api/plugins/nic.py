from repository import models

class Nic(object):
    def __init__(self,server_obj,info):
        self.server_obj = server_obj
        self.nic_dict = info


    def process(self):
        # 网卡
        new_nic_info_dict = self.nic_dict['data']
        """
        {
            'eth0': {
                'up': True,
                'hwaddr': '00: 1c: 42: a5: 57: 7a',
                'ipaddrs': '10.211.55.4',
                'netmask': '255.255.255.0'
            }"""
        nic_disk_info_list = self.server_obj.nic.all()
        """
        [
            obj,
            obj,
            obj,
        ]
        """
        new_disk_slot_set = set(new_nic_info_dict.keys())
        old_disk_slot_set = {obj.name for obj in nic_disk_info_list}
        # add_slot_list = new_disk_slot_set - old_disk_slot_set
        add_nic_list = new_disk_slot_set.difference(old_disk_slot_set)
        del_nic_list = old_disk_slot_set.difference(new_disk_slot_set)
        update_nic_list = old_disk_slot_set.intersection(new_disk_slot_set)
        record_list = []
        if add_nic_list:
            self.add_nic(record_list,new_nic_info_dict,add_nic_list)
        if del_nic_list:
            self.del_nic(record_list,del_nic_list)
        if update_nic_list:
            self.update_nic(record_list,new_nic_info_dict,update_nic_list)

        if record_list:
            models.ServerRecord.objects.create(server_obj=self.server_obj, content=';'.join(record_list))


    def add_nic(self,record_list,new_nic_info_dict,add_nic_list):
        # 增加 [2,5]
        for nic in add_nic_list:
            value = new_nic_info_dict[nic]
            tmp = "[%s]添加[%s]网卡:%s;%s;%s"%(self.server_obj.hostname,nic,value['hwaddr'],value['ipaddrs'],value['netmask'])
            record_list.append(tmp)
            value['name'] = nic
            value['server_obj'] = self.server_obj
            models.NIC.objects.create(**value)

    def del_nic(self,record_list,del_nic_list):
        # 删除 [4,6]
        tmp = "[%s]移除[%s]网卡" % (self.server_obj.hostname,del_nic_list)
        record_list.append(tmp)
        models.NIC.objects.filter(server_obj=self.server_obj, name__in=del_nic_list).delete()

    def update_nic(self,record_list,new_nic_info_dict,update_nic_list):
        # 更新 [7,8]
        for nic in update_nic_list:
            value = new_nic_info_dict[nic]
            '''{
                'up': True,
                'hwaddr': '00: 1c: 42: a5: 57: 7a',
                'ipaddrs': '10.211.55.4',
                'netmask': '255.255.255.0'
            }'''
            obj = models.NIC.objects.filter(server_obj=self.server_obj, name=nic).first()
            for k,new_val in value.items():
                old_val = getattr(obj,k)
                if old_val != new_val:
                    record = "[%s]的[%s]网卡的[%s]由[%s]变更为[%s]" % (self.server_obj.hostname,nic,k,old_val,new_val)
                    record_list.append(record)
                    setattr(obj,k,new_val)
            obj.save()