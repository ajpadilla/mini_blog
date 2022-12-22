import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

'''
    Definiendo una exchage de tipo fanout(enviara el mensaje a todas las colas conocidas, sin necesidad de identificador)
    
    para mostrar toda la lista de exchanges
    sudo rabbitmqctl list_exchanges
'''
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

'''
    publica en el exchange con el nombre logs y dejamos que rabbit nombre las cosas de forma automatica
    
    El significado de una clave vinculante depende del tipo de intercambio. 
    Los intercambios fanout , que usamos anteriormente, simplemente ignoraron su valor.
'''
channel.basic_publish(exchange='logs', routing_key='', body=message)

print(" [x] Sent %r" % message)
connection.close()