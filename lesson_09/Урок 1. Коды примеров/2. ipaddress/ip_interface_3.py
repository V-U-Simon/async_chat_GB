"""Python для сетевых инженеров"""

# создание объектов IPv4Interface или IPv6Interface
from ipaddress import ip_interface, ip_network

# Функция ipaddress.ip_interface() позволяет создавать
# объект IPv4Interface или IPv6Interface соответственно
IPV4_INT = ip_interface('10.0.1.1/24')

# получение адреса, маски, сети интерфейса
print(IPV4_INT.ip)
print(IPV4_INT.netmask)
print(IPV4_INT.network)

# проверка типа адреса
IP_1 = '10.0.1.1/24'
IP_2 = '10.0.1.0/24'


def ip_network_check(ip_addr):
    """Проверка, является ли адрес адресом сети или хоста"""
    try:
        ip_network(ip_addr)
        return True
    except ValueError:
        return False


print(ip_network_check(IP_1))
print(ip_network_check(IP_2))
