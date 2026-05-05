Aquí tienes la transcripción de la práctica de laboratorio a formato Markdown, manteniendo la estructura original y las fórmulas matemáticas.

-----

# M3-bis2. OSCILACIONES ACOPLADAS

## OBJETIVOS

Se pretenden ilustrar algunos de los fenómenos que aparecen cuando un sólido rígido se somete a oscilaciones, revelando un acoplamiento mecánico en inercia. En particular, se estudiarán los modos normales de oscilación y las frecuencias características.

## FUNDAMENTO TEÓRICO

El movimiento oscilatorio de un sólido rígido sujeto a diferentes muelles puede ser sumamente complejo, pero siempre es posible describirlo en función de los llamados modos normales como una superposición de éstos. A cada modo normal sí le corresponde una frecuencia bien definida, que se conoce como frecuencia característica del modo. Además, es posible empezar el movimiento con condiciones iniciales tales que se excite exclusivamente un modo normal cualquiera. El número de modos normales de un sistema es igual a su número de grados de libertad.

Sea una barra homogénea de masa $m$ y longitud $L$ sujetada verticalmente por ambos extremos con dos muelles de constantes elásticas $k$. El sistema queda descrito con las coordenadas respecto del equilibrio del sistema $(z_1, z_2)$. Supongamos pequeñas oscilaciones.

Para este sistema, las expresiones de las energías cinética ($T$) y potencial ($U$, elástica más gravitatoria) son:

$$T = \frac{1}{2} m \dot{z}_{CM}^2 + \frac{1}{2} I \dot{\omega}^2 = \frac{1}{8} m (\dot{z}_1 + \dot{z}_2)^2 + \frac{1}{24} m (\dot{z}_1 - \dot{z}_2)^2 \quad (1)$$

$$U = \frac{1}{2} k z_1^2 + \frac{1}{2} k z_2^2 \quad (2)$$

Este sistema tiene dos grados de libertad, por tanto, tendrá dos modos normales. Puede demostrarse que las frecuencias de los modos normales vienen dadas por:

$$\omega_s^2 = \frac{2k}{m} \quad (3)$$

$$\omega_a^2 = \frac{6k}{m} \quad (4)$$

correspondientes a los modos llamados **simétrico** (lento) y **antisimétrico** (rápido), respectivamente, descritos por las coordenadas normales $z_{CM}$ y $z_{12} \equiv z_1 - z_2$.

## METODOLOGÍA

El montaje consta de un soporte con 2 muelles verticales idénticos que sujetan una barra horizontal (de masa irrelevante en esta práctica) y conectados a dos sensores PASCO (sensibilidad 0.03 N) que permiten medir la fuerza que ejerce cada muelle. Partiendo del equilibrio de la barra, ejecute el programa M3bis2 y pulse el botón de CERO de cada sensor.

Capture los datos de fuerza correspondientes al movimiento oscilatorio (\>10 ciclos) iniciado conforme las siguientes situaciones:

a) **Frecuencia natural $\omega_0$:** Mantenga un extremo de la barra fijo (con el soporte esfera-imán). Desplace ligeramente el otro extremo verticalmente y suéltelo. La barra se comporta como si fuera una masa puntual de masa $m/3$ sujeta a un muelle. Repítalo tres veces.

b) **Modo simétrico ($\omega_s$):** Desplace la barra verticalmente sin cambiar su orientación (tire de ambos extremos o del centro) y suéltela. Ambos extremos deben describir la misma función senoidal ($z_1 = z_2$). Determine la frecuencia con cada extremo y promedie. Repítalo tres veces.

c) **Modo antisimétrico ($\omega_a$):** Coloque la varilla auxiliar justo debajo del centro de masas. Desplace ambos extremos con desplazamientos opuestos e idénticos ($z_1 = -z_2$) y suelte. Los extremos deben describir senoides invertidas. Determine la frecuencia y promedie. Repítalo tres veces.

d) **Superposición de modos:** Desplace un extremo mientras el otro está en reposo y suéltelo. Determine las frecuencias propias $\omega_{min}$ y $\omega_{max}$. Repítalo tres veces.

## RESULTADOS

1.  Determine el periodo mediante conteo de ciclos, ajuste senoidal o **FFT**. Compare resultados.

2.  Complete la siguiente tabla:

| $\omega_o$ | $\omega_s$ | $\omega_a$ |
| :--- | :--- | :--- |
| | | |

*¿Debe existir alguna proporción numérica entre estas tres frecuencias? Razone según las ecs. (3) y (4).*

3.  En el movimiento complejo, ajuste a una serie senoidal o calcule la FFT. Complete la tabla:

| $\omega_{min}$ | $\omega_{max}$ |
| :--- | :--- |
| | |

*Compare $\omega_{max}$ con $\omega_a$ y $\omega_{min}$ con $\omega_s$. Razone lo observado.*

4.  Calcule las coordenadas normales $z_{CM}$ y $z_{12} \equiv z_1 - z_2$ a partir de las fuerzas. Represéntelas frente al tiempo y mida sus frecuencias:

| $\omega_{CM}$ | $\omega_{12}$ |
| :--- | :--- |
| | |

*Compare $\omega_{12}$ con $\omega_a$ y $\omega_{CM}$ con $\omega_s$. Razone lo observado.*

## BIBLIOGRAFÍA

1.  J.B. MARION. "Dinámica Clásica de las Partículas y los Sistemas". Reverté, Barcelona (1975).
2.  [http://www.sc.ehu.es/sbweb/fisica3/oscilaciones/varilla\_muelle/varilla\_muelle.html](https://www.google.com/search?q=http://www.sc.ehu.es/sbweb/fisica3/oscilaciones/varilla_muelle/varilla_muelle.html)

-----

### Explicación del Concepto: Modos Normales en Osciladores Acoplados

El sistema descrito consiste en una barra rígida unida a dos muelles. A diferencia de un muelle con una masa simple (que solo sube y baja), este sistema tiene dos "maneras" fundamentales de vibrar:

1.  **Modo Simétrico ($\omega_s$):** La barra sube y baja completamente horizontal. Los dos muelles trabajan "en equipo". Es el movimiento más lento.
2.  **Modo Antisimétrico ($\omega_a$):** El centro de la barra se queda quieto mientras los extremos suben y bajan de forma opuesta (como un columpio subibaja). Debido a la rotación de la barra, la inercia efectiva cambia, resultando en una frecuencia más alta.

Cuando mueves solo un lado de la barra, estás excitando **ambos modos a la vez**. Esto crea un fenómeno de interferencia (pulsaciones) donde la energía pasa de un muelle al otro.

Para ayudarte a visualizar cómo cambian estas frecuencias según la masa y la constante elástica, he preparado el siguiente simulador interactivo.

```json?chameleon
{"component":"LlmGeneratedComponent","props":{"height":"700px","prompt":"Generar un simulador de oscilaciones acopladas para una barra rígida con dos muelles. \n\nObjetivo: Visualizar los modos simétrico, antisimétrico y la superposición de ambos.\n\nControles:\n1. Constante del muelle (k): Deslizador para ajustar la rigidez.\n2. Masa de la barra (m): Deslizador para ajustar la inercia.\n3. Condiciones Iniciales (Botones): \n   - 'Simétrico' (z1 = 10, z2 = 10)\n   - 'Antisimétrico' (z1 = 10, z2 = -10)\n   - 'Un solo extremo' (z1 = 10, z2 = 0)\n4. Botón de Play/Pause y Reset.\n\nVisualización:\n- Un panel superior con la animación 2D de la barra (un rectángulo horizontal) colgada de dos resortes representados por líneas en zigzag. La barra debe oscilar verticalmente y rotar según los desplazamientos z1 y z2.\n- Un panel inferior con un gráfico de líneas en tiempo real que muestre z1 (un color) y z2 (otro color) frente al tiempo.\n- Mostrar los valores calculados teóricamente de omega_s y omega_a en pantalla basados en los valores de los deslizadores.\n\nComportamiento:\n- Usar las ecuaciones del movimiento derivadas de las energías dadas: la aceleración del CM y la aceleración angular deben calcularse a partir de las fuerzas de los muelles (-k*z1 y -k*z2).\n- Implementar la integración numérica (Euler o Runge-Kutta simple) para animar el movimiento suavemente.\n- El usuario debe ver cómo en el modo 'Un solo extremo' la amplitud de oscilación se transfiere de un muelle al otro.","id":"im_9d81bdd4c3ff74ac"}}
```