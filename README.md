# Moderación del Extremismo en Redes Sociales (ModEx) 📊💻

Este proyecto es parte del curso Análisis y Diseño de Algoritmos II, enfocado en aplicar diferentes estrategias algorítmicas para resolver el problema de moderar el extremismo en una red social.

## 📖 Acerca del Proyecto
En este proyecto, abordamos el desafío de reducir el extremismo en una red social ajustando las opiniones de los usuarios. La red está compuesta por usuarios, cada uno con una opinión cuantificada entre -100 (fuertemente desfavorable) y 100 (fuertemente favorable) y un puntaje de receptividad que indica qué tan fácil es influir en su opinión. El objetivo es minimizar el extremismo de la red respetando un límite en el esfuerzo requerido para moderar a los usuarios.

### El proyecto implementa tres estrategias algorítmicas clave:

- Fuerza Bruta: Genera todas las posibles estrategias de moderación y selecciona la óptima.
- Algoritmo Voraz: Prioriza la moderación de usuarios con opiniones más extremas y mayor receptividad.
- Programación Dinámica: Explora la solución óptima descomponiendo el problema en subproblemas manejables.
  
## 🔍 Definición del Problema
El extremismo de la red se determina por qué tan lejos están las opiniones de los usuarios de un punto de moderación (0). Nuestra tarea es reducir este extremismo usando un presupuesto limitado para moderar opiniones, representado como el esfuerzo máximo permitido. Aplicamos las estrategias para determinar qué usuarios deben ser moderados y cuánto esfuerzo gastar en cada uno para lograr la mayor reducción de extremismo.

## 💡 Características del Proyecto
Implementaciones Algorítmicas: Se implementan tres enfoques diferentes—fuerza bruta, voraz y programación dinámica—para resolver el problema.
Análisis de Complejidad: Un análisis detallado de la complejidad temporal y espacial de cada algoritmo.
Entrada/Salida: El sistema lee datos de la red desde un archivo de texto y produce la estrategia de moderación óptima, el esfuerzo asociado y la puntuación final de extremismo.

## 🚀 Tecnologías Utilizadas
- Python: Los algoritmos y simulaciones están implementados en Python.
- Estructuras de Datos: Se utilizaron listas y matrices para soluciones de programación dinámica.
- Diseño Algorítmico: Enfoque en métodos voraces, fuerza bruta y programación dinámica.
