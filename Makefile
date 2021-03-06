DOMAIN = default
PROJECT = Test
NAME = test
USERNAME = admin
ROLE = admin
FILE = ./files/demo.classroom.yaml

update:
	git reset --hard origin/main
	
send:
	git add .
	git commit -m "$(M)"
	git push

classroom:
	. ~/admin.sh
	python engine.py $(FILE)

domain:
	python ./resources/create_domain.py --id $(DOMAIN)

project:
	python ./resources/create_project.py --project-name $(PROJECT) --username $(USERNAME) --role $(ROLE)

network:
	python ./resources/create_network.py --domain $(DOMAIN) --project $(PROJECT) --name $(NAME)

subnet:
	python ./resources/create_subnet.py --domain $(DOMAIN) --project $(PROJECT) --name $(NAME) --network-id $(NID) --cidr 10.10.10.0/24

router:
	python ./resources/create_router.py --domain $(DOMAIN) --project $(PROJECT) --name $(NAME) --internal-sid $(ISID) --external-nid $(NID) --external-sid $(ESID) --ip $(IP)
