"""
http

tcp - port
ip - IP-adress

ip-adress:5000 -> socket

socket - интерфейс для взаимодействия с
транспортным уровнем стека протоколов TCP/IP

AF_INET - adress family IPv4 (INET), IPv6 (INET6)
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


def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    URL = parsed[1]
    return (method, URL)


def generate_headers(method, URL):
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)

    if URL not in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)


def generate_content(status_code, URL):
    if status_code == 404:
        return '<h1>404</h1> <p> Not found </p>'

    if status_code == 405:
        return '<h1>405</h1> <p> Metod not allowed </p>'

    return URLS[URL]()


def generate_response(request):
    method, URL = parse_request(request)
    headers, status_code = generate_headers(method, URL)
    body = generate_content(status_code, URL)
    HTML_code_parts = [headers, body]
    return ''.join(HTML_code_parts)


def run_server():
    # Создать новый сокет с параметрами:
    # AF_INET - протокол сетевого уровня IPv4,
    # AF_INET6 - протокол сетевого уровня IPv6,
    # SOCK_STREAM - протокол транспортного уровня TCP (STREAM - поток бит)
    # SOCK_DGRAM - протокол транспортного уровня UDP (DGRAM - датаграммы)
    # (СОкет - это то, через что можно взаимодействовать с транспотным уровнем
    # стека протоколов TCP/IP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Задать параметры сокета
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Связать сокет с IP-адресом и портом
    server_address = ('localhost', 5000)
    server_socket.bind(server_address)
    # Обявить о желании принимать соединения с очередью из одного элемента
    server_socket.listen(1)

    while True:
        # Принять запрос на установку соединения
        # (БЛОКИРУЮЩИЙ МЕТОД)
        client_socket, client_address = server_socket.accept()

        print('\nClient address:\n',
              client_address)

        # Получить данные по сети
        # (БЛОКИРУЮЩИЙ МЕТОД)
        request = client_socket.recv(1024).decode('utf-8')

        print('\nRequest from browser:\n',
              request,
              '\nEND of request from browser\n')

        if not request == '':
            response = generate_response(request)

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
