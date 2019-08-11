run:
	python3 app.py

babel_create_pot:
	pybabel extract -F babel.cfg -o messages.pot .

babel_create_init_languages:
	pybabel init -i messages.pot -d translations -l en
	pybabel init -i messages.pot -d translations -l de

babel_update:
	pybabel extract -F babel.cfg -o messages.pot .
	pybabel update -i messages.pot -d translations

babel_compile:
	pybabel compile -d translations
