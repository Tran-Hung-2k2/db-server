from jinja2 import Environment, FileSystemLoader
import os

def generate_jinja(config, template_path):
    # Load the Jinja template
    env = Environment(
        loader=FileSystemLoader(searchpath=os.path.dirname(template_path))
    )
    template = env.get_template(os.path.basename(template_path))
    # Render the template with the provided configuration
    rendered_script = template.render(config=config)
    rendered_script = "\n".join([line for line in rendered_script.splitlines() if line.strip()])
    
    return rendered_script


def get_block_content(block_type, source_type, source_config):
    if block_type == "data_loader":
        if source_type == "postgres":
            from services_python.mage_service.template.datasource.postgres.validator import (
                validate_config,
            )
            source_config = validate_config(config=source_config)
            template_path = "services_python/mage_service/template/datasource/postgres/template.j2"
        elif source_type == "mongodb":
            from services_python.mage_service.template.datasource.mongodb.validator import (
                validate_config,
            )
            source_config = validate_config(config=source_config)
            template_path = "services_python/mage_service/template/datasource/mongodb/template.j2"
        elif source_type == "api":
            from services_python.mage_service.template.datasource.api.validator import (
                validate_config,
            )
            source_config = validate_config(config=source_config)
            template_path = "services_python/mage_service/template/datasource/api/template.j2"
        elif source_type == "upload_file":
            from services_python.mage_service.template.datasource.upload_file.validator import (
                validate_config,
            )
            source_config = validate_config(config=source_config)
            template_path = "services_python/mage_service/template/datasource/upload_file/template.j2"
        else:
            return "Hello world"
    elif block_type == "transformer":
        if source_type == "difference":
            from services_python.mage_service.template.transform.difference.validator import (
                validate_config,
            )
            source_config = validate_config(config=source_config)
            template_path = "services_python/mage_service/template/transform/difference/template.j2"
        elif source_type == "drop_duplicate":
            from services_python.mage_service.template.transform.drop_duplicate.validator import (
                validate_config,
            )
            source_config = validate_config(config=source_config)
            template_path = "services_python/mage_service/template/transform/drop_duplicate/template.j2"
        elif source_type == "fill_missing_value":
            from services_python.mage_service.template.transform.fill_missing_value.validator import (
                validate_config,
            )
            source_config = validate_config(config=source_config)
            template_path = "services_python/mage_service/template/transform/fill_missing_value/template.j2"
        elif source_type == "normalize":
            from services_python.mage_service.template.transform.normalize.validator import (
                validate_config,
            )
            source_config = validate_config(config=source_config)
            template_path = "services_python/mage_service/template/transform/normalize/template.j2"
        elif source_type == "remove_outlier":
            from services_python.mage_service.template.transform.remove_outlier.validator import (
                validate_config,
            )
            source_config = validate_config(config=source_config)
            template_path = "services_python/mage_service/template/transform/remove_outlier/template.j2"
        elif source_type == "standardize":
            from services_python.mage_service.template.transform.standardize.validator import (
                validate_config,
            )
            source_config = validate_config(config=source_config)
            template_path = "services_python/mage_service/template/transform/standardize/template.j2"
        else:
            return "Hello world"
    return generate_jinja(
        config=source_config,
        template_path=template_path,
    )