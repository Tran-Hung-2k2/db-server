import jinja2
import os
import yaml

def generate_jinja(template_file, output_file, input_file):
    # Create the Jinja environment
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(template_file)))

    # Render the template
    template = env.get_template(os.path.basename(template_file))
    rendered_content = template.render()

    # Read the input file
    with open(input_file, 'r') as file:
        input_data = yaml.safe_load(file)

    # Render the template with input data
    rendered_content = template.render(input_data)

    # Write the rendered content to the output file
    with open(output_file, 'w') as file:
        file.write(rendered_content)

    print(f"Python file generated at {output_file}")

def main():
    # template_file = '/home/duonghdt/Desktop/Python/db-server/services_python/spark_service/template/kafka_to_delta_spark_dag_template.j2'
    # output_file = '/home/duonghdt/Desktop/Python/db-server/services_python/spark_service/spark_dag/generated_spark_dag.py'
    # input_file = '/home/duonghdt/Desktop/Python/db-server/services_python/spark_service/input/kafka_to_delta_spark_dag_input.yaml'

    template_file = '/home/duonghdt/Desktop/Python/db-server/services_python/spark_service/template/kafka_to_delta_spark_job_template.j2'
    output_file = '/home/duonghdt/Desktop/Python/db-server/services_python/spark_service/spark_job/generated_spark_job.py'
    input_file = '/home/duonghdt/Desktop/Python/db-server/services_python/spark_service/input/kafka_to_delta_spark_job_input.yaml'
    generate_jinja(template_file, output_file, input_file)

if __name__ == "__main__":
    main()