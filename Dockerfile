FROM python:3.9.10-buster

# Node.jsのインストール
RUN curl -sL https://deb.nodesource.com/setup_12.x |bash - \
    && apt-get install -y --no-install-recommends \
    nodejs

RUN pip install --upgrade pip  
RUN pip install fastapi uvicorn pandas streamlit SQLAlchemy jupyterlab


# docker run -it -p 8501:8501 -p 8888:8888 -v $PWD:/work api-st-sql-lab bash
# jupyter lab --allow-root --ip 0.0.0.0