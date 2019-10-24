FROM python:3.7.5-slim

RUN mkdir PREFIX_MAN1

COPY requirements.txt PREFIX_MAN1/requirements.txt

RUN echo 'Acquire::http::Proxy "http://proxy.uk.labs.sophos:8080";' > /etc/apt/apt.conf
RUN apt-get update && apt-get install -y build-essential \
	cmake \
	libffi-dev

RUN pip install -r PREFIX_MAN1/requirements.txt --proxy=http://proxy.uk.labs.sophos:8080

COPY . PREFIX_MAN1

WORKDIR PREFIX_MAN1

ENTRYPOINT ["python", "app.py"]