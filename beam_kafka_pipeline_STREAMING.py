import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.kafka import ReadFromKafka, WriteToKafka
from apache_beam.coders import StrUtf8Coder
from kafka import KafkaProducer

# Define Beam pipeline options
options = PipelineOptions()

# Create Kafka producer config
producer_config = {
    'bootstrap.servers': 'localhost:9092',
    'max.request.size': 10485760 
}

def process_message(message):
    key, value = message
    return (key, value.decode('utf-8').upper())  # For example, uppercase the value

with beam.Pipeline(options=options) as pipeline:
    (
        pipeline
        | 'ReadFromKafka' >> ReadFromKafka(
            consumer_config={'bootstrap.servers': 'localhost:9092', 'group.id': 'my_group'},
            topics=['input-topic'],
            key_coder=StrUtf8Coder(),
            value_coder=StrUtf8Coder()
        )
        | 'ProcessMessages' >> beam.Map(process_message)
        | 'WriteToKafka' >> WriteToKafka(
            producer_config=producer_config,
            topic='output-topic',
            key_coder=StrUtf8Coder(),
            value_coder=StrUtf8Coder()
        )
    )