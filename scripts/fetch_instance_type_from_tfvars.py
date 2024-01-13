import hcl2

input_file = './bench/terraform/input.tfvars'
output_file = './scripts/infra.txt'

try:
    with open(input_file, 'r') as file:
        config = hcl2.load(file)

    machine_type_line = None
    for item in config['configuration']:
        if item['name'] == 'edge-server':
            machine_type_line = f'machine_type = "{item["machine_type"]}"'
            break

    if machine_type_line:
        with open(output_file, 'w') as file:
            file.write(machine_type_line)

except Exception as e:
    print(f"Err: {e}")
