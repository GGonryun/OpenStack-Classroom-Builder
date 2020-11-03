# Classroom Builder
1. Prepare your classroom using the template found in `files` named tutorial.classroom.yaml.
2. Each classroom should be isolated, and should not share resources with another classroom file.
3. TODO: Run the command `make validate ./path/to/your/classroom.yaml` to validate your yaml file before creating your classroom.
4. Run the command `make classroom ./path/to/your/classroom.yaml`, without a path specified, it will deploy the test classroom.
5. All steps are idempotent except the final virtual machine step, if you re-run the same classroom script you will always receive a new set of machines, but will always use existing users, networks, and projects.