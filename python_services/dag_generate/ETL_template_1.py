# dag_template.jinja2
@dag(
    "{{ dag_name }}",
    default_args={
        "depends_on_past": {% if default_args.depends_on_past is defined %}{{ default_args.depends_on_past }}{% else %}False{% endif %},
        "retries": {% if default_args.retries is defined %}{{ default_args.retries }}{% else %}1{% endif %},
        "retry_delay": timedelta(minutes={{ default_args.retry_delay_minutes | default(5) }}),
        "schedule_interval": {{ default_args.schedule_interval | default(null) }},
        "start_date": {{ default_args.start_date | default("days_ago(2)") }},
        "provide_context": {% if default_args.provide_context is defined %}{{ default_args.provide_context }}{% else %}True{% endif %}
    },
    description="{{ description | default('') }}",
    tags={{ tags | default([]) }}
)



# dag_template.jinja2
@dag(
    "{{ parameters.dag_name | default('ETL_TEMPLATE_CLUSTER') }}",
    default_args={
        "depends_on_past": {{ parameters.default_args.depends_on_past | default(false) }},
        "retries": {{ parameters.default_args.retries | default(1) }},
        "retry_delay": timedelta(minutes={{ parameters.default_args.retry_delay_minutes | default(5) }}),
        "schedule_interval": {{ parameters.default_args.schedule_interval | default(null) }},
        "start_date": {{ parameters.default_args.start_date | default("days_ago(2)") }},
        "provide_context": {{ parameters.default_args.provide_context | default(true) }}
    },
    description="{{ parameters.description | default('DAG receives parameters in cluster mode') }}",
    tags={{ parameters.tags | default([]) }}
)
