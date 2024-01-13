import subprocess
import hcl2


def get_git_diff(file_path, commit1="HEAD~1", commit2="HEAD"):

    full_commit1 = subprocess.run(["git", "rev-parse", commit1], stdout=subprocess.PIPE).stdout.decode().strip()
    full_commit2 = subprocess.run(["git", "rev-parse", commit2], stdout=subprocess.PIPE).stdout.decode().strip()
    print(f"Getting diff between commits: {full_commit1} and {full_commit2}")

    command = ["git", "diff", full_commit1, full_commit2, file_path]
    result = subprocess.run(command, stdout=subprocess.PIPE)
    print(result.stdout.decode())
    return result.stdout.decode()


def format_hcl(data):
    formatted = ""

    def format_value(value):
        if isinstance(value, dict):
            return "{\n" + "\n".join(f"  {k} = {format_value(v)}" for k, v in value.items()) + "\n}"
        elif isinstance(value, list):
            return "[\n" + ",\n".join(f"  {format_value(v)}" for v in value) + "\n]"
        elif isinstance(value, str):
            return f'"{value}"' if not value.startswith('"') else value
        else:
            return str(value)

    for key, values in data.items():
        if isinstance(values, list):
            formatted += f"{key} = [\n" + ",\n".join(format_value(v) for v in values) + "\n]\n"
        else:
            formatted += f"{key} = {format_value(values)}\n"
    return formatted


if __name__ == '__main__':
    main_tf_diff = get_git_diff("./infra/main.tf")
    print(main_tf_diff)
    property_names_to_look_for = ["machine_type", "image", "zone", "count"]
    detected_changes = {}
    tag = "edge-server"
    for line in main_tf_diff.splitlines():
        if line.startswith('- ') or line.startswith('+ '):
            for prop in property_names_to_look_for:
                if f"{prop} =" in line:
                    value = line.split('=')[1].strip()
                    if tag not in detected_changes:
                        detected_changes[tag] = {}
                    if prop not in detected_changes[tag]:
                        detected_changes[tag][prop] = {}
                    detected_changes[tag][prop]['old' if line.startswith('- ') else 'new'] = value

    with open('./bench/terraform/input.tfvars', 'r') as file:
        input_tfvars = hcl2.loads(file.read())

    for config in input_tfvars['configuration']:
        if set(config['tags']).intersection(detected_changes.keys()):
            for tag in config['tags']:
                if tag in detected_changes:
                    for prop in detected_changes[tag]:
                        if prop in config:
                            config[prop] = detected_changes[tag][prop]['new']

    formatted_hcl = format_hcl(input_tfvars)
    with open('./bench/terraform/input.tfvars', 'w') as file:
        file.write(formatted_hcl)
