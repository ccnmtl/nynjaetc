MANAGE=./manage.py
APP=nynjaetc
FLAKE8=./ve/bin/flake8

jenkins: ./ve/bin/python check jshint jscs flake8 test

./ve/bin/python: requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

test: ./ve/bin/python
	$(MANAGE) jenkins --pep8-exclude=migrations

flake8: ./ve/bin/python
	$(FLAKE8) $(APP) --max-complexity=6

jshint: node_modules/jshint/bin/jshint
	./node_modules/jshint/bin/jshint media/js/chapter_marker_player.js media/js/nynjaetc.js

jscs: node_modules/jscs/bin/jscs
	./node_modules/jscs/bin/jscs media/js/chapter_marker_player.js media/js/nynjaetc.js

node_modules/jshint/bin/jshint:
	npm install jshint --prefix .

node_modules/jscs/bin/jscs:
	npm install jscs --prefix .

runserver: ./ve/bin/python check
	$(MANAGE) runserver

migrate: ./ve/bin/python check jenkins
	$(MANAGE) migrate

check: ./ve/bin/python
	$(MANAGE) check

shell: ./ve/bin/python
	$(MANAGE) shell_plus

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm celerybeat-schedule
	rm .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make check
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make check
	make test
	make migrate
	make flake8

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: ./ve/bin/python check jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate
