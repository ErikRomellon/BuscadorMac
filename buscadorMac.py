#Programa realizado por Erik Jesús Romellón Lorenzana

import paramiko, os, subprocess, re
from time import sleep

listaIP = []
print("Bienvenido al buscador de MAC.\nIngresa un rango de direcciones ip para escanear\n")
def busqueda():
    ip_inicio = input("Ingresa ip de inicio: ")
    ip_final = input("Ingresa ip de final: ")

    def Get_Host(x):
        puntos = 0
        posContador = 0

        for i in x:
            if i == ".":
                puntos = puntos + 1
            if puntos == 3:
                return (x[0:posContador + 1], x[posContador + 1:])
                break
            posContador += 1

    Network, primerHost = Get_Host(ip_inicio)
    Network, ultimoHost = Get_Host(ip_final)

    emptyString = ""

    Counter = 0

    print("REALIZANDO BUSQUEDA DE HOSTS ACTIVOS EN "+Network +primerHost+" - "+ultimoHost)
    for i in range(int(primerHost), int(ultimoHost) + 1):
        proceso = subprocess.getoutput("ping -n 1 " + Network + str(i))
        emptyString += proceso
        buscar = re.compile(r"TTL=")
        mo = buscar.search(emptyString)
        try:
            if mo.group() == "TTL=":
                print("Host " + Network + str(i) + " está Up")
                ip = Network + str(i)
                listaIP.append(ip)
        except:
            print("Host " + Network + str(i) + " está Down")

        emptyString = ""
busqueda()

#Despliegue de elementos encontrados
if listaIP:
    print("\nSE HAN ENCONTRADO LOS SIGUIENTES HOSTS ACTIVOS:")
    for ip in listaIP:
        print(ip)
    enter = input("Presione enter para inciar la configuracion ")



def buscarMac():

    #Realiza las verificaciones de la marca del switch y modelo

    output = devices_access.recv(300).decode("utf-8")
    devices_access.send("show mac address-table address "+mac+"\n")
    output = devices_access.recv(300).decode("utf-8")
    sleep(5)
    output = devices_access.recv(300).decode("utf-8")
    print(output)
    self = re.findall(r'(Self)', output)
    management = re.findall(r'(Management)', output)
    gi = re.findall(r'(Gi)',output)

    if self or management or gi:
        print(f"\nSE HA ENC0NTRADO EN {ip} LA MAC {mac}")
        print(output)
    else:
        print(f"MAC no encontrada en {ip}")


#Inicio de configuracion
if listaIP:
    for ip in listaIP:
        print(f"\n\tCONFIGURANDO {ip}")
        usuario = input(f"Ingrese nombre de usuario de {ip}: ")
        password = input(f"Ingrese el password de {ip}: ")

        # conexion por SSH
        try:
            print(f"\nIntentando establecer conexion con {ip}")
            cliente = paramiko.SSHClient()
            cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            cliente.connect(hostname=ip, port=22, username=usuario, password=password)
            devices_access = cliente.invoke_shell()
            print("Conexion realizada vía SSH!!!\n\n")
            sleep(1)
            os.system("cls")
            print(f"\n\tVerificando compatibilidad de {ip} ...\n")
            sleep(1)
            output = devices_access.recv(100).decode("utf-8")
            verificar = re.findall('>', output)
            if verificar:
                if verificar[0] == '>':
                    enable = input("Ingresa contraseña enable: ")
                    devices_access.send("enable\n")
                    sleep(10)
                    devices_access.send(enable+"\n")
            sleep(1)
            mac = input("\nIngresa direccion mac a buscar: ")
            buscarMac()

        #Excepciones
        except paramiko.ssh_exception.AuthenticationException:
            print(f"No fue posible hacer conexion con {ip}, usuario o contraseña incorrecta ")
        except paramiko.ssh_exception.NoValidConnectionsError:
            print(f"\nERROR!! : No se puede conectar al puerto 22 en {ip}")
        except TimeoutError:
            print("Se produjo un error durante el intento de conexión ya que la parte conectada no respondió adecuadamente tras un periodo de tiempo, o bien se produjo un error en la conexión establecida ya que el host conectado no ha podido responder")
else:
    print("\n\n\tNo se ha encontrado ningun equipo en la red, verifica conexion o rango de direccion ip")

print("\n\n\tEjecucion de programa finalizado")
fin = input("Presiona enter para cerrar el programa")