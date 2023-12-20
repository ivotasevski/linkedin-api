FROM python:3.12

RUN pip3 install pipenv

WORKDIR /usr/src/app

COPY Pipfile ./
COPY Pipfile.lock ./

RUN mkdir .venv

RUN set -ex && PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

COPY . .

ENV PATH="$PATH:/usr/src/app/.venv/bin"

EXPOSE 8000

CMD [ "gunicorn", "-b0.0.0.0:8000", "wsgi:app" ]