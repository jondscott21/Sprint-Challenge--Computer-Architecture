"""CPU functionality."""

import sys
import datetime

LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
DIV = 0b10100011
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001

CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
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
        self.FL = 0
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
        # print(self.ram_read(self.pc))
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

    def handle_CMP():
        # Compare the values in two registers.

        # * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.

        # * If registerA is less than registerB, set the Less-than `L` flag to 1,
        # otherwise set it to 0.

        # * If registerA is greater than registerB, set the Greater-than `G` flag
        # to 1, otherwise set it to 0.
        pass

    def handle_JMP():
        # Jump to the address stored in the given register.

        # Set the `PC` to the address stored in the given register.
        pass

    def handle_JEQ():
        # If `equal` flag is set (true),
        #  jump to the address stored in the given register.
        pass

    def handle_JNE():
        # If `E` flag is clear (false, 0), 
        # jump to the address stored in the given register.
        pass

    def run(self):
        """Run the CPU."""
        self.running = True   
        # t = datetime.datetime.now()
        while self.running:
            # if datetime.datetime.now() - t < datetime.timedelta(seconds=1):
            #     self.reg[self.IS] = 1
            IR = self.ram[self.pc]
            print("IR: ", IR)
            self.branchtable[IR]()