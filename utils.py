def remove_comment(line):
    idx = line.find(';')
    if idx != -1:
        line = line[:idx] + "\n"
    return line


def remove_line_no(line):
    idx = line.find("\t")
    curr_line = line[idx+2:]
    return curr_line


def capitalise_hex(temp_hex):
    formatted_hex = ""
    for char in temp_hex:
        if char.isalpha():
            formatted_hex += char.upper()
        else:
            formatted_hex += char
    return formatted_hex


def count_lines(file_path):
    with open(file_path, "r") as file:
        return len(file.readlines())


def int_address_to_hex(address):
    if isinstance(address, str):
        address = int(address)
    hex_address = int_to_hex(address)
    temp_hex = hex_address.zfill(6)
    formatted_hex = capitalise_hex(temp_hex)
    return formatted_hex


def int_to_hex(num):
    if isinstance(num, str):
        num = int(num)
    hex_num = hex(num)[2:]
    hex_num = capitalise_hex(hex_num)
    return hex_num


def hex_to_binary(hex_string):
    binary = ""
    for hex_digit in hex_string:
        bin_digit = bin(int(hex_digit, 16))[2:].zfill(4)
        binary += bin_digit
    return binary


def binary_to_hex(bin_string):
    bin_string = bin_string[::-1]
    curr_digit = ""
    hex_str = ""
    for c in bin_string:
        curr_digit += c
        if len(curr_digit) == 4:
            curr_digit = curr_digit[::-1]
            curr_digit = hex(int(curr_digit, 2))[2:]
            hex_str += curr_digit
            curr_digit = ""

    if len(curr_digit) > 0:
        curr_digit = curr_digit[::-1]
        curr_digit.zfill(4)
        curr_digit = hex(int(curr_digit, 2))[2:]
        hex_str += curr_digit

    hex_str = hex_str[::-1]
    return capitalise_hex(hex_str)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def twos_comp(num):
    if isinstance(num, str):
        num = int(num)
    bin_str = bin(num)[2:]
    rev_bin_str = bin_str[::-1]
    rev_twos_comp = ""
    one_found = False
    for dig in rev_bin_str:
        if dig == '0' and not one_found:
            rev_twos_comp += '0'
        elif dig == '1' and not one_found:
            rev_twos_comp += '1'
            one_found = True
        elif dig == '0' and one_found:
            rev_twos_comp += '1'
        elif dig == '1' and one_found:
            rev_twos_comp += '0'

    twos_comp = rev_twos_comp[::-1]
    return twos_comp


def zfill_neg(bin_string, needed_len):
    while len(bin_string) < needed_len:
        bin_string = '1' + bin_string
    return bin_string


def split_instruction(instruction):
    from constants import FORMAT_ONE

    inst_split = instruction.split()

    label = ""
    operation = "xx"
    operand = 0

    if "EQU" in inst_split:
        label = inst_split[0]
        operation = "EQU"
        operand = inst_split[2]
        return (label,operation,operand)

    if "*" in inst_split:
        label = "*"
        operation = ""
        operand = inst_split[1]
        return (label,operation,operand)
    
    if "LTORG" in inst_split:
        operation = "LTORG"
        return (label,operation,operand)

    # Handle format one instructions separately (no operands)
    for instr in FORMAT_ONE:
        if instr in inst_split:
            operation = instr
            if len(inst_split) == 2:
                label = inst_split[0]

    if operation != "xx":
        return (label, operation, operand)

    # Handle RSUB separately (no operand)
    if "RSUB" in inst_split:
        operation = "RSUB"
        if len(inst_split) == 2:
            label = inst_split[0]
    elif len(inst_split) == 3:  # Instruction with label
        label = inst_split[0]
        operation = inst_split[1]
        operand = inst_split[2]
    elif len(inst_split) == 2:  # Instruction without label
        operation = inst_split[0]
        operand = inst_split[1]

    return (label, operation, operand)

def check_format(source_path):
    with open(source_path, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        seperator_count = line.count('\t\t')
        if(seperator_count != 2):
            raise Exception("File is incorrect format, aborting now")
    
def process_intermediate_file(source_path, dest_path):
    with open(source_path, "r") as f:
        lines = f.readlines()
    
    with open(dest_path, "w") as inter_file:
        for line in lines:
            line = remove_comment(line)
            line = remove_line_no(line)
            inter_file.write(line)


