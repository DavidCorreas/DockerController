FROM openjdk:8-jre

COPY easydocker-0.0.1-SNAPSHOT.jar /webapp/app.jar

WORKDIR /webapp

EXPOSE 443

CMD ["java" , "-jar", "app.jar", \
    "--spring.jpa.hibernate.ddl-auto=update", \
    "--spring.datasource.url=jdbc:mysql://mysql-master:3306/easy-docker-db?useSSL=false&allowPublicKeyRetrieval=true", \
    "--spring.datasource.username=root", \
    "--spring.datasource.password=1234", \
    "--spring.datasource.driverClassName=com.mysql.cj.jdbc.Driver", \
    "--server.port=443", \
    "--spring.rabbitmq.host=rabbitmq", \
    "--spring.rabbitmq.port=5672", \
    "--spring.rabbitmq.username=rabbituser", \
    "--spring.rabbitmq.password=1234"]