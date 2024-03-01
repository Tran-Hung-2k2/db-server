from jinja2 import Template
import yaml
from pathlib import Path
# Current dir path
cw_dir_path=str(Path(__file__).parent.absolute())
# Load the YAML configuration
with open("example_yaml.yaml", "r") as yaml_file:
    config = yaml.safe_load(yaml_file)
# Load the Jinja template
with open("example_yaml_jinja_template.jinja2", "r") as template_file:
    template = Template(template_file.read())
# Render the template with the YAML configuration
rendered_dag = template.render(config=config)
# Print or save the rendered DAG definition
with open(f"{cw_dir_path}/dag_{config['dag_id']}.py", "w") as create_dag:
    create_dag.write(template.render(config=config))
print(rendered_dag)