FROM python:3.6

# Install app dependencies
COPY /requirements.txt ./
RUN pip install -r requirements.txt
# Copy files and run project.
COPY ./ ./ 
ENTRYPOINT  [ "python", "server.py" ]