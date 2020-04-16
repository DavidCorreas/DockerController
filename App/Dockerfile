FROM openjdk:8-jre

COPY easydocker-0.0.1-SNAPSHOT.jar /webapp/app.jar

WORKDIR /webapp

EXPOSE 8443

CMD ["java" , "-jar", "app.jar", \
    "--spring.jpa.hibernate.ddl-auto=create-drop", \
    "--spring.datasource.url=jdbc:mysql://mysql-database:3306/easy-docker-db?useSSL=false&allowPublicKeyRetrieval=true", \
    "--spring.datasource.username=root", \
    "--spring.datasource.password=1234", \
    "--server.port=8443", \
    "--spring.rabbitmq.host=rabbitmq", \
    "--spring.rabbitmq.port=5672", \
    "--spring.rabbitmq.username=rabbituser", \
    "--spring.rabbitmq.password=1234"]