import tempfile
import subprocess
import glob
import shutil
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


def compile_report(temp_dir):
    # Compiles the report
    command = ["pdflatex", "main.tex"]
    shell = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=temp_dir.name)
    output, errors = shell.communicate()
    if errors:
        raise RuntimeError(f"Error while running command '{command}':\n" +
        f"{errors.decode()}")


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

    # Make temporary directory
    temp_dir = tempfile.TemporaryDirectory()

    # Copies figures and fonts to the temp directory
    figures_dir = "figures"
    font_dir = "fonts"
    parent = "src/templates/report"
    fig_dst_dir = temp_dir.name+"/figures"
    font_dst_dir = temp_dir.name+"/fonts"

	# Make necessary subdirectories in temp directory
    if not os.path.exists(fig_dst_dir):
    	os.mkdir(os.path.join(temp_dir.name, figures_dir))
    if not os.path.exists(font_dst_dir):
    	os.mkdir(os.path.join(temp_dir.name, font_dir))

    # Copy files from report template to temp directory
    for image in glob.iglob(os.path.join(os.path.join(parent, figures_dir), "*.*")):
    	shutil.copy(image, fig_dst_dir)
    for font in glob.iglob(os.path.join(os.path.join(parent, font_dir), "*.*")):
    	shutil.copy(font, font_dst_dir)
    shutil.copyfile(os.path.join(parent, "roboto.sty"), os.path.join(temp_dir.name, "roboto.sty"))
    shutil.copyfile(os.path.join(parent, "tudelft-report.bst"), os.path.join(temp_dir.name, "tudelft-report.bst"))
    shutil.copyfile(os.path.join(parent, "tudelft-report.cls"), os.path.join(temp_dir.name, "tudelft-report.cls"))

	# Copies files to generate report (these files will contain variable info eventually, so will not be copied literally in the future)
    shutil.copyfile(os.path.join(parent, "1-inleiding.tex"), os.path.join(temp_dir.name, "1-inleiding.tex"))
    shutil.copyfile(os.path.join(parent, "2-resultaten.tex"), os.path.join(temp_dir.name, "2-resultaten.tex"))
    shutil.copyfile(os.path.join(parent, "3-aanbevelingen.tex"), os.path.join(temp_dir.name, "3-aanbevelingen.tex"))
    shutil.copyfile(os.path.join(parent, "main.tex"), os.path.join(temp_dir.name, "main.tex"))
    shutil.copyfile(os.path.join(parent, "title-page.tex"), os.path.join(temp_dir.name, "title-page.tex"))

    # TEMPORARY QUESTIONS FOR TESTING
    test_q = ["Is this a question?", "Is this also a question?", "How many questions are there?"]
    test_a = ["This is an answer", "Yes", 3]

    # Fill in information in template
    qa_template = latex_jinja_env.get_template(os.path.join(parent, "vraag-en-antwoord.tex"))
    qa = qa_template.render(test_q=test_q, test_a=test_a)
    with open(temp_dir.name+"/vraag-en-antwoord.tex",'w') as output:
    	output.write(qa)
    
    # Generate PDF
    compile_report(temp_dir)

    # Copy report pdf from temp directory to reports folder
    shutil.copyfile(os.path.join(temp_dir.name, "main.pdf"), os.path.join("src/output/pdf", session_id+".pdf"))

    # Delete temp folder
    temp_dir.cleanup()

