import sqlite3
from dataclasses import dataclass


@dataclass
class Note:
	id: int = None
	title: str = None
	content: str = ''


class Database:
	def __init__(self, DB_NAME):
		DB_FILENAME = f'{DB_NAME}.db'
		self.conn = sqlite3.connect(DB_FILENAME) #conexao com a base de dados
		# execute - recebe uma string contendo um comando SQL e envia para o banco de dados.
		note = self.conn.execute("CREATE TABLE IF NOT EXISTS note (id INTEGER PRIMARY KEY, title STRING, content STRING NOT NULL);")
		
	#adiciona dados ao banco
	def add(self, note: Note):
		self.conn.execute(f"INSERT INTO note (title, content) VALUES ('{note.title}', '{note.content}');")
		self.conn.commit()

	def get_all(self):
		cursor = self.conn.execute("SELECT id, title, content FROM note")
		lista = []
		for linha in cursor:
			id = linha[0]
			title = linha[1]
			content = linha[2]
			note = Note(id,title,content)
			lista.append(note)
		return lista

	def update(self, entry: Note):
		self.conn.execute(f"UPDATE note SET title = '{entry.title}' WHERE id = {entry.id}")
		self.conn.execute(f"UPDATE note SET content = '{entry.content}' WHERE id = {entry.id}")
		self.conn.commit()

	def delete(self, note_id: int):
		self.conn.execute(f"DELETE FROM note WHERE id = {note_id};")
		self.conn.commit()
