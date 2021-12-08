FROM python:3.9.2-buster

# Install system dependencies
RUN apt-get update -y
RUN apt-get install -y texlive texlive-lang-european texlive-fonts-extra
RUN apt-get install -y tree

# Setup non-root user
RUN useradd -ms /bin/bash appuser
WORKDIR /home/appuser/app
RUN umask u=rw
RUN mkdir /home/appuser/app/logs
RUN mkdir /home/appuser/app/data

# Install poetry
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV PATH=/home/appuser/.local/bin:$PATH
RUN pip install poetry

# Install Python dependencies
COPY --chown=appuser poetry.lock /home/appuser/app/poetry.lock
COPY --chown=appuser pyproject.toml /home/appuser/app/pyproject.toml
RUN poetry install

# Environment variables
ENV DATABASE_URL postgresql+psycopg2://postgres@127.0.0.1/DataEnWatNu
ENV LATEX_PATH "pdflatex"
ENV SECRET_KEY CHANGEME
ENV LOGGING_LEVEL WARNING
ENV LOGGING_BACKUP_COUNT 10
ENV LOGGING_SIZE 10240
ENV LOGGING_EMAIL ""
ENV MAIL_SERVER ""
ENV MAIL_PORT 587
ENV MAIL_USE_TLS 1
ENV MAIL_USERNAME ""
ENV MAIL_PASSWORD ""
ENV ADMINS ""

# Setup entrypoint
COPY --chown=appuser ./entrypoint.sh /home/appuser/app/entrypoint.sh
RUN chmod +x /home/appuser/app/entrypoint.sh

# Copy app
COPY --chown=appuser . /home/appuser/app
RUN tree /home/appuser/app
RUN chmod +x /home/appuser/app/tools/generate_radar_plot.py

CMD ["/home/appuser/app/entrypoint.sh"]