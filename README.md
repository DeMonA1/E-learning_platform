# E-learning_platform

About fixtures.
python manage.py dumpdata courses(name app) --indent=2(indentation) -> JSON in standart output

python manage.py dumpdata courses --indent=2 --ouput=courses/fixtures/subjects.json -> to the file

python manage.py loaddata subjects.json -> load data
