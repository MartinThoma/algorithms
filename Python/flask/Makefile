run:
	gunicorn --bind 0.0.0.0:5000 wsgi:app
test:
	ab -l -s 30 -c 200 -n 200 -v 1 http://localhost:5000/
