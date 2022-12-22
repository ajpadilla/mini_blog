import pika

import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel()
print(' [*] Waiting for messages. To exit press CRTL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

    '''
        Es un error común perder el basic_ack. Es un error fácil, pero las consecuencias son graves. Los mensajes se volverán a enviar cuando su cliente se cierre (lo que puede parecer una nueva entrega aleatoria), pero RabbitMQ consumirá cada vez más memoria, ya que no podrá liberar ningún mensaje sin recuperar.
        Para depurar este tipo de error, puede usar rabbitmqctl para imprimir el campo message_unacknowledged:
        sudo rabbitmqctl list_queues name messages_ready messages_unacknowledged

    '''


'''
    Para vencer eso, podemos usar el método de canal Channel#basic_qos con la configuración prefetch_count=1 . 
    Esto utiliza el método de protocolo basic.qos para decirle a RabbitMQ que no envíe más de un mensaje a un trabajador a la vez. 
    O, en otras palabras, no envíe un nuevo mensaje a un trabajador hasta que haya procesado y reconocido el anterior. 
    En cambio, lo enviará al próximo trabajador que aún no esté ocupado. 
    Si todos los trabajadores están ocupados, su cola puede llenarse. 
    Querrá vigilar eso, y tal vez agregar más trabajadores, o usar el mensaje TTL .
'''

channel.basic_qos(prefetch_count=1)
'''
se elimina el parametro auto_ack, evita que rabbit requiera de un mesaje de recibido para saber si se proceso el mensaje
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
Ahora el trabajador se vera en la obligacion de enviar un acuse de recibido al procesar el mensaje, 
una vez que termine con la tarea
Rabbit destribuye de forma equitativa en envio de tares a los diferentes workers.

Usando este código podemos estar seguros de que incluso si matas a un trabajador usando CTRL+C mientras estaba procesando un mensaje, 
no se perderá nada. Poco después de que el trabajador muera, se volverán a enviar todos los mensajes no reconocidos.

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)


El acuse de recibo debe enviarse por el mismo canal que recibió la entrega.
Los intentos de reconocer usando un canal diferente darán como resultado una excepción de protocolo a nivel de canal. Consulte la guía de documentos sobre confirmaciones para obtener más información.
 '''
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()