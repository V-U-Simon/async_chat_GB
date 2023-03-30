# 3. Написать функцию host_range_ping_tab(),
# возможности которой основаны на функции из примера 2.
# Но в данном случае результат должен быть итоговым по всем ip-адресам,
# представленным в табличном формате (использовать модуль tabulate).
# Таблица должна состоять из двух колонок и выглядеть примерно так:
#
# Reachable
# 10.0.0.1
# 10.0.0.2
# Unreachable
# 10.0.0.3
# 10.0.0.4

from ping_range import ping_range
from tabulate import tabulate


def ping_range_tab(ip_start, ip_end):
    """
    ping some range if IP address. Only for last octet of IP.
    
    >> print(ping_range_tab('127.0.0.1', '127.0.0.3'))
    # +-------------------+---------------------+
    # | available_hosts   | unavailable_hosts   |
    # +===================+=====================+
    # | 127.0.0.1         | 127.0.0.2           |
    # +-------------------+---------------------+
    # |                   | 127.0.0.3           |
    # +-------------------+---------------------+
    """
    available_hosts, unavailable_hosts = ping_range(ip_start, ip_end)

    res = {
        'available_hosts': available_hosts,
        'unavailable_hosts': unavailable_hosts,
    }

    return tabulate(res, headers='keys', tablefmt="grid")


if __name__ == "__main__":
    print(ping_range_tab('127.0.0.1', '127.0.0.3'))