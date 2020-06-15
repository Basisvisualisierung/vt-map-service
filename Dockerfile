FROM python:3.8.3-alpine

WORKDIR /service

RUN pip install Flask
RUN pip install flask-cors
RUN pip install gunicorn
RUN pip install pyyaml

EXPOSE 5000

COPY ./src /service

# Use only for development purposes
#ENV FLASK_APP=vt-map-service.py
#ENV FLASK_ENV=development
#ENV FLASK_DEBUG=1
#CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]

CMD ["gunicorn", "-b", "0.0.0.0:5000", "vt-map-service:service"]
