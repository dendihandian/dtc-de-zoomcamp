FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py 

# In Dockerfiles, an ENTRYPOINT instruction is used to set executables that will always run when the container is initiated.
ENTRYPOINT [ "python", "ingest_data.py" ]