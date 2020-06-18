"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #8 bit program 
        self.reg = [0] * 8
        #RAM: 256 
        self.ram = [0] * 256
        #program counter: index of current instruction 
        self.pc = 0
        #Program in running initially 
        self.running = True 
        self.operand_a = 0
        self.operand_b = 0
        self.stack_pointer = 0
        self.flag: 0
        self.call_func = {
             0b00000001: self.hlt,
             0b01000111: self.prn,
             0b10000010: self.ldi,
             0b10100000: self.add,
             0b10100010: self.mul,
             0b01000101: self.push,
             0b01000110: self.pop,
             0b00010001: self.ret,
             0b01010000: self.call
        } 



    def load(self):
        """Load a program into memory."""
        filename = sys.argv[1]
        # print(filename)
        address = 0
        try:
            with open(filename) as f:
                for line in f:
                    line = line.split('#')
                    # num = line[0].strip()
                    # if num == '':
                    #     continue 
                    try:
                        v = int(line[0], 2)
                    except ValueError:
                        continue
                    self.ram[address] = v
                    address += 1
                    
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)
                    
                

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, address):
        return self.ram[address] 

    def ram_write(self, address, value):
        self.ram[address] = value 

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] += self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def mul(self):
        self.alu('MUL', self.operand_a, self.operand_b)

    def add(self):
        self.alu('ADD', self.operand_a, self.operand_b)

    def hlt(self):
        self.running = False 

    def ldi(self):
        self.reg[self.operand_a] = self.operand_b
    
    def prn(self):
        print(self.reg[self.operand_a])

    def push(self):
        self.reg[7] -= 1
        self.stack_pointer = self.reg[7]
        self.ram[self.stack_pointer] = self.reg[self.operand_a]

    def pop(self):
        self.stack_pointer = self.reg[7]
        val = self.ram[self.stack_pointer]
        self.reg[self.operand_a] = val
        self.reg[7] += 1

    def call(self):
        self.reg[7] -= 1
        self.stack_pointer = self.reg[7]
        self.ram[self.stack_pointer] = (self.pc+ 2)
        # self.ram_write(self.program_counter + 2, self.stack_pointer)
        self.pc = (self.reg[self.operand_a])

    def ret(self):
        self.stack_pointer = self.reg[7]
        val = self.ram_read(self.stack_pointer)
        # val = self.ram[self.stack_pointer]
        self.pc = val
        self.reg[7] += 1 
    
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            ir = self.ram_read(self.pc)
            self.operand_a = self.ram_read(self.pc + 1)
            self.operand_b = self.ram_read(self.pc + 2)

            self.call_func[ir]()
            if f'{ir:08b}'[3] == '0':
                self.pc += (ir >> 6) + 1

            # # Halt
            # # 0b before binary is used so python can read binary  
            # if ir == 0b00000001:
            #     self.running == False
            #     self.pc += 1
            # #LDI: set the value of a register to an integer
            # elif ir == 0b10000010:
            #     # operand_a = self.ram_read(self.pc + 1)
            #     # operand_b = self.ram_read(self.pc + 2)
            #     self.reg[operand_a] = operand_b
            #     self.pc += 3
            # # PRN  
            # elif ir == 0b01000111:
            #     # operand_a = self.ram_read(self.pc + 1)
            #     data = self.reg[operand_a]
            #     print(data)
            #     self.pc += 2
            # else:
            #     print(f'Unknown instruction {ir} at address {self.pc}')
            #     sys.exit(1)




            
