"""CPU functionality."""

import sys
import datetime

LDI = 0b10000010 #130
PRN = 0b01000111 #71
MUL = 0b10100010 #162
ADD = 0b10100000 #160
SUB = 0b10100001 #161
DIV = 0b10100011 #163
HLT = 0b00000001 #1
PUSH = 0b01000101 #69
POP = 0b01000110 #70
CALL = 0b01010000 #80
RET = 0b00010001 #17

CMP = 0b10100111 #167
JMP = 0b01010100 #84
JEQ = 0b01010101 #85
JNE = 0b01010110 #86

AND = 0b10101000 #168
OR = 0b
XOR = 0b
NOT = 0b
SHL = 0b
SHR = 0b
MOD = 0b
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #  Random access memory -- ram
        self.ram = [0] * 256
        #  Process register -- reg
        self.reg = [0] * 8
        # Process counter -- pc
        self.pc = 0
        self.sp = 7
        self.IS = 6
        self.FL = [0] * 8
        self.less = 0
        self.greater = 1
        self.equal = 2
        self.reg[self.sp] = 0xF4
        self.branchtable = {}
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[SUB] = self.handle_SUB
        self.branchtable[DIV] = self.handle_DIV
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET

        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE
        self.running = False

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    # print(line)
                    comment_split = line.split("#")
                    num = comment_split[0].strip()
                    if num == "":
                        continue
                    instruction = int(num,2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op = "AND":
            self.reg[reg_a] & self.reg[reg_b]
        elif op = "OR":
            self.reg[reg_a] | self.reg[reg_b]
        elif op = "XOR":
            self.reg[reg_a] ^ self.reg[reg_b]
        elif op = "NOT":
            ~self.reg[reg_a]
        elif op = "SHL":
            self.reg[reg_a] << self.reg[reg_b]
        elif op = "SHR":
            self.reg[reg_a] >> self.reg[reg_b]
        elif op = "MOD":
            self.reg[reg_a] % self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
    
    def handle_LDI(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.reg[op_a] = op_b
        self.pc += 3

    def handle_PRN(self):
        op_a = self.ram_read(self.pc + 1)
        print(self.reg[op_a])
        self.pc += 2

    def handle_MUL(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("MUL", op_a, op_b)
        self.pc += 3

    def handle_ADD(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("ADD", op_a, op_b)
        self.pc += 3

    def handle_SUB(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("SUB", op_a, op_b)
        self.pc += 3

    def handle_DIV(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("DIV", op_a, op_b)
        self.pc += 3

    def handle_AND(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("AND", op_a, op_b)
        self.pc += 3
    def handle_OR(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("OR", op_a, op_b)
        self.pc += 3
    def handle_XOR(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("XOR", op_a, op_b)
        self.pc += 3
    def handle_NOT(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = None
        self.alu("NOT", op_a, op_b)
        self.pc += 2
    def handle_SHL(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("SHL", op_a, op_b)
        self.pc += 3
    def handle_SHR(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.alu("SHR", op_a, op_b)
        self.pc += 3
    def handle_MOD(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        if self.reg[op_b] == 0:
            print("You can not modulus by zero")
            self.running = False
        else:
            self.alu("MOD", op_a, op_b)
            self.pc += 3

    def handle_HLT(self):
        self.running = False

    def handle_PUSH(self):
        reg_idx = self.ram_read(self.pc + 1)
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.reg[reg_idx])
        self.pc += 2

    def handle_POP(self):
        reg_idx = self.ram_read(self.pc + 1)
        self.reg[reg_idx] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
        self.pc += 2
    
    def handle_CALL(self):
        val = self.pc + 2
        self.reg[self.sp] -= 1

        self.ram_write(self.reg[self.sp], val)
        op_a = self.ram_read(self.pc + 1)

        subroutine_address = self.reg[op_a]
        self.pc = subroutine_address

    def handle_RET(self):
        return_address = self.reg[self.sp]

        self.pc = self.ram_read(return_address)
        self.reg[self.sp] += 1

    def handle_CMP(self):
        # Compare the values in two registers.
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        # * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
        if self.reg[op_a] == self.reg[op_b]:
            self.FL[self.equal] = 1
        else:
            self.FL[self.equal] = 0
        # * If registerA is less than registerB, set the Less-than `L` flag to 1,
        # otherwise set it to 0.
        if self.reg[op_a] < self.reg[op_b]:
            self.FL[self.less] = 1
        else:
            self.FL[self.less] = 0
        # * If registerA is greater than registerB, set the Greater-than `G` flag
        # to 1, otherwise set it to 0.
        if self.reg[op_a] > self.reg[op_b]:
            self.FL[self.greater] = 1
        else:
            self.FL[self.greater] = 0
        self.pc += 3

    def handle_JMP(self):
        # Jump to the address stored in the given register.
        jump = self.ram_read(self.pc + 1)
        # print(jump)
        # Set the `PC` to the address stored in the given register.
        self.pc = self.reg[jump]
    def handle_JEQ(self):
        # If `equal` flag is set (true),
        #  jump to the address stored in the given register.
        if self.FL[self.equal] == 1:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else:
            self.pc += 2

    def handle_JNE(self):
        # If `E` flag is clear (false, 0), 
        # jump to the address stored in the given register.
        if self.FL[self.equal] == 0:
            self.pc = self.reg[self.ram_read(self.pc + 1)]
        else:
            self.pc += 2

    def run(self):
        """Run the CPU."""
        self.running = True   
        # t = datetime.datetime.now()
        while self.running:
            # if datetime.datetime.now() - t < datetime.timedelta(seconds=1):
            #     self.reg[self.IS] = 1
            IR = self.ram[self.pc]
            self.branchtable[IR]()