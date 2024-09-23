FROM python:3.11.10-slim


WORKDIR /app

# Set environment variables
ENV OPENAI_API_KEY=


COPY pyproject.toml ./

# RUN pip install poetry
RUN pip install --no-cache-dir poetry

RUN poetry install --no-root


COPY . .

COPY .pg_service.conf ~/
COPY .pgpass ~/

# RUN poetry run python manage.py migrate
# RUN poetry run python manage.py collectstatic --noinput

EXPOSE 8000


CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]