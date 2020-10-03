# pull official base image
FROM python:3.8

# set working directory
WORKDIR /app

# install app dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# add app
COPY . ./

# start app
ENTRYPOINT [ "flask" ]
CMD [ "run", "--host=0.0.0.0"]