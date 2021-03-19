import jinja2
import os
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from jinja2 import Template
from pdflatex import PDFLaTeX


def generate_radarchart(scores, session_id):
    # first param is a list containing the scores 
    # second param is the session_id (to name the image)
    df = pd.DataFrame({
    'group': ["Gevoel van urgentie", "Data op strategisch niveau", "Skillset medewerkers", "Staat van digitalisering", "Bereidheid tot verandering"],
    "Gevoel\n van\n urgentie": [scores[0], scores[0], scores[0], scores[0], scores[0]],
    "Data op\n strategisch niveau": [scores[1], scores[1], scores[1], scores[1], scores[1]],
    "Skillset\n mede-\n werkers\n\n": [scores[2], scores[2], scores[2], scores[2], scores[2]],
    "Staat\n van\n digitalisering": [scores[3], scores[3], scores[3], scores[3], scores[3]],
    "Bereidheid\n tot verandering": [scores[4], scores[4], scores[4], scores[4], scores[4]]
    })
    
    categories=list(df)[1:]
    N = len(categories)
    
    values=df.loc[0].drop('group').values.flatten().tolist()
    values += values[:1]
    
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    
    ax = plt.subplot(111, polar=True)   
    plt.xticks(angles[:-1], categories, color='#6f7274', size=6)
    ax.set_rlabel_position(0)
    plt.yticks([5,10,15,20], ["5","10","15","20"], color="grey", size=7)
    plt.ylim(0,25)

    ax.plot(angles, values, linewidth=1, linestyle='solid')
    ax.fill(angles, values, 'b', alpha=0.1)

    # Saving the chart as a PNG
    if not os.path.exists("src/static/images"):
        os.mkdir("src/static/images")
    plt.savefig("src/static/images/"+session_id+".png") 

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