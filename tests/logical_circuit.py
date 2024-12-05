def operation(base, input_bit):
    truth_table = {
        # "state": {"input_bit (0)": ("output_bit", "new_state"), "input_bit (1)": ("output_bit", "new_state")}
        "00": {"0": ("00", "00"), "1": ("11", "10")},
        "10": {"0": ("10", "01"), "1": ("01", "11")},
        "01": {"0": ("11", "00"), "1": ("00", "10")},
        "11": {"0": ("01", "01"), "1": ("10", "11")}
    }

    return truth_table[base][str(input_bit)]


def logicalOperation(base, input_bit):
    base_int = int(base, 2)
    input_int = int(input_bit, 2)

    xor_res = base_int ^ input_int
    and_res = base_int & input_int

    xor_out = format(xor_res, "02b")
    and_out = format(and_res, "02b")

    return xor_out, and_out

# Test cases
test_cases = [("00", "0"), ("00", "1"), ("10", "0"), ("10", "1"),
              ("01", "0"), ("01", "1"), ("11", "0"), ("11", "1")]


print("---------- Hardcode ----------------")
for base, input_bit in test_cases:
    output, new_state = operation(base, input_bit)
    print("base =", base, "input =", input_bit, "output =", output, "new_state =", new_state)

print("------------------------------------\n")

print("---------- Logical operations --------")
for base, input_bit in test_cases:
    output, new_state = logicalOperation(base, input_bit)
    print("base =", base, "input =", input_bit, "output =", output, "new_state =", new_state)