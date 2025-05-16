from constants import *
from utils import *


class InstructionDecoder:
    
    def __init__(self, symbols, base_address="000000"):
        self.symbols = SYMBOLS
        self.literals = LITERALS
        self.base_address = base_address
        self.m_record_lines = []  # Track addresses that need modification records
    
    def decode_format_one(self, operation):
        return SICXE_OPCODES[operation]
    
    def decode_format_two(self, operation, operand):
        registers = operand.split(',')
        
        reg1 = REGISTER_NUMBERS[registers[0]]
        try:
            reg2 = REGISTER_NUMBERS[registers[1]]
        except:
            reg2 = 0
            
        reg1_hex = int_to_hex(reg1)
        reg2_hex = int_to_hex(reg2)
        opcode = SICXE_OPCODES[operation]
        
        return opcode + reg1_hex + reg2_hex
    
    def decode_format_three(self, operation, operand, curr_location):
        if operation == "RSUB":
            return "4F0000"
            
        opcode = SICXE_OPCODES[operation]
        opcode_binary = hex_to_binary(opcode)
        opcode_binary = opcode_binary[:-2]

        n = '0'
        i = '0'
        x = '0'
        b = '0'
        p = '0'
        e = '0'
        

        if operand[-2:] == ',X':
            x = '1'
            operand = operand[:-2]
            

        if operand[0] == '#':  
            n = '0'
            i = '1'
            operand = operand[1:]
        elif operand[0] == '@': 
            n = '1'
            i = '0'
            operand = operand[1:]
        else: 
            n = '1'
            i = '1'

        b, p, disp = self._check_operand(operand, curr_location)
        inst_binary = opcode_binary + n + i + x + b + p + e + disp
        hex_inst = binary_to_hex(inst_binary)
        
        return hex_inst
    
    def decode_format_four(self, location, operation, operand):
        opcode = SICXE_OPCODES[operation[1:]]
        opcode_binary = hex_to_binary(opcode)
        opcode_binary = opcode_binary[:-2]
        

        n = '0'
        i = '0'
        x = '0'
        b = '0'
        p = '0'
        e = '1'
        requires_M_record = True
        


        if operand[-2:] == ',X':
            x = '1'
            operand = operand[:-2]
        
        if operand[0] == "=":
            operand = self.literals[operand][1:]
        elif operand[0] == '#':
            n = '0'
            i = '1'
            operand = operand[1:]
            operand = int_to_hex(operand).zfill(5)
            requires_M_record = False
        elif operand[0] == '@':
            n = '1'
            i = '0'
            operand = operand[1:]
            operand = self.symbols[operand][1:]
        else:  
            n = '1'
            i = '1'
            operand = self.symbols[operand][1:]
            
        if requires_M_record:
            self.m_record_lines.append(location)
            
        operand_binary = hex_to_binary(operand)
        inst_binary = opcode_binary + n + i + x + b + p + e + operand_binary
        hex_inst = binary_to_hex(inst_binary)
        
        return hex_inst
    
    def decode_format_fourL(self,operation,operand):
        opcode = SICXE_OPCODES[operation]

        operands = operand.split(",")
        register = REGISTER_NUMBERS[operands[0]]
        literal = operands[1][1:]
        print(literal)

        register_hex = int_to_hex(register)
        literal_hex = "".join(self.decode_bytes(literal))

        if(len(literal_hex) > 5):
            raise Exception(f"Literal value is too large for the address field in instruction {operation} {operand}")
        literal_hex = literal_hex.zfill(5)

        return opcode + register_hex + literal_hex

    
    def decode_bytes(self, operand):
        value_list = operand.split(",")
        hex_values = []
        
        for value in value_list:
            if value[0] == 'X':  # Hexadecimal
                hex_num = value[2:-1]
                hex_values.append(hex_num)
            
            if value[0] == 'C':  # Character
                string = value[2:-1]
                hex_str = ""
                for char in string:
                    ascii_val = ord(char)
                    hex_ascii = int_to_hex(ascii_val)
                    hex_str += hex_ascii
                hex_values.append(hex_str)
                
        return hex_values
    

    def decode_word(self, operand):
        value_list = operand.split(",")
        hex_values = []
        
        for value in value_list:
            int_val = int(value)
            hex_val = int_to_hex(int_val)
            if int_val < 0:
                twos = twos_comp(int_val)
                twos = zfill_neg(twos,24)
                hex_val = binary_to_hex(twos)
            else:
                hex_val = hex_val.zfill(6)
                
            hex_values.append(hex_val)
            
        return hex_values
    
    def _check_operand(self, operand, curr_location):
        if is_number(operand):
            b = '0'
            p = '0'
            disp_int = int(operand)
            if disp_int < 0:
                disp = zfill_neg(twos_comp(disp_int), 12)
            else:
                disp = bin(disp_int)[2:].zfill(12)
            return b, p, disp
        
        curr_location = int(curr_location, 16)
        if operand in self.symbols:
           
            new_location = int(self.symbols[operand], 16)
        if operand in self.literals:
            new_location = int(self.literals[operand], 16)

        base_location = int(self.base_address, 16)
        
        pc_disp = new_location - (curr_location + 3)
        base_disp = new_location - base_location
        
        if -2048 <= pc_disp <= 2047:
            b = '0'
            p = '1'
            if pc_disp < 0:
                disp = twos_comp(pc_disp)
                disp = zfill_neg(disp, 12)
            else:
                disp = bin(pc_disp)[2:].zfill(12)
            return b, p, disp
        
        else:
            b = '1'
            p = '0'
            disp = bin(base_disp)[2:].zfill(12)
            return b, p, disp
    
    def set_base_address(self, operand):
        self.base_address = self.symbols[operand]
    
    def get_m_records(self):
        return self.m_record_lines
    

