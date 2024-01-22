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

from pwn import *
from json import dumps

p = r

p.recvuntil(b'> ')
p.sendline(b'1')
p.recvuntil(b': ')
p.sendline(b'')

p.recvuntil(b'IV: ')
iv = p.recvline(keepends=False).decode()
p.recvuntil(b'Command: ')
cmd = unhex(p.recvline(keepends=False).decode())

payload = dumps({"from": "guest", "act": "echo", "msg": ""}).encode()
print(payload[16:32])

c1 = cmd[0:16]
cn = cmd[16:]

c1 = xor(c1, payload[16:32], b', "act": "flag",')

c_new = c1 + cn

p.recvuntil(b'> ')
p.sendline(b'2')
p.recvuntil(b'IV: ')
p.sendline(iv)
p.recvuntil(b'Command: ')
p.sendline(enhex(c_new).encode())

p.recvuntil(b'Failed to decode UTF-8: ')
decrypted = unhex(p.recvline(keepends=False).decode())

print(decrypted)
print(decrypted[0:16])
print(decrypted[16:32])

iv_new = xor(decrypted[0:16], unhex(iv), b'{"from": "admin"')

print(len(iv_new))

p.recvuntil(b'> ')
p.sendline(b'2')
p.recvuntil(b'IV: ')
p.sendline(enhex(iv_new).encode())
p.recvuntil(b'Command: ')
p.sendline(enhex(c_new).encode())

p.recvuntil(b'Congratulations! The flag is: ')
flag = p.recvline()
print("Flag:", flag)

assert b"irisctf{" in flag

exit(0)
