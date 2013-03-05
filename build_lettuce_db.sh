#!/bin/bash
rm -f lettuce.db
./manage.py syncdb --migrate --noinput --settings=nynjaetc.settings_lettuce
./manage.py import_from_forest --settings=nynjaetc.settings_lettuce
mv lettuce.db test_data/test.db
