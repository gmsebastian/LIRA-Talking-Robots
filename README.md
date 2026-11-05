# LIRA Talking Robots

Este es un repositorio para correr nodos de ROS2 y un LLM local para que los robots interactúen
con las personas en un evento social.

## Requisitos

- Ubuntu 22.04 o posterior.
- [ROS2](https://docs.ros.org/en/humble/Installation.html) (Humble o posterior).
- [Ollama](https://ollama.com/download).

> [!NOTE]
> Dado que se ejecuta un LLM localmente, se **recomienda extensivamente** correr este proyecto en
> un sistema con GPU dedicada; sin embargo, se han logrado buenos resultados con una iGPU
> Intel Iris Xe TigerLake.

## Instalación

Antes de compilar los paquetes de ROS2, es imperativo correr el script `Setup.sh`, el cual
creará un entorno virtual de Python donde se instalarán las dependencias necesarias.

```bash
./Setup.sh
```

> [!IMPORTANT]
> Reabrir la teminal después de ejecutar el script anterior.

Una vez instaladas las dependencias, compilar los tres paquetes de ROS2

```bash
cd ros2_ws
colcon build
source install/setup.bash
```

Por último, cargar el modelo con ollama. Dependiendo de la conexión a internet, esto puede tardar
alrededor de 30 minutos.

```bash
ollama run <modelo>
```

Recomendamos usar `gemma4:e4b` para GPUs dedicadas y `gemma4:e2b` para iGPUs.

## Correr el proyecto

Una vez que la instalación se haya completado exitosamente, abrir 4 terminales y correr los
siguientes comandos:

### Terminal 1

```bash
ros2 run speech2text faster_whisper_asr
```

### Terminal 2

```bash
ros2 run text2speech t2s
```

### Terminal 3

```bash
ros2 run llm_planning ollama_planning
```

### Terminal 4

????

Continuará
