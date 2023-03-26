
from sys import exit, platform
from ipaddress import ip_address, IPv4Address, IPv6Address
from asyncio import ProactorEventLoop, set_event_loop, run, gather, create_subprocess_shell, subprocess
from tabulate import tabulate
from itertools import repeat


class AsyncPingHosts:
    def __init__(self, addresses):
        """
        Инициализация кросс-платформенной асинхронной пинг-машины
        """

        # пингуемые адреса
        self.addresses = addresses
        # доступные из них
        self.reachable = list()
        # недоступные
        self.unreachable = list()

        self._set_addresses_type()

    def _set_addresses_type(self):
        """
        Установить тип адресов в  значение ipaddress.IPv4Address или ipaddress.IPv6Address,
        если в качестве аргумента адресов указан список.
        sys.exit (1) - выход, если перехвачено исключение ValueError.
        """
        try:
            if self._is_addresses_is_list():
                self.addresses = [self._set_address_type(address) for address in self.addresses]
        except ValueError as error:
            print(error)
            exit(1)

    def _is_addresses_is_list(self):

        """
        Валидация объекта - список адресов.True, если переданный объект является списком,
        иначе вывести ValueError
        """

        if type(self.addresses) is list:
            return True
        raise ValueError(f'Passed addresses must be a list type. {type(self.addresses)} given.')

    @staticmethod
    def _set_address_type(address):
        """
        Установите тип адреса ipaddress.IPv4Address или ipaddress.IPv6Address
        """
        if not type(address) in (IPv4Address, IPv6Address):
            try:
                address = ip_address(address)
            except ValueError as error:
                print(error)
                exit(1)
        return address

    def ping_hosts(self):
        """
        Межплатформенный асинхронный пинг хоста.
        """
        print('Пожалуйста, подождите, пока не закончится пинг. '
              'Нужно около 5 сек если все адреса доступны, '
              'около 20 секунд или более в противном случае '
              'в зависимости от количества переданных адресов')

        if platform == 'win32':
            # Обратите внимание, что в Windows вы должны установить
            # цикл обработки событий в ProactorEventLoop
            loop = ProactorEventLoop()
            # запуск цикла обработки событий
            set_event_loop(loop)
            loop.run_until_complete(self._async_ping())
            loop.close()
        else:
            run(self._async_ping())

    async def _async_ping(self):
        """Получить задачи и запускать их одновременно"""
        tasks = (self._ping_host(str(address)) for address in self.addresses)
        await gather(*tasks)

    async def _ping_host(self, address):
        """
        Проверить связь с хостом и добавьте его в список
        доступных или недоступных на основе кода возврата из подпроцесса.
        """

        ping_key = self._get_ping_key()
        proc = await create_subprocess_shell(
            f'ping {ping_key} 4 {address}', stdout=subprocess.DEVNULL
        )
        await proc.communicate()
        if proc.returncode == 0:
            self.reachable.append(address)
        else:
            self.unreachable.append(address)

    @staticmethod
    def _get_ping_key():
        """
        Получить ключ для команды ping,
        которая устанавливает количество отправляемых пакетов.
        """
        key = '-c'
        if platform == 'win32':
            key = '/n'
        return key

    def get_ping_status_table(self):
        """Получить таблицу с адресами и их статусами."""
        headers = ['Address', 'Status']
        reachable = list(zip(self.reachable, repeat('reachable')))
        unreachable = list(zip(self.unreachable, repeat('unreachable')))
        return tabulate(reachable + unreachable, headers, tablefmt="github")

if __name__ == '__main__':
    # создаем объекты адресов
    FROM_ADDR = ip_address('10.0.0.1')
    TO_ADDR = ip_address('10.0.0.15')

    # диапазон пингуемых адресов
    ADDRESSES = [FROM_ADDR + i for i in range(int(TO_ADDR) - int(FROM_ADDR) + 1)]

    """
    [IPv4Address('10.0.0.1'), IPv4Address('10.0.0.2'), IPv4Address('10.0.0.3'), IPv4Address('10.0.0.4'), 
    IPv4Address('10.0.0.5'), IPv4Address('10.0.0.6'), IPv4Address('10.0.0.7'), IPv4Address('10.0.0.8'),
    IPv4Address('10.0.0.9'), IPv4Address('10.0.0.10'), IPv4Address('10.0.0.11'), IPv4Address('10.0.0.12'), 
    IPv4Address('10.0.0.13'), IPv4Address('10.0.0.14'), IPv4Address('10.0.0.15')]
    """

    ping = AsyncPingHosts(ADDRESSES)
    ping.ping_hosts()
    print(ping.get_ping_status_table())
