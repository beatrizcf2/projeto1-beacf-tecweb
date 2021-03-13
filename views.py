from utils import load_data, load_template, save_params, add_to_jsonfile, build_response
from urllib.parse import unquote_plus
from database import Database, Note
# urllib.parse.unquote_plus --> replace plus signs with 
# spaces, as required for unquoting HTML form values.

def index(request):
	db = Database('banco-notes')
	
	if request.startswith('POST'):
		params = save_params(request) #params = {'titulo':algm coisa, 'detalhes':outra coisa}
		#add_to_jsonfile(params, 'notes.json')
		db.add(Note(title=params['titulo'], content=params['detalhes']))
		return build_response(code=303, reason='See Other', headers='Location: /')

	else:
		# Cria uma lista de <li>'s para cada anotação
		# Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
		note_template = load_template('components/note.html')
		notes_li = [
			note_template.format(title=note.title, details=note.content)
			for note in db.get_all()
		]
		notes = '\n'.join(notes_li)
		
		return build_response(load_template('index.html').format(notes=notes))

