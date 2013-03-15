import functools

from balancer.drivers.haproxy import haproxy_driver


class SoleVipException(Exception):
    pass


def _check_and_subst_vip(f):
    @functools.wraps(f)
    def __inner(self, virtualserver, *args, **kwargs):
        dev_extra = self.device_ref['extra']
        if 'sole_vip' in dev_extra:
            if virtualserver['address'] != dev_extra['sole_vip']:
                raise SoleVipException("VIP address is not supported")
            virtualserver = dict(virtualserver)
            if 'sole_rip' in dev_extra:
                virtualserver['address'] = dev_extra['sole_rip']
        f(self, virtualserver, *args, **kwargs)
    return __inner


class SoleVipHaproxyDriver(haproxy_driver.HaproxyDriver):
    create_virtual_ip = _check_and_subst_vip(
            haproxy_driver.HaproxyDriver.create_virtual_ip)
    delete_virtual_ip = _check_and_subst_vip(
            haproxy_driver.HaproxyDriver.delete_virtual_ip)