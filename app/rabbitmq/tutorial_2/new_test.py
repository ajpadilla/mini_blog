import pika
import sys

# Evitar realiazar tareas que consuman muchos recursos de inmediato y tener que esperar a que se completen
#

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()

'''
    Cuando RabbitMQ se cierra o falla, olvidará las colas y los mensajes a menos que le indique que no lo haga. 
    Se requieren dos cosas para asegurarse de que los mensajes no se pierdan: debemos marcar tanto la cola como los mensajes como duraderos.
    Aunque este comando es correcto por sí mismo, no funcionará en nuestra configuración. Eso es porque ya hemos definido una cola llamada hola que no es duradera. 
    RabbitMQ no le permite redefinir una cola existente con diferentes parámetros y devolverá un error a cualquier programa que intente hacerlo. 
    Pero hay una solución rápida: declaremos una cola con un nombre diferente, por ejemplo task_queue :
'''
channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"

'''
debemos marcar nuestros mensajes como persistentes, proporcionando una propiedad de modo de entrega con el valor de pika.spec.PERSISTENT_DELIVERY_MODE
'''
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    )
)
print(" [X] Sent %r" % message)
connection.close()
