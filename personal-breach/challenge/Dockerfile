FROM ubuntu:22.04 as chroot

RUN /usr/sbin/useradd -u 1000 user

RUN apt-get update
RUN apt-get install python3-flask -y

COPY entrypoint.sh /home/user/
RUN chmod +x /home/user/entrypoint.sh

COPY src/ /home/user/src/

CMD /home/user/entrypoint.sh

FROM gcr.io/kctf-docker/challenge@sha256:0f7d757bcda470c3bbc063606335b915e03795d72ba1d8fdb6f0f9ff3757364f
COPY --from=chroot / /chroot
COPY nsjail.cfg /home/user/
CMD kctf_setup && kctf_drop_privs nsjail --config /home/user/nsjail.cfg -- /home/user/entrypoint.sh
