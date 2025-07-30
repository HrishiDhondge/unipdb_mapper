FROM python:3.11-slim
WORKDIR /app

# Installing the unipdb_mapper
RUN pip install unipdb_mapper

# Default command
CMD ["unipdb"]
