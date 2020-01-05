install:
	pip3 install -r requirements.txt --user

clean:
	rm -rf __pycache__

locust:
	locust -f locustfile.py --host=http://localhost:5000
