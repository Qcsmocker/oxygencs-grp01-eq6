# # docker build -t jfkfred/oxygencs .
# # docker tag jfkfred/oxygencs jfkfred/oxygencs:0.0.1
# # docker push jfkfred/oxygencs:latest
# # docker push jfkfred/oxygencs:0.0.1

# FROM python:3.8-alpine

# RUN pip3 install --no-cache-dir --upgrade pipenv

# WORKDIR /usr/app/

# COPY . .

# RUN pipenv install

# CMD [ "pipenv", "run", "start" ]

# -----------------------------------------------------------------------------------

#docker build -t jfkfred/oxygencs .
#docker tag jfkfred/oxygencs jfkfred/oxygencs:0.0.1
#docker push jfkfred/oxygencs:latest
#docker push jfkfred/oxygencs:0.0.1


#
# Builder
#
FROM python:3.8-alpine AS builder

RUN pip3 install --no-cache-dir --upgrade pipenv

ENV PIPENV_VENV_IN_PROJECT=1

WORKDIR /usr/app/
COPY ./Pipfile .

RUN pipenv install
RUN ls -al

#
# Application
#
FROM python:3.8-alpine

WORKDIR /usr/app/

COPY ./app .
COPY --from=builder /usr/app/.venv/ /usr/app/.venv/

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Tell docker that all future commands should run as the appuser user
USER appuser

CMD [ "./.venv/bin/python", "main.py" ]
