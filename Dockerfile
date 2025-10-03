#############################
# BUILDER STAGE
#############################
FROM python:3.10-slim AS builder

# install system deps needed for build
RUN apt-get update -o Acquire::Max-FutureTime=100000 \
 && apt-get install -y --no-install-recommends \
        build-essential \
        git \
 && rm -rf /var/lib/apt/lists/*

# create venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# install annoy first (binary-only)
RUN pip install --no-cache-dir annoy

# copy and install python dependencies
COPY docker-requirements.txt .
RUN pip install --no-cache-dir -r docker-requirements.txt \
 && pip install --no-cache-dir git+https://github.com/FutureComputing4AI/EMBER2024.git

#############################
# FINAL STAGE (REBASING)
#############################
FROM python:3.10-slim

# install runtime-only deps (no compiler, just minimal)
RUN apt-get update -o Acquire::Max-FutureTime=100000 \
 && apt-get install -y --no-install-recommends \
        libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# copy python virtual env from builder
COPY --from=builder /opt/venv /opt/venv

# copy defender app
COPY defender /opt/defender/defender

# set non-root user
RUN groupadd -r defender && useradd --no-log-init -r -g defender defender
USER defender

# working dir
WORKDIR /opt/defender/

# expose API port
EXPOSE 8080

# env vars
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/opt/defender"
ENV DF_MODEL_PATH models/lgbm_model_0.txt
ENV DF_MODEL_THRESH 0.5
ENV DF_MODEL_NAME thrember
ENV DF_MODEL_BALL_THRESH 0.25
ENV DF_MODEL_HISTORY 10000
ENV MPLCONFIGDIR=/opt/defender/.matplotlib
# run app
CMD ["python", "-m", "defender"]
