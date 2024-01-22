import secrets
import subprocess
from pwn import u32

#FLAG = b"irisctf{1ns3cUre_c0mput1ng_1n_s3cur3_c0mput1ng?}"
FLAG = b"irisctf{1f_0nly_s3cc0mp_c0ulD_us3_4ll_eBPF_1nstruct10ns!}"
assert len(FLAG) == 48+8+1
FLAG = FLAG[8:-1]
print(FLAG)
flag = [u32(FLAG[i:i+4]) for i in range(0, 48, 4)]

MIN_DIST = 69
# TODO threads?
FILTER_CNT = 8

# packet           sys #    arch        ip    ip      args
reg_check_packet = [0x1337, 0xc000003e, None, None] + flag
lens = []

def gen_instructions(flag=False):
    global reg_check_m, a, x, dist
    dist += 1

    # Choose class of instruction to try to emit
    choice = secrets.randbelow(1000)
    ## Load mem
    if choice < 50: # 5%
        source = secrets.randbelow(16)
        if reg_check_m[source] is None:
            return ""
        if secrets.randbelow(2): # dest
            a = reg_check_m[source]
            return f"ld M[{source}]\n"
        else:
            x = reg_check_m[source]
            return f"ldx M[{source}]\n"
        pass
    ## Load flag
    elif choice < 100: # 5%
        source = secrets.randbelow(12+2)
        if source >= 2:
            source += 2
            a = reg_check_packet[source]
            dist = 0
            #return f"ld [{source*4}]\n"
            mode = secrets.randbelow(4)
            if mode == 0:
                mask = secrets.randbelow(2**32)
                a &= mask
                return f"ld [{source*4}]\nand #{mask}\n"
            elif mode == 1:
                mask = secrets.randbelow(2**32)
                a |= mask
                return f"ld [{source*4}]\nor #{mask}\n"
            else:
                return f"ld [{source*4}]\n"
        else:
            a = reg_check_packet[source]
            dist = 0
            return f"ld [{source*4}]\n"
    ## Check
    elif choice < 150: # 5%
        if dist < MIN_DIST or not flag: return "" # require distance from load
        #chance = secrets.randbelow(16)
        #if chance > 12:
        # check a value
        mode = secrets.randbelow(3)
        token = "label" + secrets.token_hex(8)
        mask = secrets.randbelow(2**32)
        if mode == 0:
            a &= mask
            return f"and #{mask}\njeq #{hex(a)}, {token}\nret #0x00000000\n{token}:"
        if mode == 1:
            a |= mask
            return f"or #{mask}\njeq #{hex(a)}, {token}\nret #0x00000000\n{token}:"
        if mode == 2:
            mask &= 0x0000ffff
            a *= mask
            a &= 0xffffffff
            return f"mul #{mask}\njeq #{hex(a)}, {token}\nret #0x00000000\n{token}:"
    ## tax/txa
    elif choice < 175: # 2.5%
        if secrets.randbelow(2):
            x = a
            return "tax\n"
        else:
            a = x
            return "txa\n"
    ## Math
    elif choice < 900: # 72.5%
        target = secrets.randbelow(100) < 85
        mode = secrets.randbelow(4)
        if mode == 0:
            if target:
                v = secrets.randbelow(2**32)
                a ^= v
                a &= 0xffffffff
                return f"xor #{v}\n"
            else:
                a ^= x
                a &= 0xffffffff
                return f"xor %x\n"
        elif mode == 1:
            if target:
                v = secrets.randbelow(2**32)
                a += v
                a &= 0xffffffff
                return f"add #{v}\n"
            else:
                a += x
                a &= 0xffffffff
                return f"add %x\n"
        elif mode == 2:
            if target:
                v = secrets.randbelow(2**32)
                a -= v
                a &= 0xffffffff
                return f"sub #{v}\n"
            else:
                a -= x
                a &= 0xffffffff
                return f"sub %x\n"
        elif mode == 3:
            if target:
                v = secrets.randbelow(2**16)
                a *= v
                a &= 0xffffffff
                return f"mul #{v}\n"
    ## Store into memory
    elif choice < 1000: # 10%
        source = secrets.randbelow(16)
        if secrets.randbelow(1): # a
            reg_check_m[source] = a
            return f"st M[{source}]\n"
        else:
            reg_check_m[source] = x
            return f"stx M[{source}]\n"

    return ""

reg_check_m = [None] * 16 # 16 32-bit words
for filter_n in range(FILTER_CNT):
    for i in range(16): reg_check_m[i] = None
    BPF = ""
    a = 0x0
    x = 0x0
    dist = 0

    PRELUDE = """ld [0]
    jeq #0x1337, start
    ret #0x7fff0000
    start:
    """
    BPF = PRELUDE
    for _ in range(128):
        BPF += gen_instructions()
    BPF += "tax"

    ICTR = BPF.count("\n")

    p = subprocess.Popen(["./bpf_asm", "-c"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    garbage, _ = p.communicate(BPF.encode())

    PRELUDE = ""

    for i in range(16):
        c = secrets.randbelow(2**32)
        PRELUDE += f"ldi #{hex(c)}\nst M[{i}]\n"
        reg_check_m[i] = c
    PRELUDE += """
    ld #0x7aec22e4 ; load known constants
    ldx #0x5ab5ff4c
    """

    POSTLUDE = """
    ret #0x00050000
    die: ret #0x00000000
    """
    a = 0x7aec22e4
    x = 0x5ab5ff4c

    BPF = PRELUDE
    while ICTR < (4096 - 72 - 300):
        temp = gen_instructions(flag=True)
        dist += 1
        ICTR += temp.count("\n")
        BPF += temp

    # checks
    BPF += f"""
    jne #{hex(a)}, die
    txa
    jne #{hex(x)}, die
    """
    for i in range(16):
        BPF += f"ld M[{i}]\njne #{hex(reg_check_m[i])}, die\n"

    BPF += POSTLUDE

    p = subprocess.Popen(["./bpf_asm", "-c"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    assembled, _ = p.communicate(BPF.encode())
    assembled = garbage + assembled
    lens.append(assembled.count(b"\n"))

    with open(f"./bpf_chal_{filter_n}.bpf", "wb") as f:
        f.write(assembled)

with open("./bpf_chal_filters.c", "w") as f:
    for i in range(FILTER_CNT):
        f.write(f"""
struct sock_filter filter_{i}[] = {{
#include "./bpf_chal_{i}.bpf"
}};""")
    filters = ",".join(f"filter_{i}" for i in range(FILTER_CNT))
    f.write(f"struct sock_filter* filters[] = {{ {filters} }};\n")
    lens = ",".join(str(i) for i in lens)
    f.write(f"size_t filter_len[] = {{ {lens} }};")

with open("./bpf_chal_cnt.txt", "w") as f:
    f.write(str(FILTER_CNT))
