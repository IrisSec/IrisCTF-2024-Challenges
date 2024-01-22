from z3 import *
import re
from pwn import p32
pattern = "^\d+: [a-fx\d]+ [a-fx\d]+ [a-fx\d]+ [a-fx\d]+  (.*)$"
pattern = re.compile(pattern)
# irisctf{1ns3cUre_c0mput1ng_1n_s3cur3_c0mput1ng?}
# irisctf{1f_0nly_s3cc0mp_c0ulD_us3_4ll_eBPF_1nstruct10ns!}
s = Solver()
# 6 args 64-bit each read as 12 32-bit args
flag = [BitVec("flag%d" % i, 32) for i in range(6*2)]
print(flag)
#s.add(flag[0] == 1936290409) # iris
#s.add(flag[1] == 2070312035) # ctf{
for f in flag:
    s.add((f & 0xff) > 0x20)
    s.add((f & 0xff) < 0x80)
    s.add(((f>>8) & 0xff) > 0x20)
    s.add(((f>>8) & 0xff) < 0x7f)
    s.add(((f>>16) & 0xff) > 0x20)
    s.add(((f>>16) & 0xff) < 0x7f)
    s.add(((f>>24) & 0xff) > 0x20)
    s.add(((f>>24) & 0xff) < 0x7f)
args = [0x1337, 0xc000003e, None, None] + flag

def pv(val):
    global X
    val = val.split("= ")[1]
    if "mem" in val:
        i = val.split("[")[1].split("]")[0]
        i = int(i)
        return mem[i]
    if val == "X": return X
    if "0x" in val:
        return int(val, 16)
    return int(val)

def pp(val):
    return int(val.split("[")[1].split("]")[0])

with open("./bpf_chal", "rb") as f:
    chal = f.read()

LENS = [3796]*8
filters = []
POS = [0]
target = bytes.fromhex("15 00 01 00 37 13 00 00")
while chal.find(target, POS[-1]+1+8) > 0:
    POS.append(chal.find(target, POS[-1]+1+8)-8)
POS = POS[1:]
for i in range(8):
    pos = POS[i]
    filters.append(chal[pos:pos+LENS[i]*8])

dumps = []
import subprocess
for i, f in enumerate(filters):
    with open(f"./bpf_chal_dumped_{i}", "wb") as ff:
        ff.write(f)
    p = subprocess.Popen(["seccomp-tools", "disasm", f"./bpf_chal_dumped_{i}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    dump, _ = p.communicate()
    dumps.append(dump.decode().split("\n"))
print("Finished dumps")
#print(dumps[0])
#exit()

#with open("./bpf_chal_seccomp_dump_test.txt") as f:
for f in dumps:
    A = 0
    X = 0
    mem = [None] * 16
    skip = 0
    for line in f:
        if type(A) == int:
            A = A & 0xffffffff
        line = line.strip()
        match = pattern.match(line)
        if match is None:
            continue
        match = match.group(1)
        #skip += 1
        #if skip <= 3:
        #    continue
        #print(match)
        #print(A)
        match match:
            case "A = sys_number":
                A = args[0]
            case "A = arch":
                A = args[1]
            case _ if match.startswith("A = args["):
                val = pp(match)
                assert val < 6
                if ">>" not in match:
                    A = args[val*2 + 4] # ..
                else:
                    A = args[val*2 + 4 + 1] # ..
                #print(">>", A)
            case _ if match.startswith("A = mem["):
                val = pp(match)
                A = mem[val]
            case _ if match.startswith("mem["):
                val = pp(match)
                if match.endswith("A"):
                    mem[val] = A
                else:
                    mem[val] = X
            case _ if match.startswith("A = X"):
                A = X
            case _ if match.startswith("X = A"):
                X = A
            case _ if match.startswith("A = "):
                val = pv(match)
                A = val
            case _ if match.startswith("X = "):
                val = pv(match)
                X = val
            case _ if match.startswith("A += "):
                val = pv(match)
                A += val
            case _ if match.startswith("A -= "):
                val = pv(match)
                A -= val
            case _ if match.startswith("A *= "):
                val = pv(match)
                A *= val
            case _ if match.startswith("A /= "):
                val = pv(match)
                if type(A) == int and type(val) == int:
                    A //= val
                else:
                    if type(A) == int: A = BitVecVal(A, 32)
                    elif type(val) == int: val = BitVecVal(val, 32)
                    A /= val
            case _ if match.startswith("A &= "):
                val = pv(match)
                A &= val
            case _ if match.startswith("A |= "):
                val = pv(match)
                #print("|", A, val)
                A |= val
                #print("|", A, val)
            case _ if match.startswith("A ^= "):
                val = pv(match)
                A ^= val
            case _ if match.startswith("return"):
                pass
            case _ if match.startswith("if"):
                if "==" in match:
                    val = match.split("== ")[1].split(")")[0]
                    if "ARCH_X86_64" in val:
                        val = 0xc000003e
                    else:
                        val = int(val) if "x" not in val else int(val, 16)
                    #print(A == val)
                    if type(A == val) == bool:
                        if A != val:
                            print(A, val)
                            exit()
                        continue
                    s.add(A == val)
                else:
                    val = match.split("!= ")[1].split(")")[0]
                    if "ARCH_X86_64" in val:
                        val = 0xc000003e
                    else:
                        val = int(val) if "x" not in val else int(val, 16)
                    #print(A == val)
                    if type(A == val) == bool:
                        if A != val:
                            print(A, val)
                            exit()
                        continue

                    s.add(A == val)
            case _:
                print("unknown")
                exit()

print(s.check())
z = s.model()
l = b""
for f in flag:
    l += p32(z[f].as_long())
print(b"irisctf{" + l + b"}")

