# Grab the latest alpine image
FROM python:3.8-slim

# Install dependencies
ADD ./requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD ./ /opt/webapp/
WORKDIR /opt/webapp

# Run the image as a non-root user
RUN adduser --disabled-password web_user
USER web_user

EXPOSE 8000

# Run the app.
ENV PYTHONPATH "${PYTHONPATH}:app"
CMD gunicorn --bind 0.0.0.0:8000 main:app
