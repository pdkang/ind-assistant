FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends openssl libssl-dev
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
