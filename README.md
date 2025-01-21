# Proyecto 7 y Medio 🎴

¡Bienvenido al proyecto **7 y Medio**! Este proyecto implementa una versión digital del popular juego de cartas, combinando estrategias de programación, diseño web y bases de datos.

## Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Miembros del Equipo](#miembros-del-equipo)
- [Requisitos Previos](#requisitos-previos)
- [Instalación de MySQL Connector](#instalación-de-mysql-connector)
  - [En Windows](#en-windows)
  - [En Linux](#en-linux)
  - [Resolución de Errores de Privilegios](#resolución-de-errores-de-privilegios)
- [Página Web](#página-web)

---

## Descripción del Proyecto
El proyecto **7 y Medio** es una implementación digital del juego de cartas "Siete y Medio", desarrollado como parte de un proyecto educativo. Combina diferentes áreas de programación:
- **Back-end:** Lógica del juego y manejo de base de datos con Python y MySQL.
- **Front-end:** Diseño de una página web interactiva que explica las reglas, tutoriales y documentación técnica del proyecto.
- **Base de Datos:** Persistencia de datos utilizando MySQL alojado en Azure.

**Características principales:**
- Simulación del juego para 2-6 jugadores.
- Perfiles de riesgo para bots controlados por la IA.
- Sistema de ranking persistente almacenado en la base de datos.
- Página web moderna y accesible.

---

## Miembros del Equipo
- **David Perera Gonzalez**
- **Cristina Vázquez Garrrote**
- **Aleix Linares Sousa**

---

## Requisitos Previos
Antes de comenzar, asegúrate de tener instalados los siguientes componentes:
1. **Python 3.8 o superior**.
2. **MySQL** (versión 5.7 o superior).
3. Acceso a una base de datos MySQL alojada (en este proyecto, usamos Azure).

---

## Instalación de MySQL Connector

### En Windows
1. Abre la terminal o PowerShell.
2. Ejecuta el siguiente comando para instalar el conector:
   ```bash
   pip install mysql-connector-python
   ```
3. Una vez instalado, verifica la instalación con:
   ```bash
   python -m pip show mysql-connector-python
   ```

### En Linux
1. Abre la terminal.
2. Instala el conector con:
   ```bash
   pip install mysql-connector-python
   ```
3. Verifica la instalación:
   ```bash
   python -m pip show mysql-connector-python
   ```

---

### Resolución de Errores de Privilegios
Si encuentras un error relacionado con permisos administrativos durante la instalación de paquetes en Linux o Windows, sigue estos pasos:

#### En Windows:
1. Abre PowerShell como administrador:
   - Haz clic derecho en el menú de inicio y selecciona **PowerShell (Administrador)**.
2. Ejecuta el comando de instalación nuevamente:
   ```bash
   pip install mysql-connector-python
   ```

#### En Linux:
1. Si ves un error de permisos, utiliza `sudo` para ejecutar el comando con privilegios de administrador:
   ```bash
   sudo pip install mysql-connector-python
   ```
2. Alternativamente, puedes instalar el conector solo para el usuario actual:
   ```bash
   pip install --user mysql-connector-python
   ```

---

## Página Web
Explora nuestra página web para aprender más sobre el proyecto:  
**[Visita la página aquí](https://aleixgls.github.io/ProyectoSieteYMedio_ACD/)**  

---

¡Gracias por explorar nuestro proyecto! Si tienes preguntas, no dudes en ponerte en contacto con cualquiera de los miembros del equipo. 🎉

