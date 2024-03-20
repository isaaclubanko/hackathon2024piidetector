FROM python:3.10

# Add application code
ADD . /app

# Install dependencies
RUN pip install /app/

# Start app
EXPOSE 8080

CMD pii-detector