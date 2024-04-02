# The OS we're running the app under
FROM ubuntu:22.04

# set the working directory in the container
WORKDIR /src

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# install curl
RUN apt-get update && apt-get install -y curl

# install rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# install python
RUN apt-get update && apt-get install -y \
    python3 \
    python3-setuptools \
    python3-pip \
    python3-dev

# install dependencies for librealsense
RUN apt-get -y install libusb-1.0-0-dev

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python3 -m pip install -r requirements.txt

# add a non-root user to run the app
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Switch to non-root user 
USER appuser 

# Copy the source code into the container.
COPY . .