FROM python:3.10-slim

WORKDIR /bot

COPY bot.py .

RUN pip install flask requests

EXPOSE 8080

CMD ["python", "bot.py"]
