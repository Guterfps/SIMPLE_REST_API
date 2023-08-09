from kafka import KafkaProducer
bootstrap_servers = ['kafka1:9092']

def SendMsg(msg):
    topicName = 'Notifications'
    producer = KafkaProducer(bootstrap_servers = bootstrap_servers, 
                            api_version = (2, 0, 2))
    producer = KafkaProducer()
    ack = producer.send(topicName, b' ' + msg.encode('utf-8'))
    metadata = ack.get()
    print(metadata.topic)
    print(metadata.partition)
