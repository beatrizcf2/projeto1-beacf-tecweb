'''
request = 'GET /img/logo-getit.png HTTP/1.1
Host: 0.0.0.0:8080
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Referer: http://0.0.0.0:8080/
Accept-Encoding: gzip, deflate
Accept-Language: pt-BR,pt;q=0.9,de-DE;q=0.8,de;q=0.7,en-DE;q=0.6,en;q=0.5,en-US;q=0.4'
''' 

import json
from urllib.parse import unquote_plus

#recebe uma string com a requisição e devolve a rota, excluindo o primeiro caractere (/).
def extract_route(request):
	path = request.split('\n')[0].split()[1]
	if path[0] == '/':
		return path[1:]

def read_file(path):
	if path.suffix=='.txt'or path.suffix=='.html' or path.suffix=='.js' or path.suffix=='.css':
		file = open(path, mode='r')
		return file.read().encode()
	else: 
		file = open(path, mode='rb')
		return file.read()

def load_data(json_file):
	json_path = 'data/'+json_file
	with open(json_path, "r") as read_file:
		return json.load(read_file)

def load_template(template_file):
	file_path = 'templates/'+template_file
	with open(file_path, "r") as template:
		return template.read()

#função que recebe a requisição e devolve 
#os parâmetros para desacoplar esta lógica

def save_params(request):
	request = request.replace('\r', '') #remove caracteres indesejados
	#cabeçalho e corpo estao sempre separados por duas quebras de linha
	partes = request.split('\n\n')
	corpo = partes[1] #resultado do submit titulo&detalhes
	params = {}
	for chave_valor in corpo.split('&'):
		chave_valores = unquote_plus(chave_valor).split('=') #separav titulo e descricao de seus valores
		if chave_valor.startswith('deletar'):
			params['deletar']= chave_valores[1] #vai me retornar o id
		elif chave_valor.startswith('id'):
			params['id']=chave_valores[1]
		elif chave_valor.startswith('titulo'):
			params['titulo']=chave_valores[1]
		elif chave_valor.startswith('detalhes'):
			params['detalhes']=chave_valores[1]
	print('params: ', params)
	return params


# recebe a nova anotação e a adiciona à lista do arquivo notes.json
# https://www.kite.com/python/answers/how-to-append-to-a-json-file-in-python
def add_to_jsonfile(params, json_file):
	data = load_data(json_file)
	json_path = 'data/'+json_file
	with open(json_path, "w") as file:
	    data.append(params)
	    json.dump(data, file)

#https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
def build_response(body='', code=200, reason='OK', headers=''):
	status_line = 'HTTP/1.1 '+ str(code) + ' ' + reason
	if headers != '':
		headers = '\n'+headers

	response = status_line + headers + '\n\n' + body 
	#return bytes(response, 'utf8')
	return response.encode()
	




