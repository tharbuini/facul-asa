import pika
import logging

logger = logging.getLogger(__name__)
logging.getLogger("pika").propagate = False
FORMAT = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)s]%(levelname)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)

class Publisher(object):
    def __init__(self, config, exchange:str):
        self.config = config
        self.exchange = exchange
        self.queue = exchange # recebe o mesmo nome do exchange, então utilizei a mesma variável
    
    def publish(self, routing_key, message):
        try:        
            connection = self.create_connection()
            channel = connection.channel()
            channel.exchange_declare(exchange=self.exchange, exchange_type = 'topic')
            channel.queue_declare(queue=self.queue)
            channel.queue_bind(exchange=self.exchange, queue=self.queue, routing_key=routing_key)

            channel.basic_publish(exchange=self.exchange, 
                                routing_key=routing_key,                               
                                body=message)
        except Exception as e:
            logger.error(f'Erro na conexão do RabbitMQ ==> {e}')       

    def create_connection(self):
        param = pika.ConnectionParameters(host=self.config['host'], port=self.config['port'])
        return pika.BlockingConnection(param)

