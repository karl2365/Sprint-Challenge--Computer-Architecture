"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, file):
        """Construct a new CPU."""
     
        self.LDI = 0b10000010
        self.HLT = 0b00000001
        self.PRN = 0b01000111
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.reg[7] = 0b11110100 
        self.program_filename = file
        self.fl = 0b00000001



    def load(self):
        """Load a program into memory."""
        address = 0

        with open(self.program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

                line = int(line, 2)
                self.ram[address] = line

                address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010

        else:
            raise Exception("Unsupported ALU operation")

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
        pc = 0 
        sc = 7
        
        running = True
        # print(self.ram)
        while running:
            inst = self.ram[pc]

            if inst == self.LDI:
                self.reg[self.ram[pc+1]] = self.ram[pc+2]
                # print(self.reg[pc+1])
                pc += 3

            elif inst == self.PRN:
                reg_num = self.ram[pc + 1]
                # print(reg_num)
                print(self.reg[reg_num])
                pc += 2

            elif inst == self.MUL:
                reg_a = self.ram[pc+1]
                reg_b = self.ram[pc+2]
                self.alu('MUL', reg_a, reg_b)
                pc += 3

            elif inst == self.PUSH:
                self.reg[sc] -= 1
                reg_num = self.ram[pc + 1]
                value = self.reg[reg_num]
                address = self.reg[sc]
                self.ram[address] = value
                pc += 2

            elif inst == self.POP:
                reg_num = self.ram[pc + 1]
                value = self.ram[self.reg[sc]]
                self.reg[reg_num] = value
                self.reg[sc] += 1
                pc += 2

            elif inst == self.CMP:
                reg_a = self.ram[pc+1]
                reg_b = self.ram[pc+2]
                self.alu('CMP', reg_a, reg_b)
                pc += 3

            elif inst == self.JMP:
                register = self.ram[pc + 1]
                pc = self.reg[register]
            
            elif inst == self.JEQ:
                print(pc)
                if self.fl == 0b00000001:
                    register = self.ram[pc + 1]
                    pc = self.reg[register]

            elif inst == self.JNE:
                if self.fl  != 0b00000001:
                    register = self.ram[pc + 1]
                    pc = self.reg[register]

            elif inst == self.HLT:
                running = False

            else:
                print(inst)
                print('instruction not found')
                running = False


