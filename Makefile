get:
	git reset --hard HEAD
	git pull
send:
	git add .
	git commit -m "$(M)"
	git push

run:
	python engine.py ./files/demo.classroom.yaml

domain:
	python ./resources/create_domain.py --id default
