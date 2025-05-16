import constants
from utils import *


class Pass1:

    def __init__(self):
        self.symbols = constants.SYMBOLS
        self.literals = constants.LITERALS
        self.equates = constants.EQUATES
        self.locctr = {}
        self.starting_address = 0
        self.ending_address = 0
        self.prog_name = ""
        self.num_lines = 0
        self.end_directive_address = ""
        
        
    def execute(self, file_path):
        self.num_lines = self._count_lines(file_path) - 2  
        
        with open(file_path, "r") as f:
            self._process_first_line(f)
            curr_loc = self.starting_address
            for i in range(self.num_lines):
                line = f.readline()
                current_inst = line
                current_inst = remove_comment(current_inst)
                label, operation, operand = split_instruction(current_inst)
                
                formatted_loc = int_address_to_hex(curr_loc)
                if operation not in constants.DIRECTIVES and 'LTORG' not in line:
                    self.locctr[i] = formatted_loc
                
                if(operation == "END"):
                    self.end_directive_address = formatted_loc
                
                if operation == "EQU":
                    self.symbols[label] = self.equate_operand(operand,formatted_loc)
                    self.locctr[i] = self.symbols[label]
                    self.equates.append(current_inst)


                if label and label != '*' and operation != "EQU":
                    self.symbols[label] = formatted_loc
                
                if label == "*":
                    self.literals[operand] = formatted_loc

                

                
                if(i == self.num_lines-1):
                    if(operation == "END"):
                        self.ending_address = formatted_loc
                    else:
                        self.ending_address = int_address_to_hex(self._update_location(curr_loc, operation, operand,label))
                        break
                
                curr_loc = self._update_location(curr_loc, operation, operand,label)
        
        self._write_output_locations(file_path)
        self._write_symbol_table()
        self.write_literal_table()
        
        return self.locctr, self.symbols, self.starting_address, self.ending_address,self.end_directive_address
    
    def _count_lines(self, file_path):
        with open(file_path, "r") as f:
            return len(f.readlines())
    
    def _process_first_line(self, f):
        f.readline()  # Skip column headings
        line = f.readline()
        
        split_line = line.split()
        
        self.prog_name = split_line[0]
        self.starting_address = int(split_line[2])
    
    def equate_operand(self,operand,formatted_loc):
        if(operand == '*'):
            return formatted_loc
        elif(is_number(operand)):
            return int_address_to_hex(operand)
        elif operand in self.symbols:
            return self.symbols[operand]
        else:
            if("+" in operand):
                addresses = operand.split("+")
                address1 = ""
                address2 = ""

                if(addresses[0] == "*"):
                    address1 = formatted_loc
                if(addresses[1] == "*"):
                    address2 = formatted_loc

                if(addresses[0] in self.symbols):
                    address1 = self.symbols[addresses[0]]
                if(addresses[1] in self.symbols):
                    address2 = self.symbols[addresses[1]]

                address1 = int(address1,16)
                address2 = int(address2,16)
                new_address = address1 + address2
                new_address = int_address_to_hex(new_address)
                return new_address

            if("-" in operand):
                addresses = operand.split("-")
                address1 = ""
                address2 = ""

                if(addresses[0] == "*"):
                    address1 = formatted_loc
                if(addresses[1] == "*"):
                    address2 = formatted_loc

                if(addresses[0] in self.symbols):
                    address1 = self.symbols[addresses[0]]
                if(addresses[1] in self.symbols):
                    address2 = self.symbols[addresses[1]]
                

                address1 = int(address1,16)
                address2 = int(address2,16)
                new_address = address1 - address2
                if(new_address < 0):
                    new_address = twos_comp(new_address)
                    new_address = zfill_neg(new_address,24)
                    new_address = binary_to_hex(new_address)
                    return new_address
                new_address = int_address_to_hex(new_address)
                return new_address


    def _update_location(self, curr_loc, operation, operand,label):

        if operation in constants.FORMAT_ONE:
            curr_loc += 1
        elif operation in constants.FORMAT_TWO:
            curr_loc += 2
        elif operation in constants.FORMAT_THREE:
            curr_loc += 3
        elif operation and operation[0] == '+':  # Format 4 (extended)
            curr_loc += 4
        elif operation in constants.FORMAT_FOURL:
            curr_loc+=4
        elif operation == "RESW":
            if operand in self.symbols:
                operand = self.symbols[operand]
                integer_operand = int(operand,16)
            integer_operand = int(operand)
            curr_loc += (3 * integer_operand)
        elif operation == "RESB":
            if operand in self.symbols:
                operand = self.symbols[operand]
                integer_operand = int(operand,16)
            integer_operand = int(operand)
            curr_loc += integer_operand
        elif operation == "BYTE":
            if operand in self.symbols:
                operand = self.symbols[operand]
            operands = operand.split(",")
            for op in operands:
                if op[0] == 'C': 
                    op = op[2:-1] 
                    curr_loc += len(op)
                if op[0] == 'X':
                    op = op[2:-1] 
                    curr_loc += len(op) // 2
        elif operation == "WORD":
            if operand in self.symbols:
                operand = self.symbols[operand]
            operands = operand.split(",")
            for _ in operands:
                curr_loc += 3
        elif operation == "END":
            self.ending_address = curr_loc
        elif label == "*":
            operand = operand[1:]
            if operand[0] == 'C': 
                    operand = operand[2:-1] 
                    curr_loc += len(operand)
            if operand[0] == 'X':
                    operand = operand[2:-1] 
                    curr_loc += len(operand) // 2
        
        return curr_loc
    
    def _write_output_locations(self, file_path):
        output_path = constants.DEFAULT_PATHS["pass1_file_path"]
        
        with open(file_path, "r") as f, open(output_path, "w") as new_file:
            f.readline()
            new_file.write("Location\tLabel\t\tInstruction\n")
            
            for i in range(self.num_lines + 1):
                line = f.readline()
                try:
                    location = self.locctr[i-1]
                except:
                    location = ""
                
                new_file.write(f"{location}\t\t{line}")
    
    def _write_symbol_table(self):
        constants.SYMBOLS = self.symbols
        constants.EQUATES = self.equates
        symbol_file_path = constants.DEFAULT_PATHS["symbol_file_path"]
        
        with open(symbol_file_path, "w") as symbols_file:
            symbols_file.write("Symbol\t\tLocation\n")
            for key, value in self.symbols.items():
                symbols_file.write(f"{key}\t\t{value}\n")

    def write_literal_table(self):
        constants.SYMBOLS = self.symbols
        literal_file_path = constants.DEFAULT_PATHS["literal_file_path"]
        with open(literal_file_path, "w") as literals_file:
            literals_file.write("Symbol\t\tLocation\n")
            for key, value in self.literals.items():
                literals_file.write(f"{key}\t\t{value}\n")

    def get_program_name(self):
        return self.prog_name
    
    def get_starting_address(self):
        return self.starting_address
    
    def get_ending_address(self):
        return self.ending_address
    
    def get_num_lines(self):
        return self.num_lines
    
    def get_end_directive_address(self):
        return self.end_directive_address