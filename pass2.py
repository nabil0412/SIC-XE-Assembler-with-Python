import constants
from utils import *
from instruction_decoder import InstructionDecoder


class Pass2:

    
    def __init__(self, symbols, starting_address, ending_address, base_address, end_directive_address):

        self.symbols = constants.SYMBOLS
        self.literals = constants.LITERALS
        self.equates = constants.EQUATES
        self.starting_address = starting_address
        self.ending_address = ending_address
        self.base_address = base_address
        self.end_directive_adress = end_directive_address
        self.decoded_instructions = {}
        self.arrays = {}
        self.reserves_w = {}  
        self.reserves_b = {} 
        self.decoder = InstructionDecoder(symbols, base_address)
        
    def execute(self, file_path, num_lines):
        with open(file_path, "r") as f:
            f.readline() 
            f.readline() 
            
            for i in range(num_lines):
                line = f.readline()
                idx = line.find('\t')
                curr_location = line[:idx]
                array = False
                
                label, operation, operand = split_instruction(line[idx+2:])

                hex_inst = ""
                if operation in constants.FORMAT_ONE:
                    hex_inst = self.decoder.decode_format_one(operation)
                elif operation in constants.FORMAT_TWO:
                    hex_inst = self.decoder.decode_format_two(operation, operand)
                elif operation in constants.FORMAT_THREE:
                    hex_inst = self.decoder.decode_format_three(operation, operand, curr_location)
                elif operation[1:] in constants.FORMAT_THREE and operation[0] == '+':  # Format 4
                    hex_inst = self.decoder.decode_format_four(curr_location, operation, operand)
                elif operation in constants.FORMAT_FOURL:
                    hex_inst = self.decoder.decode_format_fourL(operation,operand)
                elif operation == "BASE":
                    self.decoder.set_base_address(operand)
                    self.base_address = self.symbols[operand]
                elif operation == "BYTE":
                    if operand in self.symbols:
                        operand = int(self.symbols[operand])
                    hex_inst = self.decoder.decode_bytes(operand)
                    array, hex_inst = self._check_array_bytes(hex_inst, curr_location)
                    if(array):
                        self.arrays[curr_location] = hex_inst
                elif operation == "WORD":
                    if operand in self.symbols:
                        operand = int(self.symbols[operand])
                    hex_inst = self.decoder.decode_word(operand)
                    array, hex_inst = self._check_array_words(hex_inst, curr_location)
                    if(array):
                        self.arrays[curr_location] = hex_inst
                elif operation == "RESB":
                    if operand in self.symbols:
                        operand = int(self.symbols[operand],16)
                    self.reserves_b[curr_location] = int(operand)
                elif operation == "RESW":
                    if operand in self.symbols:
                        operand = int(self.symbols[operand],16)
                    self.reserves_w[curr_location] = int(operand)
                elif operand in self.literals:
                    hex_inst = self.decoder.decode_bytes(operand[1:])
                    array, hex_inst = self._check_array_bytes(hex_inst, curr_location)
                elif operation  not in constants.DIRECTIVES:
                    raise Exception(f"For location {curr_location} , no such instruction {operation} found, aborting now")
                
                if not array:
                    self.decoded_instructions[curr_location] = hex_inst

        self._write_object_code_file(file_path)
        self._write_htme_records()
        
        return self.decoded_instructions
    
    def _check_array_words(self, hex_inst, curr_location):
        if len(hex_inst) == 1:
            hex_inst = ''.join(hex_inst)
            return False, hex_inst
        
        int_loc = int(curr_location, 16)
        for word in hex_inst:
            self.decoded_instructions[int_address_to_hex(int_loc)] = word
            int_loc += 3
            
        return True, hex_inst
    
    def _check_array_bytes(self, hex_inst, curr_location):
        if len(hex_inst) == 1:
            hex_inst = ''.join(hex_inst)
            return False, hex_inst
        
        int_loc = int(curr_location, 16)
        for byte in hex_inst:
            self.decoded_instructions[int_address_to_hex(int_loc)] = byte
            sz = int((len(byte)/2))
            int_loc += sz
            
        return True, hex_inst
    
    def _write_object_code_file(self, file_path):

        output_path = "./assets/pass2/out_pass2.txt"
        
        with open(file_path, "r") as f, open(output_path, "w") as pass2_f:
            col_head = f.readline()
            idx = col_head.find("\n")
            col_head = col_head[:idx]
            pass2_f.write(col_head + "\t\tObject Code\n")
            
            num_lines = sum(1 for _ in f)
            f.seek(0)
            f.readline()
            
            for i in range(num_lines):
                curr_line = f.readline()

                
                idx = curr_line.find('\t')
                curr_loc = curr_line[:idx]
                rest_line= curr_line[idx+2:]
                if(rest_line in self.equates):
                    pass2_f.write(curr_line)
                    continue
                
                idx = curr_line.find("\n")
                if idx != -1:
                    curr_line = curr_line[:idx]

                try:
                    object_code = self.decoded_instructions[curr_loc]
                except:
                    object_code = ""
                
                if(curr_loc in self.arrays):
                    object_code = ",".join(self.arrays[curr_loc])

                if("*" in curr_line and "=" in curr_line):
                    pass2_f.write(curr_line + "\t\t\t" + object_code + "\n")
                else:
                    pass2_f.write(curr_line + "\t\t" + object_code + "\n")
    
    def _write_htme_records(self):
        output_path = "./assets/pass2/HTME.txt"
        
        with open(output_path, "w") as htme_file:
            self._write_h_record(htme_file)
            
            self._write_t_records(htme_file)
            
            self._write_m_records(htme_file)
            
            self._write_e_record(htme_file)
    
    def _write_h_record(self, file):
        prog_name = getattr(self, 'prog_name')
        file.write(f"H.{prog_name}.{int_address_to_hex(self.starting_address)}.{self._prog_length()}\n")
    
    def _write_t_records(self, file):
        start = int(self.starting_address, 16) if isinstance(self.starting_address, str) else self.starting_address
        end = int(self.ending_address, 16) if isinstance(self.ending_address, str) else self.ending_address
        curr_address= start
        
        end_literal = False
        while curr_address != end:
            curr_address,end_literal = self._write_t_record(file, curr_address,end_literal)
            hex_addr = int_address_to_hex(curr_address)
            
            if hex_addr in self.reserves_w:
                steps = self.reserves_w[hex_addr]
                curr_address += steps * 3
            elif hex_addr in self.reserves_b:
                steps = self.reserves_b[hex_addr]
                curr_address += steps
    
    def _write_t_record(self, file, curr_address,end_literal):
        sz = 0
        codes = []
        start = int_address_to_hex(curr_address)
        
        
        while True:
            address_hex = int_address_to_hex(curr_address)
            
            if address_hex not in self.decoded_instructions or self.decoded_instructions[address_hex] == "":
                break


            if address_hex == self.end_directive_adress and end_literal == False:
                end_literal = True
                break
            
            code = self.decoded_instructions[address_hex]
            code_bytes = int(len(code) / 2)
            
            if sz + code_bytes > 30:
                break
            else:
                sz += code_bytes
                curr_address += code_bytes
                codes.append(code)
        
        if not codes:
            return curr_address,end_literal
        
        record = f"T.{start}.{int_to_hex(sz).zfill(2)}"
        for code in codes:
            record += f".{code}"
            
        file.write(record + '\n')
        return curr_address,end_literal
    
    def _write_m_records(self, file):

        for address in self.decoder.get_m_records():
            address_int = int(address, 16)
            address_int += 1
            address_hex = int_address_to_hex(address_int)
            file.write(f"M.{address_hex}.05\n")
    
    def _write_e_record(self, file):
        file.write(f"E.{int_address_to_hex(self.starting_address)}")
    
    def _prog_length(self):
        start = int(self.starting_address, 16) if isinstance(self.starting_address, str) else self.starting_address
        end = int(self.ending_address, 16) if isinstance(self.ending_address, str) else self.ending_address
        length = end - start
        return int_address_to_hex(length)
    
    def set_program_name(self, name):
        self.prog_name = name