FROM python:3.11.2

ENV EXCLUSION_MS_API_IP='localhost:8000'

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD streamlit run home.py --server.port 8501