import argparse
import os
import socket
import sys
from constants import *

open_ports = []


def main():
    """Метод определяет обрабатывает входящие аргументы. При отсутствии параметров -p/-c/-d завершает работу скрипта

        Raises
        ------
        Exception
            При ошибке, вознишкей в методе process_command()
    """

    script_name = os.path.basename(sys.argv[0])
    parser = argparse.ArgumentParser(usage=f'{script_name} [OPTIONS] HOST_NAME START END')
    parser.add_argument(
        "-s", "--scanner", dest="scanner", action='store_true', help="Определяет, какие TCP порты открыты в заданном диапазоне"
    )
    parser.add_argument("host_name", type=str, help="Имя хоста")
    parser.add_argument("start", type=int, help="Левая граница диапазона поиска")
    parser.add_argument("end", type=int, help="Правая граница диапазона поиска")
    args = parser.parse_args()

    if not (args.scanner or args.host_name or args.start or args.end):
        sys.exit(unexpected_input)

    try:
        check_ports(args.host_name, args.start, args.end)
    except Exception as e:
        sys.exit(e)


def check_ports(host_name, start, end):
    """Метод определяет статус портов в заданном диапазоне.

        Parameters
        ----------
        host_name: str
            имя хоста
        start: int,
            левая граница диапазона портов
        end: int,
            правая граница диапазона портов
    """

    if start < 1 or end > 65535 or start > end:
        sys.exit(unexpected_input)
    ip = socket.gethostbyname(host_name)
    for port in range(start, end + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
                sock.close()
        except ConnectionResetError:
            sys.exit("Ошибка подключения")
    if len(open_ports) == 0:
        print("Открытых портов в диапазоне {0}-{1} нет".format(start, end))
        sys.exit(0)
    print("Открытые порты в диапазоне {0}-{1}:".format(start, end))
    print(open_ports)


if __name__ == '__main__':
    main()
