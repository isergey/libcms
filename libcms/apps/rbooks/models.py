# coding: utf-8
import cPickle as pickle
from netaddr import IPAddress, IPNetwork, IPRange
from django.db import models
from django.core.exceptions import ValidationError

RANGE_TYPES = (
    (0, u'Сеть'),
    (1, u'Хост'),
    (2, u'Диапазон'),
)
class InternalAccessRange(models.Model):
    range = models.CharField(verbose_name=u'IP адрес или сеть', max_length=256,
        help_text=u'Пример. 192.168.11.11 - ip адрес; 192.168.0.0/16 - сеть; 192.168.1.1-192.168.1.10 - диапазон'
    )
    comments = models.TextField(verbose_name=u'Коментарии', max_length=512, blank=True)
    type = models.IntegerField(verbose_name=u'Тип введенного значения', choices=RANGE_TYPES)
    pickle = models.CharField(max_length=1024)
    def clean(self):
        error = False
        addr = self.range.strip()

        try:
            ip_object = IPAddress(addr)
            self.type = 1
            self.pickle = pickle.dumps(ip_object)
            return
        except Exception as e:
            error = True

        try:
            ip_object = IPNetwork(addr)
            self.type = 0
            self.pickle = pickle.dumps(ip_object)
            return
        except Exception as e:
            error = True

        try:
            addres_range = addr.split('-')
            if len(addres_range) == 2:
                ip_object = IPRange(addres_range[0].strip(), addres_range[1].strip())
                self.type = 2
                self.pickle = pickle.dumps(ip_object)
                return
        except Exception as e:
            error = True

        if error:
            raise ValidationError(u'Введеное значение не может быть сопоставлено с адресом, сетью или диапазоном')

    def get_ip_object(self):
        return pickle.loads(str(self.pickle))



def in_internal_ip(ip):
    ip = IPAddress(ip)
    addresses = InternalAccessRange.objects.all()
    for address in addresses:
        addr_obj = address.get_ip_object()

        if isinstance(addr_obj, IPNetwork) or isinstance(addr_obj, IPRange):
            if ip in addr_obj:
                return True

        if isinstance(addr_obj, IPAddress):
            if ip == addr_obj:
                return True

    return False
