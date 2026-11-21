FROM python:3.12

ARG USERNAME=developer
ARG USER_UID=1000
ARG USER_GID=1000

# Create group and user
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd \
        --uid ${USER_UID} \
        --gid ${USER_GID} \
        --create-home \
        --shell /bin/bash \
        ${USERNAME}

WORKDIR /workspace


RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    ssh \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app/ ./app/

EXPOSE 8000

USER ${USERNAME}