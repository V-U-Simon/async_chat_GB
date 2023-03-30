# 2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
# Меняться должен только последний октет каждого адреса.
# По результатам проверки должно выводиться соответствующее сообщение.

from ping import ping
import ipaddress


def ping_range(start_ip, end_ip):
    """
    Ping only last octet of IP address.
    mask example: 192.168.100.20 / 24
    """
    ip_list = []

    host = '.'.join(start_ip.split('.')[:-1])
    print(host)
    start = int(start_ip.split('.')[-1])
    end = int(end_ip.split('.')[-1])
    for ip in range(start, end + 1):
        try:
            ip_list.append(ipaddress.IPv4Address(f"{host}.{ip}"))
        except ipaddress.AddressValueError as e:
            print(e)
            continue

    available_ips, unavailable_ips = ping(ip_list)
    return available_ips, unavailable_ips


if __name__ == "__main__":
    available_hosts, unavailable_hosts = ping_range('127.0.0.1', '127.0.0.30')
