import io
import math
import base64
import struct
import sys
from binarystream import BinaryStream

class VMFuncEntry:
    def __init__(self, br: BinaryStream):
        if br != None:
            self.address = br.readU32()
            self.name = br.readS()

class VMStackState:
    def __init__(self, ip: int, regs: list[int]):
        self.ip = ip
        self.regs = regs

class VM:
    def __init__(self, br: BinaryStream):
        self.mem = bytearray(bytes([0]*512))
        self.regs = [0]*9
        self.call_stack: list[VMStackState] = []

        if br == None:
            self.br = BinaryStream(io.BytesIO(b""))
            self.size = 0
            self.magic = 0x4d564c4d
            self.funs = []
        else:
            self.br = br
            #self.br.seek(0, 2)
            self.size = self.br.base_stream.getbuffer().nbytes
            print(self.size)
            #self.br.seek(0)

            self.magic = br.readU32()
            if self.magic != 0x4d564c4d:
                raise Exception('Invalid magic')
            
            self.funs = []
            fun_count = br.readI32()
            for _ in range(fun_count):
                self.funs.append(VMFuncEntry(br))
    
    def find_fun(self, name: str):
        fun = next((f for f in self.funs if f.name == name), None)
        return fun
    
    def find_fun_addr(self, addr: int):
        fun = next((f for f in self.funs if f.address == addr), None)
        return fun

    def call_fun(self, name: str):
        fun = self.find_fun(name)
        if fun == None:
            self.dump(f'Function {name} does not exist')
        
        #self.call_stack.append(VMStackState(fun.address, self.regs.copy()))
        #print(f"calling from 0x{self.br.tell():x} {self.regs}")
        self.call_stack.append(VMStackState(self.br.tell(), self.regs.copy()))
        self.br.seek(fun.address)
    
    def ret_fun(self):
        r8 = self.regs[8]
        top_stack = self.call_stack.pop()
        #print(f"returning to 0x{top_stack.ip:x} {top_stack.regs}")
        self.regs = top_stack.regs
        self.regs[8] = r8
        self.br.seek(top_stack.ip)
    
    def to_signed_32bit(self, value):
        return (value + 2**31) % 2**32 - 2**31

    def dump(self, reason: str):
        s = f'Fatal exception!!! Cause: {reason}\n'
        for i in range(len(self.regs) // 2):
            s += f'  r{i*2} = {self.regs[i*2]}, r{i*2+1} = {self.regs[i*2+1]}\n'
        
        s += f'  a = {self.regs[8]}\n'
        
        ip_extra = ''
        if len(self.call_stack) > 0:
            last_call = self.call_stack.pop()
            fun_addr = self.find_fun_addr(last_call)
            if fun_addr != None:
                ip_extra = f' ({fun_addr.name})'
                
        s += f'  ip = 0x{self.br.tell():x}{ip_extra}\n'

        for i in range(math.ceil(len(self.mem) // 16)):
            s += f'  mem[{str(i).zfill(2)}] = {self.mem[i*16:i*16+16].hex(" ")}\n'
        
        print(s)
        exit(1)

    def step(self):
        try:
            return self.step_inner()
        except struct.error:
            self.dump('Ran out of bytes to read')
        except Exception as e:
            self.dump(str(e))
        
        return True

    def step_inner(self):
        ip = self.br.tell()
        if ip >= self.size:
            return True
        
        opc = self.br.readUC()
        match opc:
            case 0xc0: # mov
                idx = self.br.readUC()
                val = self.regs[self.br.readUC()]
                self.regs[idx] = val
            case 0xc1: # movc
                idx = self.br.readUC()
                val = self.br.readI32()
                self.regs[idx] = val
            case 0xc2: # add
                self.regs[8] += self.regs[self.br.readUC()]
                self.regs[8] = self.to_signed_32bit(self.regs[8])
            case 0xc3: # sub
                self.regs[8] -= self.regs[self.br.readUC()]
                self.regs[8] = self.to_signed_32bit(self.regs[8])
            case 0xc4: # mul
                self.regs[8] *= self.regs[self.br.readUC()]
                self.regs[8] = self.to_signed_32bit(self.regs[8])
            case 0xc5: # div
                self.regs[7] = self.regs[8] % self.regs[self.br.readUC()]
                self.regs[8] //= self.regs[self.br.readUC()]
                self.regs[7] = self.to_signed_32bit(self.regs[7])
                self.regs[8] = self.to_signed_32bit(self.regs[8])
            case 0xc6: # and
                self.regs[8] &= self.regs[self.br.readUC()]
                self.regs[8] = self.to_signed_32bit(self.regs[8])
            case 0xc7: # or
                self.regs[8] |= self.regs[self.br.readUC()]
                self.regs[8] = self.to_signed_32bit(self.regs[8])
            case 0xc8: # xor
                self.regs[8] ^= self.regs[self.br.readUC()]
                self.regs[8] = self.to_signed_32bit(self.regs[8])
            case 0xc9: # shl
                self.regs[8] <<= self.regs[self.br.readUC()]
                self.regs[8] = self.to_signed_32bit(self.regs[8])
            case 0xca: # shr
                self.regs[8] >>= self.regs[self.br.readUC()]
                self.regs[8] = self.to_signed_32bit(self.regs[8])
            case 0xd0: # print
                str_pos = self.br.readU32()
                tmp_pos = self.br.tell()
                self.br.seek(str_pos)
                s = self.br.readS()
                print(s, end='')
                self.br.seek(tmp_pos)
            case 0xd1: # print_char
                c = chr(self.regs[self.br.readUC()])
                print(c, end='')
            case 0xd2: # print_number
                c = self.regs[self.br.readUC()]
                print(c, end='')
            case 0xd3: # read_line
                mem_pos = self.regs[self.br.readUC()]
                mem_left = self.regs[self.br.readUC()]
                res = input()
                if res == "<<DIE>>":
                    self.dump('User terminated program')
                
                for c in res:
                    if mem_pos > len(self.mem) - 1 - 4:
                        self.dump('Invalid memory access')
                    
                    self.mem[mem_pos] = ord(c)
                    mem_pos += 1
                    mem_left -= 1
                    if mem_pos >= len(self.mem) - 1 or mem_left == 0:
                        self.mem[mem_pos] = 0
                        break
            case 0xd4: # read_mem                
                offset = self.regs[self.br.readUC()]
                if offset > len(self.mem) - 1 - 4:
                    self.dump('Invalid memory access')
                
                self.regs[8] = struct.unpack_from('<i', self.mem, offset)[0]
            case 0xd5: # write_mem
                offset = self.regs[self.br.readUC()]
                if offset > len(self.mem) - 1 - 4:
                    self.dump('Invalid memory access')
                
                struct.pack_into('<i', self.mem, offset, self.regs[8])
            case 0xe0: # jmp
                addr = self.br.readU32()
                self.br.seek(addr)
            case 0xe1: # jmpneq
                addr = self.br.readU32()
                a = self.regs[8]
                b = self.regs[self.br.readUC()]
                if a != b:
                    self.br.seek(addr)
            case 0xe2: # jmpeq
                addr = self.br.readU32()
                a = self.regs[8]
                b = self.regs[self.br.readUC()]
                if a == b:
                    self.br.seek(addr)
            case 0xe3: # jmpgt
                addr = self.br.readU32()
                a = self.regs[8]
                b = self.regs[self.br.readUC()]
                if a > b:
                    self.br.seek(addr)
            case 0xe4: # jmplt
                addr = self.br.readU32()
                a = self.regs[8]
                b = self.regs[self.br.readUC()]
                if a < b:
                    self.br.seek(addr)
            case 0xe5: # jmpgte
                addr = self.br.readU32()
                a = self.regs[8]
                b = self.regs[self.br.readUC()]
                if a >= b:
                    self.br.seek(addr)
            case 0xe6: # jmplte
                addr = self.br.readU32()
                a = self.regs[8]
                b = self.regs[self.br.readUC()]
                if a <= b:
                    self.br.seek(addr)
            case 0xf0: # call
                str_pos = self.br.readU32()
                tmp_pos = self.br.tell()
                self.br.seek(str_pos)
                s = self.br.readS()
                self.br.seek(tmp_pos)
                self.call_fun(s)
            case 0xf1: # return
                self.ret_fun()
            case 0xf2: # exit
                return True
            case _: # crash
                self.dump('Invalid opcode')
        
        return False

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'rb') as f:
            br = BinaryStream(f)
            try:
                vm = VM(br)
            except:
                print('Invalid header')
                exit(1)
            
            vm.call_fun('main')
            ctr = 0
            while True:
                xit = vm.step()
                if xit:
                    exit()
                
                ctr += 1
                if ctr == 0x1000000:
                    print('Too many cycles')
                    exit()
    else:
        prog_hex = input('Send a program, base64 encoded: ')
        prog_hex = prog_hex.replace(' ', '')
        if len(prog_hex) > 4096 * 2:
            print('Program too big')
            exit(1)
        
        prog = io.BytesIO(base64.b64decode(prog_hex))
        br = BinaryStream(prog)
        try:
            vm = VM(br)
        except:
            print('Invalid header')
            exit(1)
        
        vm.call_fun('main')
        ctr = 0
        while True:
            xit = vm.step()
            if xit:
                exit()
                
            ctr += 1
            if ctr == 0x1000000:
                print('Too many cycles')
                exit()
