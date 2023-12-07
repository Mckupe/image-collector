FROM python:3.11

# ARG YOUR_ENV

# RUN apt update
# RUN apt upgrade -y
# RUN curl -sSL https://install.python-poetry.org | python3 -

# WORKDIR /code
# COPY poetry.lock pyproject.toml /code/

# COPY . /code

# ENTRYPOINT ["poetry", "run", "python", "-m", "annapurna.main"]

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

WORKDIR /code

COPY poetry.lock pyproject.toml ./

RUN apt update
RUN apt upgrade -y
RUN python -m pip install --no-cache-dir poetry==1.4.2 \
    && poetry config virtualenvs.create false \
    && poetry install --without dev,test --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY config.py ./
COPY __init__.py ./

CMD ["uvicorn", "__init__:app", "--host", "0.0.0.0", "--port", "8000"]

# USER get-images