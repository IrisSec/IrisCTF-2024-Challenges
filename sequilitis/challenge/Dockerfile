FROM ubuntu:22.04 as chroot

RUN /usr/sbin/useradd --no-create-home -u 1000 user
COPY flag / 
RUN sh -c 'dst=$(head -c 10 /dev/urandom | base32); mkdir $dst; mv flag $dst/flag' 

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y build-essential wget unzip

COPY chal.c /home/user/
WORKDIR /home/user/
RUN wget https://www.sqlite.org/2023/sqlite-amalgamation-3440200.zip
RUN unzip sqlite-amalgamation-3440200.zip
RUN mv sqlite-amalgamation-3440200/* .
RUN gcc chal.c sqlite3.c -lpthread -DSQLITE_OMIT_LOAD_EXTENSION -o chal -lm

FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f

COPY --from=chroot / /chroot

COPY nsjail.cfg /home/user/

CMD kctf_setup && \
    kctf_drop_privs \
    socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"kctf_pow nsjail --config /home/user/nsjail.cfg -- /home/user/chal"
