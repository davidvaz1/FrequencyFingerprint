FROM openjdk:17-alpine
RUN apk add --no-cache python3
WORKDIR /app
COPY . .
RUN javac FrequencyFingerprint.java
EXPOSE 8080
CMD ["python3", "server.py"]
