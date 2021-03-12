import socket
from pathlib import Path
from utils import extract_route, read_file, build_response
from views import index

CUR_DIR = Path(__file__).parent

# As constantes SERVER_HOST e SERVER_PORT definem o endereço do servidor (no caso, 0.0.0.0) e a porta.
# Um computador pode ser acessado via rede através de uma porta.
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

#separando a responsabilidade do modelo (lista de anotações) da responsabilidade de visualização (string HTML)
# é o padra que as notas vao seguir


# O módulo socket é utilizado para lidar com chamadas de rede em baixo nível
# código a baixo diz para o programa se conectar à porta desejada e aguardar requisições
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

# serve para que o servidor seja capaz de responder mais do que uma requisição
#podemos recarregar a página no navegador quantas vezes quisermos e ela continuará a ser recebida.
while True: 
	client_connection, client_address = server_socket.accept()

	# lendo os dados enviados pelo cliente. 
	# No comando utilizado indicamos que queremos ler no máximo 1024 bytes
	# O .decode() deixa a requisicao possivel de entender
	# é o cabeçalho (header) da requisição ou resposta
	request = client_connection.recv(1024).decode()
	
	print(request)
	
	route = extract_route(request)

	filepath = CUR_DIR/route
	
	if filepath.is_file():
		response = build_response() + read_file(filepath)
	elif route == '':
		response = index(request)
	else:
		response = build_response()
		
	#serve para devolver a pagina html
	#envia as respostas
	# O código 200 é um dos possíveis códigos de status resposta. 
	#Ele diz para o navegador que a requisição foi processada com sucesso.

	client_connection.sendall(response)

	client_connection.close()

server_socket.close()

