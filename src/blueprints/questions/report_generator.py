import jinja2
import os
from jinja2 import Template
from pdflatex import PDFLaTeX


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