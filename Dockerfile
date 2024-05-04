FROM python:3.11
WORKDIR /code
RUN pip install poetry 
COPY . .
RUN poetry install
CMD ["poetry", "run", "bot"]