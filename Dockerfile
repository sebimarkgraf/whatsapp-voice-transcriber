FROM python:3.10

MAINTAINER Sebastian Moßburger <sebastian-markgraf@t-online.de>

WORKDIR /backend
COPY pyproject.toml .
RUN pip install pdm
RUN pdm install
# Copy project
COPY . .


# Run uvicorn
CMD ["pdm", "run", "uvicorn", "--host", "0.0.0.0", "src.backend:app", "--port", "42069"]
