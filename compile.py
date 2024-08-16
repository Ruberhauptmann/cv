#!/usr/bin/env python
import datetime
import os
import subprocess

import click
import jinja2
import yaml


def format_date(value: datetime.date):
    return value.strftime("%Y-%m")


def setup_jinja_environment(templates):
    jinja_env = jinja2.Environment(
        block_start_string="\\BLOCK{",
        block_end_string="}",
        variable_start_string="\\VAR{",
        variable_end_string="}",
        comment_start_string="\\#{",
        comment_end_string="}",
        line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath(templates)),
    )
    jinja_env.filters["format_date"] = format_date

    return jinja_env


def render_file(
    jinja_env,
    template_name,
    language,
    data,
    force: bool,
):
    template = jinja_env.get_template(f"{template_name}_{language}.tex")

    document = template.render(data)

    with open(f"TjarkSievers{template_name}_{language}.tex", "w") as tempfile:
        tempfile.write(document)

    command = ["latexmk"]
    if force:
        command.append("-f")
    command.append(f"TjarkSievers{template_name}_{language}.tex")
    subprocess.run(command)

    os.remove(f"TjarkSievers{template_name}_{language}.tex")


def load_data(
    cv_data,
):
    data = dict.fromkeys(
        [
            os.path.splitext(filename)[0]
            for filename in os.listdir(cv_data)
            if (not filename.startswith(".")) and filename.endswith(".yaml")
        ]
    )

    for filename in data.keys():
        with open(os.path.join(cv_data, f"{filename}.yaml"), "r") as f:
            data[filename] = yaml.safe_load(f)

    return data


@click.command()
@click.option("--force/--no-force", default=False)
@click.option("--cv-data", default="cv-data/", type=click.Path(exists=True))
@click.option("--templates", default="templates/", type=click.Path(exists=True))
@click.option("--academic-cv/--no-academic-cv", default=True)
@click.option("--short-cv/--no-short-cv", default=True)
def compile_cv(
    force,
    cv_data,
    templates,
    academic_cv: bool,
    short_cv: bool
):
    jinja_env = setup_jinja_environment(templates)

    data = load_data(cv_data)

    for language in data["general"].keys():
        if academic_cv is True:
            render_file(jinja_env, "AcademicCV", language, data, force)
        if short_cv is True:
            render_file(jinja_env, "ShortCV", language, data, force)


if __name__ == "__main__":
    compile_cv()
