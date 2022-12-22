import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

'''
    Como recordará anteriormente, estábamos usando colas que tenían nombres específicos (¿recuerda hola y task_queue ?).
    Ser capaz de nombrar una cola era crucial para nosotros: necesitábamos señalar a los trabajadores la misma cola. 
    Dar un nombre a una cola es importante cuando desea compartir la cola entre productores y consumidores.

    Pero ese no es el caso de nuestro registrador. 
    Queremos conocer todos los mensajes de registro, no solo un subconjunto de ellos. 
    También estamos interesados solo en los mensajes que fluyen actualmente, no en los antiguos. 
    Para resolver eso necesitamos dos cosas.

    En primer lugar, cada vez que nos conectamos a Rabbit, necesitamos una cola nueva y vacía. 
    Para hacerlo, podríamos crear una cola con un nombre aleatorio o, mejor aún, dejar que el servidor elija un nombre de cola aleatorio para nosotros. 
    Podemos hacer esto proporcionando un parámetro de
'''
result = channel.queue_declare(queue='', exclusive=True)

'''
    Ahora necesitamos decirle al intercambio que envíe mensajes a nuestra cola. 
    Esa relación entre el intercambio y una cola se llama enlace .
'''
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] %r" % body)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
