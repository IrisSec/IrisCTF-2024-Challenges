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

from Crypto.Util.number import long_to_bytes, bytes_to_long
from pwn import xor

def ROTL(a, b):
    return (((a) << (b)) | ((a % 2**32) >> (32 - (b)))) % 2**32

def qr(x, a, b, c, d):
    x[a] += x[b]; x[d] ^= x[a]; x[d] = ROTL(x[d],16)
    x[c] += x[d]; x[b] ^= x[c]; x[b] = ROTL(x[b],12)
    x[a] += x[b]; x[d] ^= x[a]; x[d] = ROTL(x[d], 8)
    x[c] += x[d]; x[b] ^= x[c]; x[b] = ROTL(x[b], 7)

ROUNDS = 20

def chacha_block(inp):
    x = list(inp)
    for i in range(0, ROUNDS, 2):
        qr(x, 0, 4, 8, 12)
        qr(x, 1, 5, 9, 13)
        qr(x, 2, 6, 10, 14)
        qr(x, 3, 7, 11, 15)

        qr(x, 0, 5, 10, 15)
        qr(x, 1, 6, 11, 12)
        qr(x, 2, 7, 8, 13)
        qr(x, 3, 4, 9, 14)

    return [(a+b) % 2**32 for a, b in zip(x, inp)]

def chacha_init(key, nonce, counter):
    assert len(key) == 32
    assert len(nonce) == 8

    state = [0 for _ in range(16)]
    state[0] = bytes_to_long(b"expa"[::-1])
    state[1] = bytes_to_long(b"nd 3"[::-1])
    state[2] = bytes_to_long(b"2-by"[::-1])
    state[3] = bytes_to_long(b"te k"[::-1])

    key = bytes_to_long(key)
    nonce = bytes_to_long(nonce)

    for i in range(8):
        state[i+4] = key & 0xffffffff
        key >>= 32

    state[12] = (counter >> 32) & 0xffffffff
    state[13] = counter & 0xffffffff
    state[14] = (nonce >> 32) & 0xffffffff
    state[15] = nonce & 0xffffffff

    return state

buffer = []
def encrypt(data):
    global state, buffer

    output = []
    for b in data:
        if len(buffer) == 0:
            buffer = b"".join(long_to_bytes(x).rjust(4, b"\x00") for x in state)
            state = chacha_block(state)
        output.append(b ^ buffer[0])
        buffer = buffer[1:]
    return bytes(output)

a = b"a"*64
r.recvuntil(b"> ")
r.sendline(b"1")
r.recvuntil(b"? ")
r.sendline(a)
cA = bytes.fromhex(r.recvline().decode())
r.sendlineafter(b"> ", b"2")
cB = bytes.fromhex(r.recvline().decode())
initState = xor(cA, a)
initState = [bytes_to_long(initState[i:i+4]) for i in range(0, 64, 4)]
state = initState
encrypt(a)
flag = encrypt(cB)
assert flag == b"irisctf{initialization_is_no_problem}"

exit(0)
