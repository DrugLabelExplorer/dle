FROM ubuntu:latest
MAINTAINER dle
RUN apt update; apt upgrade; apt -y install curl vim


# Instructions from https://yottabrain.org/database/mysql/install-mariadb-in-aws-ec2/
RUN curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | bash
RUN apt -y install mariadb-server
RUN apt -y install mariadb-client
RUN service mariadb start

COPY ./dockerfiles/* ./
