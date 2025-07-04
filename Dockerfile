FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -e .
EXPOSE 8000
CMD ["coexum","dashboard","serve","--host","0.0.0.0"]
