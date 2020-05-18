"""CPU functionality."""

import sys

# need to make my op codes for translation of the functions below
# if using binary to match decimal style being saved need to have
# the starting zeros removed when saving then to the ops code below

LDI = 0b10000010  # load immediate - goes into a reg
PRN = 0b01000111  # prints a number from reg
HLT = 0b1  # stops program
PUSH = 0b1000101
POP = 0b1000110
CMP = 0b10100111
JNE = 0b01010110
JMP = 0b01010100
JEQ = 0b01010101  # ls8.spec.md line 344
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
INC = 0b1100101
DEC = 0b1100110
AND = 0b10101000
NOT = 0b1101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101
CALL = 0b01010000
RET = 0b00010001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8  # this emulator only has * registers
        # r5 = interrupt mask ((IM))
        # r6 = interrupt status (IS)
        # r7 is reserved as the stack pointer
        self.ram = [0] * 256  # ram is the memory i believe so far
        self.pc = 0  # this is the Program Counter... points to the location in memory at what program to read...current action
        self.running = True  # sets this as a starter flag for the loop to run
        self.SP = 7
        self.reg[self.SP] = len(self.ram)-1
        self.FL = ''
        # FL: BITS: 00000LGE Less-than, Greater-than, Equal if reg_a is one those to reg_b as 1 or if false 0
        # this is a flag '00000LGE' see LS8-spec.md line 27 on what to set for each: <, >, ==
        # self.reg[self.FL] = '00000000'
        # self.IM = 5  # for interrupt mask
        # self.reg[self.IM] = 'n/a'  # need to look into how to set this up
        # self.IS = 6  # for interrupt status
        # # this may not be how to handle this... ls8-spec.md line 307 & 322-338?
        # self.reg[self.IS] = False
        self.branchtable = {}
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[MUL] = self.MUL
        self.branchtable[HLT] = self.HLT
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[POP] = self.POP
        self.branchtable[CALL] = self.CALL
        self.branchtable[RET] = self.RET
        self.branchtable[ADD] = self.ADD
        self.branchtable[CMP] = self.CMP
        self.branchtable[JMP] = self.JMP
        self.branchtable[JEQ] = self.JEQ
        self.branchtable[JNE] = self.JNE

    def get_number(self, list):
        add_up = 0
        if list[0] == '1':
            add_up += 128
        if list[1] == '1':
            add_up += 64
        if list[2] == '1':
            add_up += 32
        if list[3] == '1':
            add_up += 16
        if list[4] == '1':
            add_up += 8
        if list[5] == '1':
            add_up += 4
        if list[6] == '1':
            add_up += 2
        if list[7] == '1':
            add_up += 1
        return bin(add_up)

    def load(self):
        # may be a good idea to set this up with a
        # default as sys.argv[1] which is the file after
        # "python ls8.py [sys.argv file name here]"
        """Load a program into memory."""
        address = 0
        # print(sys.argv)
        if len(sys.argv) != 2:
            print("to enter a file to run")
            sys.exit(1)
        filename = sys.argv[1]
        with open(filename) as f:
            for line in f:
                if line == '':
                    continue
                comment_split = line.split('#')
                num = comment_split[0].strip()
                new_num = num
                if len(new_num) > 2:
                    num = new_num
                    num = int(num, 2)
                    # print(bin(num))
                    self.ram[address] = num
                    address += 1

    def ADD(self):
        self.pc += 1
        reg_a = self.ram[self.pc]
        self.pc += 1
        reg_b = self.ram[self.pc]
        val1 = self.reg[reg_a]
        val2 = self.reg[reg_b]
        new_value = val1 + val2
        self.reg[reg_a] = new_value
        self.pc += 1

    def SUB(self):
        # this may need adjustment..
        # don't think binary handles neg numbers...
        # we'll see i guess
        self.pc += 1
        reg_a = self.ram[self.pc]
        self.pc += 1
        reg_b = self.ram[self.pc]
        val1 = self.reg[self.ram[reg_a]]
        val2 = self.reg[self.ram[reg_b]]
        new_val = val1 - val2
        self.reg[reg_a] = new_val
        self.pc += 1

    def MUL(self):
        self.pc += 1
        reg_a = self.ram[self.pc]
        self.pc += 1
        reg_b = self.ram[self.pc]
        val1 = self.reg[reg_a]
        val2 = self.reg[reg_b]
        new_val = val1 * val2
        self.reg[reg_a] = new_val
        self.pc += 1

    def DIV(self):
        self.pc += 1
        reg_a = self.ram[self.pc]
        self.pc += 1
        reg_b = self.ram[self.pc]
        val1 = self.reg[reg_a]
        val2 = self.reg[reg_b]
        val1 /= val2
        self.pc += 1

    def DEC(self):
        # for subtracting 1 from the value stored in given reg
        # self.decrement(self.reg[regNumber])
        reg_a = self.ram[self.pc+1]
        value = self.reg[reg_a]
        print(value)
        value -= 1
        print(value)
        self.reg[reg_a] = value
        self.pc += 2

    def LDI(self):  # in run()
        # print(f" from LDI self.pc: {self.pc}")
        self.pc += 1
        register_number = self.ram[self.pc]
        rg = register_number
        self.pc += 1
        self.reg[rg] = self.ram[self.pc]
        value_string = self.reg[rg]
        vs = value_string
        self.reg[rg] = vs
        self.pc += 1

    def HLT(self):
        # print("working from branctable fn's\nGOODBYE!")
        self.running = False

    def PRN(self):  # in run()
        the_P = self.ram[self.pc+1]
        print_it = self.reg[the_P]
        print(print_it)
        self.pc += 2

    def PUSH(self):
        # print(f"pushy")
        # my SP is the index at the end of the self.ram
        # get reg from memory
        register = self.ram[self.pc + 1]
        # decrement the Stack Pointer
        self.reg[self.SP] -= 1
        # read the next value for register location
        registerV = self.reg[register]
        # take the value in that reg and add to stack
        # print(f"new stack pointer: ", self.reg[self.SP])
        self.ram[self.reg[self.SP]] = registerV
        # looking to see it was added at the end there
        # print(self.ram)
        self.pc += 2

    def POP(self):
        # pop the reg
        value = self.ram[self.reg[self.SP]]
        register = self.ram[self.pc + 1]
        # pop the value of stack location SP
        self.reg[register] = value
        # store the value into register given
        # increment the SP
        self.reg[self.SP] += 1
        # print(f"new stack pointer: {self.reg[self.SP]}")
        self.pc += 2

    def CALL(self):

        # push this to stack
        # when pushing to the stack need to move the pointer as it build down
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.pc+2
        register = self.ram[self.pc+1]
        self.pc = self.reg[register]

    def RET(self):
        # print(
        #     f"in RET FN SP:{self.SP}\n\n memory at SP: {self.ram[self.reg[self.SP]]}")
        # pop the current value off stack
        return_address = self.ram[self.reg[self.SP]]
        # should be return the address from the stack to point to set self.pc
        self.reg[self.SP] += 1  # sudo poping so need to increment
        # then set the self.pc
        # print(f"return_address: {return_address}")
        self.pc = return_address

    def CMP(self):
        # print(f"inside CMP")
        value1 = self.reg[self.ram[self.pc + 1]]
        value2 = self.reg[self.ram[self.pc + 2]]
        # are they equal... it's all tests are asking for... don't get too complicated here
        if value1 == value2:
            # self.reg[4] = True
            # switded to internal reg and not of the r0-r7
            self.FL = True
        else:
            # print('false')
            # switded to internal reg and not of the r0-r7
            self.FL = False
        self.pc += 3

    def JEQ(self):
        # print(f"inside of JEQ")
        # if true jump to address in r2
        # if self.reg[4] == True:
        if self.FL == True:
            # jump to next test
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2

    def JMP(self):
        # print(f"inside of JMP")
        # print(f"reg 2 pc {self.reg[self.ram[self.pc+1]]}")
        # pulls the new self.pc from self.reg[2]
        self.pc = self.reg[self.ram[self.pc + 1]]
        # get self.reg[2] from next spot in memory

    def JNE(self):
        # print(f"inside the JNE")
        # looks at result of CMP
        if self.FL == False:
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            self.pc += 2
        # flag is clear/false/0 jump
        # to reg determined in next line of memory

    def run(self):  # need to establish a  branch_table
        # aka a dict so that the run checks for the op then if exisits
        # runs it
        """Run the CPU."""
        while self.running:
            command = self.ram[self.pc]
            # print(f"self.pc: {self.pc}\n\nself.SP: {self.SP}")
            # print(f"self.ram: {self.ram}\nself.reg: {self.reg}")
            # # prints here pre-command to check stuf out..

            if command == PRN:
                self.branchtable[PRN]()

            elif command == CMP:
                self.branchtable[CMP]()

            elif command == JEQ:
                self.branchtable[JEQ]()

            elif command == JMP:
                self.branchtable[JMP]()

            elif command == JNE:
                self.branchtable[JNE]()

            elif command == CALL:
                self.branchtable[CALL]()

            elif command == RET:
                self.branchtable[RET]()

            elif command == MUL:
                self.branchtable[MUL]()

            elif command == ADD:
                self.branchtable[ADD]()

            elif command == LDI:
                self.branchtable[LDI]()

            # elif command == DEC:
            #     self.pc += 1
            #     reg_num = self.ram[self.pc]
            #     self.reg[reg_num] = self.ram[self.pc]
            #     reg_num -= 1

            elif command == HLT:
                self.branchtable[HLT]()

            elif command == PUSH:
                self.branchtable[PUSH]()

            elif command == POP:
                self.branchtable[POP]()

            else:
                print(
                    f"command: {bin(command)}\n\nwe don't know that shit... need to add more funcitons")
                sys.exit(1)

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, pc):  # reads data from ram/memory at a specific location
        read_at = self.ram[pc]
        print(read_at)
        return read_at

    def ram_write(self, ramN, value):  # writes info to the ram/memory at a specific location
        self.ram[ramN] = value
