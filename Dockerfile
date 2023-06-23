FROM python:3.8
RUN pip install uvicorn
RUN pip install chromadb
RUN pip install --force-reinstall fastapi==0.85.1
COPY server.py .
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]