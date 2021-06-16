from jinja2 import Template
from os import listdir
from os.path import isfile, join
import yaml

with open('templates/dataset.json', 'r') as f:
    template = Template(f.read())

datasets_templates_path = 'templates/datasets'
for f in listdir(datasets_templates_path):
    if isfile(join(datasets_templates_path, f)):
        with open(f"{datasets_templates_path}/{f}", 'r') as f:
            dataset_data = yaml.safe_load(f.read())
            with open(f"datasets/{dataset_data['id']}.json", 'w+') as json_file:
                json_file.write(template.render(dataset=dataset_data))
