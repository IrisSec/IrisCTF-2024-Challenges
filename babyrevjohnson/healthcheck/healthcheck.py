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

from pwn import *

p = remote('localhost', 1337)
print(p.recvuntil(b'color: '))
p.send(b'red\n')
print(p.recvuntil(b'color: '))
p.send(b'yellow\n')
print(p.recvuntil(b'color: '))
p.send(b'green\n')
print(p.recvuntil(b'color: '))
p.send(b'blue\n')

p.recvuntil(b'food: ')
p.send(b'chicken\n')
p.recvuntil(b'food: ')
p.send(b'pasta\n')
p.recvuntil(b'food: ')
p.send(b'steak\n')
p.recvuntil(b'food: ')
p.send(b'pizza\n')
p.recvuntil(b'Correct!\n')
assert(p.read() == b'irisctf{m0r3_th4n_0n3_l0g1c_puzzl3_h3r3}')

exit(0)
