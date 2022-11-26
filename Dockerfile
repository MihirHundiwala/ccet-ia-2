FROM python:3.8.10
COPY ./src /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000 
ENTRYPOINT [ "flask"]
CMD ["run", "-h", "0.0.0.0", "-p", "5000"]