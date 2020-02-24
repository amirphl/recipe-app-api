FROM python:3.7
MAINTAINER amirphl
ENV PYTHONUNBUFFERED 1
COPY ./requirements.txt /requirements.txt

#RUN apt-get --assume-yes install postgresql-client
RUN apt-get install gcc libc-dev
#linux-headers postgres-dev
RUN pip install -r /requirements.txt
#RUN apt-get remove gcc libc-dev linux-headers postgres-dev
# when above line added you must run 'docker-compose build'

#RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8
## Install ``python-software-properties``, ``software-properties-common`` and PostgreSQL 9.3
##  There are some warnings (in red) that show up during the build. You can hide
##  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
#RUN apt-get --assume-yes update && apt-get install -y python-software-properties software-properties-common postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3
## Note: The official Debian and Ubuntu images automatically ``apt-get clean``
## after each ``apt-get``
#
## Run the rest of the commands as the ``postgres`` user created by the ``postgres-9.3`` package when it was ``apt-get installed``
#USER postgres
#
## Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
## then create a database `docker` owned by the ``docker`` role.
## Note: here we use ``&&\`` to run commands one after the other - the ``\``
##       allows the RUN command to span multiple lines.
#RUN    /etc/init.d/postgresql start &&\
#    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
#    createdb -O docker docker
#
## Adjust PostgreSQL configuration so that remote connections to the
## database are possible.
#RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf
#
## And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
#RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf
#
## Expose the PostgreSQL port
#EXPOSE 5432
#
## Add VOLUMEs to allow backup of config, logs and databases
#VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
#
## Set the default command to run when starting the container
#CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]

RUN mkdir /app
WORKDIR /app
COPY ./app /app
RUN useradd -ms /bin/bash phl
#RUN adduser phl
USER phl