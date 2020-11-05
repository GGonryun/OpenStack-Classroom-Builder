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

project:
	python ./resources/create_project.py --project-name test --username admin --role admin

network:
	python ./resources/create_network.py --domain default --project Test --name test
