FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    curl \
    wget \
    python3 \
    python3-pip \
    python3-venv \
    # Updated OpenGL / GUI libraries for Ubuntu 24.04
    libgl1 \
    libglx-mesa0 \
    libglib2.0-0 \
    v4l-utils \
    ffmpeg \
    # Serial and hardware tools
    minicom \
    python3-serial \
    # GUI display support (X11)
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

ARG USERNAME=rov
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Delete existing user first, then group, before creating 'rov'
RUN if getent passwd $USER_UID >/dev/null 2>&1; then userdel -r $(getent passwd $USER_UID | cut -d: -f1); fi \
    && if getent group $USER_GID >/dev/null 2>&1; then groupdel $(getent group $USER_GID | cut -d: -f1); fi \
    && groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && usermod -aG dialout,video $USERNAME

WORKDIR /workspace

USER $USERNAME