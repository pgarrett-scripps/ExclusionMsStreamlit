FROM python:3.10.7

ENV EXCLUSION_API_IP='localhost:8000'

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD streamlit run home.py --server.port 8501