docker run -it --rm -v ".:/build" debian:buster bash -c "apt update && apt install -y clang && cd /build && clang++ vuln.cpp -O1 -o debug -fpie -pie -fno-stack-protector -Wl,-z,now -Wl,-z,relro"
