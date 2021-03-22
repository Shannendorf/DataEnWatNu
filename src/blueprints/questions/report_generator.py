import jinja2
import os
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from jinja2 import Template
from pdflatex import PDFLaTeX


def generate_radarchart(groups_dict, scores, session_id):
    import subprocess

    data = {"labels": [], "data": {}}
    for group in groups_dict["groups"]:
        current_group = groups_dict[group]
        title = current_group["group"].title
        data["labels"].append(title)
        data["data"][title] = current_group["score"]

    if not os.path.exists("src/static/images"):
        os.mkdir("src/static/images")
    output_path = f"src/static/images/{session_id}.png"

    data_str = str(data).replace("'", '"')
    subprocess.call([
        "tools/generate_radar_plot.py",
        "--data", data_str,
        "--output", output_path
    ])


def generate_report(answers_list, session_id):
    latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%%',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    )
    template = latex_jinja_env.get_template('src/templates/report/report.tex')
    document = template.render(section1='Rapport', answers_list=answers_list)
    with open("src/output/tex/"+session_id+".tex",'w') as output:
        output.write(document)
    pdfl = PDFLaTeX.from_texfile('src/output/tex/'+session_id+'.tex')
    pdfl.set_output_directory('src/output/pdf')
    pdf, log, completed_process = pdfl.create_pdf(keep_pdf_file=True)