# Contenido {#contenido .TOC-Heading}

[Provision an Azure SQL Database
[2](#provision-an-azure-sql-database)](#provision-an-azure-sql-database)

[Create the test workload
[4](#create-the-test-workload)](#create-the-test-workload)

[Enable and configure Query Store
[5](#enable-and-configure-query-store)](#enable-and-configure-query-store)

[Analyze execution plans and add a missing index
[6](#analyze-execution-plans-and-add-a-missing-index)](#analyze-execution-plans-and-add-a-missing-index)

[Use DMVs to find the most expensive queries
[9](#use-dmvs-to-find-the-most-expensive-queries)](#use-dmvs-to-find-the-most-expensive-queries)

[Simulate and detect a plan regression with Query Store
[12](#simulate-and-detect-a-plan-regression-with-query-store)](#simulate-and-detect-a-plan-regression-with-query-store)

[Provocar la regresión
[14](#provocar-la-regresión)](#provocar-la-regresión)

[Usar el almacenamiento de querys para ver la regresión
[18](#usar-el-almacenamiento-de-querys-para-ver-la-regresión)](#usar-el-almacenamiento-de-querys-para-ver-la-regresión)

[Apply a Query Store hint
[22](#apply-a-query-store-hint)](#apply-a-query-store-hint)

[Identify and resolve blocking
[25](#identify-and-resolve-blocking)](#identify-and-resolve-blocking)

[Cleanup [28](#cleanup)](#cleanup)

# Provision an Azure SQL Database

![](imagenes/media/image1.png){width="5.905555555555556in"
height="4.610416666666667in"}

![](imagenes/media/image2.png){width="5.905555555555556in"
height="3.70625in"}

# Create the test workload

Conexión de la bbdd con ssms

![](imagenes/media/image3.png){width="3.9172134733158357in"
height="0.4375612423447069in"}

Poblado de la bbdd

![](imagenes/media/image4.png){width="5.081395450568679in"
height="4.501791338582677in"}

Verificado de creación de las tablas

![](imagenes/media/image5.png){width="5.063206474190726in"
height="1.6668996062992125in"}

# Enable and configure Query Store

Inicialización de query store ( sirve para c apturar los tiempos de
ejecución y estadísticas desde la bbdd)

![](imagenes/media/image6.png){width="5.905555555555556in"
height="3.4291666666666667in"}

Verificar que esta activo

![](imagenes/media/image7.png){width="5.5424398512685915in"
height="2.614948600174978in"}

Si en vez de read_write estuviera en read only significaría que está
lleno el almacenamiento

# Analyze execution plans and add a missing index

![](imagenes/media/image8.png){width="5.905555555555556in"
height="6.9534722222222225in"}

Resultados primera query

![](imagenes/media/image9.png){width="5.905555555555556in"
height="2.1131944444444444in"}

Creación del índice para el optimizado

![](imagenes/media/image10.png){width="5.407004593175853in"
height="2.531603237095363in"}

Resultados tras

![](imagenes/media/image11.png){width="5.905555555555556in"
height="3.9402777777777778in"}

# Use DMVs to find the most expensive queries

Querys que mas cpu usan

![](imagenes/media/image12.png){width="5.905555555555556in"
height="3.966666666666667in"}

Búsqueda del índice faltante

![](imagenes/media/image13.png){width="5.761220472440945in"
height="7.813590332458443in"}

Hacemos una query al indice que falta

![](imagenes/media/image14.png){width="5.905555555555556in"
height="2.7930555555555556in"}

# Simulate and detect a plan regression with Query Store

Preparación del escenario

![](imagenes/media/image15.png){width="5.1361329833770775in"
height="3.0316732283464565in"}

Eliminado de los índices

![](imagenes/media/image16.png){width="5.905555555555556in"
height="1.8409722222222222in"}

Creación del nuevo índice

![](imagenes/media/image17.png){width="5.905555555555556in"
height="2.347916666666667in"}

Añadir datos

![](imagenes/media/image18.png){width="5.905555555555556in"
height="2.5479166666666666in"}

Actualizamos las estadísticas para que el optimizador vea el cambio

![](imagenes/media/image19.png){width="4.844425853018373in"
height="1.8648436132983377in"}

Creacion de un procedure

![](imagenes/media/image20.png){width="4.917352362204724in"
height="4.990279965004374in"}

## Provocar la regresión 

Limpiamos el cache de los procedimientos

![](imagenes/media/image21.png){width="5.905555555555556in"
height="6.897222222222222in"}

Ahora limpiamos el cache y ejecutamos el proceso lento

![](imagenes/media/image22.png){width="5.905555555555556in"
height="6.597222222222222in"}

Lazamos el procedimiento con el id de cliente numero 29485

![](imagenes/media/image23.png){width="5.905555555555556in"
height="6.611111111111111in"}

Enviamos los resultados al almacenamiento

![](imagenes/media/image24.png){width="4.604809711286089in"
height="2.156550743657043in"}

## Usar el almacenamiento de querys para ver la regresión 

Ver planes

![](imagenes/media/image25.png){width="5.905555555555556in"
height="3.8208333333333333in"}

![](imagenes/media/image26.png){width="5.905555555555556in"
height="4.777777777777778in"}

Forzar el mejor plan

![](imagenes/media/image27.png){width="5.905555555555556in"
height="3.254166666666667in"}

Probar el plan

![](imagenes/media/image28.png){width="5.905555555555556in"
height="6.188888888888889in"}

Limpiado

![](imagenes/media/image29.png){width="5.905555555555556in"
height="2.9298611111111112in"}

# Apply a Query Store hint

Aplicamos esta query

![](imagenes/media/image30.png){width="5.905555555555556in"
height="7.5in"}

Buscamos la query mas lenta

![](imagenes/media/image31.png){width="5.625785214348206in"
height="3.0837642169728783in"}

Frozamos para que la query se haga en un solo hilo

![](imagenes/media/image32.png){width="4.604809711286089in"
height="3.052509842519685in"}

Quitamos las pistas

![](imagenes/media/image33.png){width="4.761081583552056in"
height="2.427422353455818in"}

# Identify and resolve blocking

Primera ventana

![](imagenes/media/image34.png){width="5.905555555555556in"
height="2.5770833333333334in"}

Segunda ventana

![](imagenes/media/image35.png){width="5.905555555555556in"
height="3.4930555555555554in"}

Consulta bloqueada

Tercera ventana

![](imagenes/media/image36.png){width="5.905555555555556in"
height="2.2354166666666666in"}

Investigar el bloqueo

![](imagenes/media/image37.png){width="5.905555555555556in"
height="1.8923611111111112in"}

Volvemos a la ventana 1 para resolver el bloqueo

![](imagenes/media/image38.png){width="5.417422353455818in"
height="2.3024048556430445in"}

Volver a la ventana 2 para ver que se resuelto el problema

![](imagenes/media/image39.png){width="5.905555555555556in"
height="1.8694444444444445in"}

# Cleanup

Eliminar la tabla de test

![](imagenes/media/image40.png){width="4.6360640857392825in"
height="2.156550743657043in"}

Unforzar los clanes y pista de las querys

![](imagenes/media/image41.png){width="5.905555555555556in"
height="4.017361111111111in"}

Eliminación de la bbdd desde el portal de azure

![](imagenes/media/image42.png){width="5.905555555555556in"
height="2.251388888888889in"}
