from database import Database, Note

#Após executar este programa, um arquivo chamado banco.db deve ter aparecido na sua pasta
db = Database('banco')

#db.add(Note(title='Pão doce', content='Abra o pão e coloque o seu suco em pó favorito.'))
#db.add(Note(title=None, content='Lembrar de tomar água'))

notes = db.get_all()
for note in notes:
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')

db.update(Note(title='cabeleleila leila', content='hidratracao para o cabelo e para as unhas', id=4))

db.delete(1)
db.delete(2)
db.delete(3)

notes = db.get_all()
for note in notes:
    print(f'Anotação {note.id}:\n  Título: {note.title}\n  Conteúdo: {note.content}\n')
