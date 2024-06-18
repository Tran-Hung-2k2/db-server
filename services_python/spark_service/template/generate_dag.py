from jinja2 import Environment, FileSystemLoader
import os



def generate_jinja(config, template_path, uuid):
    # Load the Jinja template
    env = Environment(
        loader=FileSystemLoader(searchpath=os.path.dirname(template_path))
    )
    template = env.get_template(os.path.basename(template_path))
    # Render the template with the provided configuration
    rendered_script = template.render(config=config)
    rendered_script = "\n".join([line for line in rendered_script.splitlines() if line.strip()])
    output_file=f"services_python/spark_service/spark_dag/{uuid}.py"
    with open(output_file, 'w') as file:
        file.write(rendered_script)

    print(f"Python file generated at {output_file}")
    return True


def generate_dag(source_config):
    template_path="services_python/spark_service/template/basic_dag.j2"
    return generate_jinja(
        config=source_config,
        template_path=template_path,
    )