from threading import Thread, Semaphore
import threading

max_capacidad = Semaphore(20)
sofa = Semaphore(4)
contadorSofa = 4
silla_barbero = Semaphore(3)
cuentaSilla_b = 3
coord = Semaphore(3)
mutex1 = Semaphore(1)
mutex2 = Semaphore(1)
mutex3 = Semaphore(1)
mutex4 = Semaphore(1)
mutex5 = Semaphore(1)
mutex6 = Semaphore(1)
mutex7 = Semaphore(1)
mutex8 = Semaphore(1)
mutex9 = Semaphore(1)
mutex10 = Semaphore(1)
mutex11 = Semaphore(1)
cliente_listo = Semaphore(0)
dejar_silla_b = [threading.Semaphore(0) for i in range(3)]
pago = Semaphore(0)
recibo = [threading.Semaphore(0) for i in range(50)]
terminado = [threading.Semaphore(0) for i in range(50)]
cola1 = list()
cola2 = list()
cola3 = list()
contador=0
cuenta=0
cuenta_b=0
semaforoDecrementado = False

def Entrar_tienda(i):
    print("Entro un nuevo cliente "+str(i+1)+" a la tienda")

def sentarse_en_sofa(i):
    print("El cliente "+str(i+1)+" se sentó en el sofá")

def levantarse_del_sofa(i):
    print("El cliente "+str(i+1)+" se levantó del sofá")

def sentarse_en_silla_de_barbero(i):
    print("El cliente "+str(i+1)+" se sentó en la silla del barbero")

def dejar_silla_barbero(i,j):
    print("EL cliente "+str(i+1)+" dejo la silla del barbero "+str(j+1))

def pagar(i):
    print("El cliente "+str(i+1)+" pago")

def salir_tienda(i):
    print("El cliente "+str(i+1)+" salió de la tienda")

def cliente():
    #boolean condicion //si esta libre alguna silla de barbaero y no hay personas esperando
    #numcliente
 
    global contadorSofa
    global cuentaSilla_b

    max_capacidad.acquire()
    mutex1.acquire()
    global cuenta
    numcliente=cuenta
    cuenta=cuenta+1
    Entrar_tienda(numcliente)
    mutex1.release()

    mutex3.acquire()
    mutex4.acquire()
    condicion = contadorSofa==4 and cuentaSilla_b>0 
    #guardo el valor de la ejecucion en un momento determinado (cuando el cliente entra)
    mutex3.release()
    mutex4.release()


    #si hay espacio libre no es necesario pasar por el sofa
    if(not condicion):
        mutex3.acquire()
        contadorSofa=contadorSofa-1
        mutex3.release()  
        mutex8.acquire() 
        #fue necesario agregar esta exclucion para que se organicen de forma ordenada las personas que van entrando
        sofa.acquire()
        sentarse_en_sofa(numcliente)
        mutex8.release()

    mutex4.acquire()
    cuentaSilla_b = cuentaSilla_b-1
    mutex4.release()
    silla_barbero.acquire()
      

    if(not condicion):
        mutex3.acquire()
        levantarse_del_sofa(numcliente)
        contadorSofa=contadorSofa+1     
        sofa.release()
        mutex3.release()
    
    
    mutex2.acquire()
    sentarse_en_silla_de_barbero(numcliente)
    cola1.append(numcliente)
    mutex2.release()
    cliente_listo.release()
    global terminado
    terminado[numcliente].acquire()

    mutex6.acquire()
    numBarbero= cola2[0]
    cola2.remove(cola2[0])
    mutex6.release()

    dejar_silla_barbero(numcliente,numBarbero)
    dejar_silla_b[numBarbero].release()

    pago.release()
    mutex7.acquire()
    pagar(numcliente)
    cola3.append(numcliente)
    mutex7.release()
    if(numcliente==49):
    #si es el ultimo cliente es necesario enviar un signal adicional para que no quede esperando en la cola de cajero por siempre
        pago.release()

    recibo[numcliente].acquire()
    salir_tienda(numcliente)
    max_capacidad.release()
    
def cortar_pelo(i,j):
    print("EL barbero "+str(j+1)+" esta cortando cabello al cliente "+str(i+1))

def barbero():

    global cuenta_b
    mutex5.acquire()
    numBarbero=cuenta_b
    cuenta_b=cuenta_b+1
    mutex5.release()

    while(True):
        cliente_listo.acquire()
        mutex2.acquire()
        cliente_b = cola1[0]
        cola1.remove(cola1[0])
        mutex2.release()
        coord.acquire()
        cortar_pelo(cliente_b,numBarbero)
        coord.release()

        mutex6.acquire()
        terminado[cliente_b].release()
        cola2.append(numBarbero)
        mutex6.release()

        dejar_silla_b[numBarbero].acquire()
        mutex4.acquire()
        global cuentaSilla_b
        cuentaSilla_b = cuentaSilla_b+1
        mutex4.release()
        silla_barbero.release()

        

def aceptar_pago(i):
    print("pago aceptado del cliente "+str(i+1))

def  cajero():
    mutex11.acquire()
    global semaforoDecrementado
    if(not semaforoDecrementado):
        pago.acquire()# dos o mas clientes en la cola para pagar
        #se esta decrementando el semaforo a -1
        # ya que esta pensado para inicializar solo con valores positivos
        # y de los tres cajeros solo es necesario que uno decremente el contador y no los tres
        semaforoDecrementado= True
    mutex11.release()

    while(True):
        mutex10.acquire()
        pago.acquire()
        coord.acquire()
        mutex7.acquire()
        numCliente_b=cola3[0]
        cola3.remove(cola3[0])
        mutex7.release()
        aceptar_pago(numCliente_b)
        recibo[numCliente_b].release()
        coord.release()
        mutex10.release()

for i in range(50):
    Thread( target=cliente, args=()).start()

for i in range(3):
    Thread( target=barbero, args=()).start()

for i in range(3):
    Thread( target=cajero, args=()).start()
