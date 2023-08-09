from kafka import KafkaConsumer
import sys
bootstrap_servers = ["kafka1:9092"]
topicName = "Notifications"
consumer = KafkaConsumer(topicName,
bootstrap_servers=bootstrap_servers,
auto_offset_reset='earliest', api_version=(2, 0, 2))
try:
    for message in consumer:
        print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))
except KeyboardInterrupt:
    sys.exit()