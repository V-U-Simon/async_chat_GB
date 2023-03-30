# 1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
# Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
# В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения («Узел доступен», «Узел недоступен»).
# При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().

import subprocess
import ipaddress
import socket


def ping(hostnames):
    available_ips = []
    unavailable_ips = []

    for hostname in hostnames:
        try:
            ip = ipaddress.ip_address(hostname)
        except ValueError:
            try:
                ip = ipaddress.ip_address(socket.gethostbyname(hostname))
            except socket.gaierror:
                print(f"Could not resolve hostname {hostname}")
                continue

        print(f"Pinging {ip}...")
        response = subprocess.run(
            ['ping', '-c', '1', '-W', '2', str(ip)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if response.returncode == 0:
            available_ips.append(str(ip))
            print(f"{ip} is available")
        else:
            unavailable_ips.append(str(ip))
            print(f"{ip} is unavailable")

    return available_ips, unavailable_ips


if __name__ == "__main__":
    hosts = ['localhost', '127.0.0.1', 'google.com', 'yandex.ru']
    available_ips, unavailable_ips = ping(hosts)