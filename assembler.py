import constants
import utils
from pass1 import Pass1
from pass2 import Pass2


class Assembler:

    def __init__(self):

        self.symbols = constants.SYMBOLS
        self.paths = constants.DEFAULT_PATHS
        
        self.locctr = {}
        self.starting_address = 0
        self.ending_address = 0
        self.prog_name = ""
        self.base_address = "000000"
        self.num_lines = 0
        self.decoded_instructions = {}
        self.source_file = self.paths["original_file_path"]
        self.end_directive_address = ""
    
    def assemble(self):

        utils.check_format(self.source_file)
        self._create_intermediate_file()
        pass1_data = self._execute_pass1()
        #print("pass1 done")
        pass2_data = self._execute_pass2()
        #print("Pass 2 Successful")
        
    
    def _create_intermediate_file(self):
        utils.process_intermediate_file(self.source_file, self.paths["intermediate_file_path"])
    
    def _execute_pass1(self):
        pass1 = Pass1()
        self.locctr, self.symbols, self.starting_address, self.ending_address,self.end_directive_address = pass1.execute(
            self.paths["intermediate_file_path"]
        )
        self.prog_name = pass1.get_program_name()
        self.num_lines = pass1.get_num_lines()
        
        return self.locctr
    
    def _execute_pass2(self):
        pass2 = Pass2(self.symbols, self.starting_address, self.ending_address, self.base_address,self.end_directive_address)
        pass2.set_program_name(self.prog_name)
        self.decoded_instructions = pass2.execute(self.paths["pass1_file_path"], self.num_lines)
        return self.decoded_instructions
    
    def get_symbols(self):
        return self.symbols
    
    def get_location_counter(self):
        return self.locctr
    
