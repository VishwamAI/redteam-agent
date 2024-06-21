import yaml
import json
import os

def convert_yaml_to_json(yaml_file_path, json_file_path):
    with open(yaml_file_path, 'r') as yaml_file:
        yaml_content = yaml.safe_load(yaml_file)

    with open(json_file_path, 'w') as json_file:
        json.dump(yaml_content, json_file, indent=2)

if __name__ == '__main__':
    yaml_file_path = '../swagger-ui/swagger.yaml'
    json_file_path = '../swagger-ui/swagger.json'

    if os.path.exists(yaml_file_path):
        convert_yaml_to_json(yaml_file_path, json_file_path)
        print(f"Converted {yaml_file_path} to {json_file_path}")
    else:
        print(f"YAML file not found: {yaml_file_path}")
