ARG PYTHON_BASE=3.10-slim

FROM python:$PYTHON_BASE as builder

MAINTAINER Sebastian Moßburger <sebastian-markgraf@t-online.de>

WORKDIR /backend


RUN pip install -U pdm

COPY pyproject.toml pdm.lock README.md src/ .
# Required for PDM install of package
RUN pdm install --check --prod --no-editable


FROM python:$PYTHON_BASE

COPY --from=builder /backend/.venv/ /backend/.venv/
ENV PATH="/backend/.venv/bin:$PATH"

COPY src/ /backend/src/

CMD ["fastapi", "run", "/backend/src/whatsapp_transcribe/__main__.py", "--port", "80"]
