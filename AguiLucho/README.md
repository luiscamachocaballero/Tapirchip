Uno de los objetivos buscados en el proyecto TapirNet es que la nave UAV alcance la posición de un objetivo (nodo sumidero) ubicado más allá del alcance del radio control manual., una vez alcanzado el objetivo que encienda la radio e inicie una recolección de la data acumulada en el nodo sumidero, terminada esta tarea que vuelva al punto de partida. A este sistema completo se le ha denominado AguiLucho. 
Dentro de la nave, las partes que componen el hardware telemático necesario son: una computadora y/o procesador, un piloto automático y una radio. A priori, dos plataformas fueron consideradas: 
1.	Pixhawk + Gumstix COM Overo Summit + radio WiFi 802.11n chipset Ralink RT 3572 
2.	AeroCore + Gumstix COM DuoVero Zephyr (incluye radio WiFi 802.11n Wi2Wi W2CBW0015)  
Ambas plataformas son similares, ambas cuentan con microprocesadores ARM Cortex-M4 MCU para la parte de piloto automático y para la parte del software de misión, en ambos casos se emplea computers-on-module del fabricante Gumstix. 
##En la figura podemos ver un diagrama de flujo del funcionamiento de AguiLucho. La computadora de propósito específico, Computer on Module ó COM, gobierna tanto al piloto automático como a la radio. El algoritmo del sistema es el siguiente: 
1.	Las coordenadas del destino serán grabadas en el piloto automático.  
2.	La COM recibirá la altitud y la posición como datos del piloto. 
3.	Cuando la nave alcance la posición del objetivo, la COM encenderá la radio y ordenará el envío de paquetes de establecimiento de enlace 
4.	Establecido el enlace se transfieren las imágenes desde el nodo sumidero hasta la UAV 
5.	La COM controla el tiempo y el estado de la batería de la UAV 
6.	Terminada la transferencia o alcanzado un nivel crítico de carga de batería, la COM ordena el regreso a la posición inicial 
 

DroneKit, una API de código abierto escrita en Python, permite desarrollar apps que se ejecuten directamente en la computadora a bordo y se comuniquen con el piloto automático Pixhawk mediante un enlace de baja latencia; DroneKit también permite el desarrollo de apps de control remoto vía web. La API se conecta con Pixhawk a través del protocolo de comunicación MAVLink, gracias a este protocolo, la API tiene acceso a los datos de la telemetría o a los parámetros del dron a través de Bluetooth, Wi-Fi o el sistema de radio 3DR. Más aún, DroneKit puede controlar el movimiento y las operaciones de la nave. Esta API permite a los desarrolladores, entre otras funciones: 
1.	Desarrollar aplicaciones que mejoren el vuelo en piloto automático. 
2.	Proporcionar características inteligentes a un dron como la visión por ordenador, la planificación de la ruta o el modelado en 3D. 
3.	Permitir a un vehículo aéreo seguir objetivos mediante GPS. 
4.	Facilitar el seguimiento de una ruta marcada con receptores GPS. 
5.	Controlar cámaras y obtener información de telemetría. 
6.	Generación de bitácoras de datos para posterior análisis. 
  
##Figura 21 Diagrama de flujo del programa AguiLucho 
DroneKit se puede instalar en sistemas operativos Linux, Windows y Mac OS X y funciona tanto en desktops y laptops como en smartphones. También se puede acceder a la API en la nube, donde se disponen del servicio DroneShare (mapeo de vuelos en tiempo real y compartición de datos de misiones y rutas con drones).  
Una aplicación desarrollada con DroneKit en Python suele ejecutarse en una computadora abordo corriendo S.O. Linux, pero durante las pruebas de desarrollo lo más lógico y habitual es probar los prototipos en una computadora estándar conectada a un piloto automático. 
