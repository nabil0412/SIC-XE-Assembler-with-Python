DEFAULT_PATHS = {
    "original_file_path": "./assets/copy.txt",
    "intermediate_file_path": "./assets/intermediate.txt",
    "pass1_file_path": "./assets/pass1/out_pass1.txt",
    "symbol_file_path": "./assets/pass1/symbTable.txt",
    "literal_file_path":"./assets/pass1/literalTable.txt",
    "object_code_file_path": "./assets/pass2/out_pass2.txt",
    "HTME_file_path": "./assets/pass2/HTME.txt"
}


FORMAT_ONE = ["FIX", "FLOAT", "HIO", "NORM", "SIO", "TIO"]
FORMAT_TWO = ["ADDR", "CLEAR", "COMPR", "DIVR", "MULR", "RMO", "SHIFTL", "SHIFTR", "SUBR", "SVC", "TIXR"]
FORMAT_THREE = [
    "ADD", "ADDF", "AND", "COMP", "COMPF", "DIV", "DIVF", "J", "JEQ", "JGT", "JLT", "JSUB",
    "LDA", "LDB", "LDCH", "LDF", "LDL", "LDS", "LDT", "LDX", "LPS", "MUL", "MULF", "OR",
    "RD", "RSUB", "SSK", "STA", "STB", "STCH", "STF", "STI", "STL", "STS", "STSW", "STT",
    "STX", "SUB", "SUBF"
]
FORMAT_FOURL = [
    "LITAD","LITSB","LITLD","LITCMP"
]



VAR_DEF = ["BYTE", "WORD"]
DIRECTIVES = ["BASE", "ORG","START","END","LTORG","EQU"]


SICXE_OPCODES = {
    "ADD": "18", 
    "ADDF": "58", 
    "ADDR": "90", 
    "AND": "40", 
    "CLEAR": "B4",
    "COMP": "28", 
    "COMPF": "88", 
    "COMPR": "A0", 
    "DIV": "24", 
    "DIVF": "64",
    "DIVR": "9C", 
    "FIX": "C4", 
    "FLOAT": "C0", 
    "HIO": "F4", 
    "J": "3C",
    "JEQ": "30", 
    "JGT": "34", 
    "JLT": "38", 
    "JSUB": "48", 
    "LDA": "00",
    "LDB": "68", 
    "LDCH": "50", 
    "LDF": "70", 
    "LDL": "08", 
    "LDS": "6C",
    "LDT": "74", 
    "LDX": "04", 
    "LPS": "D0", 
    "MUL": "20", 
    "MULF": "60",
    "MULR": "98", 
    "NORM": "C8", 
    "OR": "44", 
    "RD": "D8", 
    "RMO": "AC",
    "RSUB": "4C", 
    "SHIFTL": "A4", 
    "SHIFTR": "A8", 
    "SIO": "F0", 
    "SSK": "EC",
    "STA": "0C", 
    "STB": "78", 
    "STCH": "54", 
    "STF": "80", 
    "STI": "D4",
    "STL": "14", 
    "STS": "7C", 
    "STSW": "E8", 
    "STT": "84", 
    "STX": "10",
    "SUB": "1C", 
    "SUBF": "5C", 
    "SUBR": "94", 
    "SVC": "B0", 
    "TD": "E0",
    "TIO": "F8", 
    "TIX": "2C", 
    "TIXR": "B8", 
    "WD": "DC",
    "LITAD":"BC",
    "LITSB":"8C",
    "LITLD":"E4",
    "LITCMP":"FC"
}

REGISTER_NUMBERS = {
    "A": 0, "X": 1, "L": 2, "B": 3, "S": 4,
    "T": 5, "F": 6, "PC": 8, "SW": 9
}


SYMBOLS = {
}

LITERALS = {
    
}

EQUATES = []