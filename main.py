"""
http

ip - IP-adress # аналогия - адрес дома
tcp - port # аналогия - номер квартиры

Socket - это пара IP адреса и порта (port):
ip-adress:5000 -> socket

Socket является интерфейсом для взаимодействия с
транспортным уровнем стека протоколов TCP/IP.

Сокеты бывают клиентские и серверные.

Протокол сетевого уровня:
AF_INET - adress family IPv4 (INET), IPv6 (INET6)
Протокол транспортного уровня:
SOCK_STREAM - TCP

SOL - socket level
setsockopt - set socket options
SO_REUSEADDR - socket option "reuse address"
"""

import socket
import views



URLS = {
    '/': views.index,
    '/blog': views.blog
}


def parse_http_request(http_request):
    """ Производит синтаксический разбор текста
        HTTP ЗАПРОСА,
        возвращая метод и адрес запроса
    """
    parsed = http_request.split(' ')
    method = parsed[0] # GET, POST...
    URL = parsed[1] # /wiki/HTML, wiki/HTTP...
    return (method, URL)


def generate_header(method, URL):
    """ Генерирует стартовую строку HTTP ОТВЕТА
    """
    if not method == 'GET':
        status_code = 405
        reason_phrase = 'Method not allowed'
    elif URL not in URLS:
        status_code = 404
        reason_phrase = 'Not found'
    else:
        status_code = 200
        reason_phrase = 'OK'

    # HTTP ОТВЕТ сервера
    starting_line = 'HTTP/1.1 {} {}\n\n'.format(status_code, reason_phrase)
    http_responce = starting_line
    return (http_responce, status_code)


def generate_content(status_code, URL):
    """ Генерирует тело HTTP ОТВЕТА (HTML код)
    """
    if status_code == 404:
        return '<h1>404</h1> <p> Not found </p>'
    if status_code == 405:
        return '<h1>405</h1> <p> Metod not allowed </p>'
    return URLS[URL]()


def generate_response(http_request):
    method, URL = parse_http_request(http_request)
    header, status_code = generate_header(method, URL)
    body = generate_content(status_code, URL)

    HTTP_response_parts = [header, body]
    return ''.join(HTTP_response_parts)


def run_server():
    # Создать новый сокет с параметрами:
    # AF_INET - протокол IP сетевого уровня IPv4,
    # AF_INET6 - протокол IP сетевого уровня IPv6,
    # SOCK_STREAM - протокол TCP транспортного уровня (STREAM - поток бит)
    # SOCK_DGRAM - протокол UDP транспортного уровня (DGRAM - датаграммы)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Задать параметры сокета для отключения ожидания 
    # автоматического закрытия сокета при обрыве соединения
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # socket.SOL_SOCKET - указание на текущий уровень на котором устанавливаются настройки
    # (SOL - socket level)
    # socket.SO_REUSEADDR - параметр отвечающий за переиспользование существующего адреса
    # 1 - значение параметра socket.SO_REUSEADDR (True)

    # Связать сокет с IP-адресом и портом
    server_IP_address = 'localhost'
    server_port = 5000
    server_socket_params = (server_IP_address, server_port)
    server_socket.bind(server_socket_params)

    # Обявить о желании принимать соединения 
    # с очередью из одного элемента
    server_socket.listen(1)

    while True:
        # Принять запрос на установку соединения
        client_socket, client_address = server_socket.accept() # !!!БЛОКИРУЮЩИЙ МЕТОД!!!

        print('\nClient address:\n',
              client_address)

        # Получить данные по сети
        http_request = client_socket.recv(1024).decode('utf-8') # !!!БЛОКИРУЮЩИЙ МЕТОД!!!

        print('\nhttp_request from browser:\n',
              http_request,
              '\nEND of http_request from browser\n')

        if not http_request == '':
            response = generate_response(http_request)

            print('\nResponse to browser:\n',
                  response,
                  '\nEND of response to browser\n')
            # Отправить данные по сети
            client_socket.send(response.encode())
            # Закрытие соединения
            client_socket.close()

            print('Connection closed')



if __name__ == "__main__":
    run_server()
