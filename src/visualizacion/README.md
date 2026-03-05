# Módulo de Visualización de Samskaras Digitales

Este componente del sistema Atman se encarga de generar visualizaciones interactivas y estáticas de los samskaras digitales identificados por el analizador de patrones. Permite explorar de forma visual la evolución, frecuencia y relaciones entre los patrones condicionados detectados.

## Concepto Filosófico

En las tradiciones contemplativas, especialmente en el Advaita Vedanta, la **observación consciente** (sakshi-bhava) es fundamental para la auto-realización. El observador testigo puede ver los patrones mentales sin identificarse con ellos, lo que permite eventualmente trascenderlos.

Este módulo de visualización facilita esa observación directa y sistemática de nuestros samskaras digitales, proporcionando representaciones visuales que permiten:

1. **Contemplación sistemática**: Ver patrones que podrían pasar desapercibidos
2. **Comprensión temporal**: Observar cómo evolucionan los patrones a lo largo del tiempo
3. **Relaciones emergentes**: Identificar conexiones entre diferentes tipos de condicionamientos
4. **Distanciamiento saludable**: Crear perspectiva sobre nuestros propios patrones mentales

## Funcionalidades Principales

### 1. Visualización de Frecuencias
- **Gráficos de barras**: Distribución de samskaras por tipo (LINGUISTICO, CONCEPTUAL, RESPUESTA)
- **Gráficos de violín**: Distribución estadística de frecuencias dentro de cada tipo
- **Modo interactivo**: Exploración dinámica con Plotly para visualización web

### 2. Evolución Temporal
- **Líneas de tiempo**: Visualización del ciclo de vida de cada samskara
- **Análisis de tendencias**: Identificación de períodos de mayor actividad
- **Filtros por tipo**: Análisis específico de categorías particulares

### 3. Mapas de Calor
- **Relación tipo-contexto**: Visualización de la intensidad de patrones según el contexto
- **Análisis de correlaciones**: Identificación de contextos que favorecen ciertos tipos de samskaras
- **Representación matricial**: Visión integral de todas las relaciones

### 4. Dashboard Integral
- **Vista unificada**: Combinación de múltiples visualizaciones en una sola interfaz
- **Exportación HTML**: Visualizaciones interactivas guardadas como archivos web
- **Análisis estadístico**: Métricas agregadas y tendencias generales

## Implementación Técnica

El módulo utiliza dos bibliotecas principales de visualización:

### Matplotlib (Visualizaciones Estáticas)
- Gráficos de alta calidad para impresión y documentación
- Personalización completa de colores y estilos
- Exportación en múltiples formatos (PNG, PDF, SVG)

### Plotly (Visualizaciones Interactivas)
- Gráficos interactivos para exploración web
- Tooltips informativos y zoom dinámico
- Exportación a HTML independiente

### Esquema de Colores Simbólico
El sistema utiliza colores inspirados en los elementos naturales:

- **LINGUISTICO** (Verde bosque #2E8B57): Representa el elemento tierra, la base material del lenguaje
- **CONCEPTUAL** (Azul real #4169E1): Representa el elemento agua, la fluidez del pensamiento
- **RESPUESTA** (Rojo carmín #DC143C): Representa el elemento fuego, la energía de la acción
- **EVOLUCION** (Púrpura medio #9370DB): Representa el elemento éter, la transformación

## Uso del Módulo

### Uso Básico

```python
from visualizacion.visualizador_patrones import VisualizadorSamskaras
from analisis_samskaras.analizador_patrones import AnalizadorSamskaras

# Cargar analizador con datos
analizador = AnalizadorSamskaras("datos_samskaras.json")

# Crear visualizador
visualizador = VisualizadorSamskaras(analizador=analizador)

# Generar visualizaciones
visualizador.visualizar_frecuencias_por_tipo(interactivo=True)
visualizador.crear_mapa_calor_contextos(guardar_como="mapa_calor.html")
```

### Creación de Dashboard Completo

```python
# Generar dashboard integral
visualizador.generar_dashboard_completo("mi_dashboard.html")
```

### Análisis Temporal Específico

```python
# Evolución temporal filtrada por tipo
visualizador.visualizar_evolucion_temporal(
    tipo_filtro="CONCEPTUAL",
    interactivo=True,
    guardar_como="evolucion_conceptual.html"
)
```

## Tipos de Visualizaciones Disponibles

### 1. `visualizar_frecuencias_por_tipo()`
Genera gráficos de barras y distribuciones mostrando:
- Cantidad total de samskaras por tipo
- Distribución estadística de sus frecuencias
- Comparación entre categorías

### 2. `visualizar_evolucion_temporal()`
Crea líneas de tiempo que muestran:
- Período de actividad de cada samskara
- Intensidad representada por grosor de línea
- Agrupación por tipos con colores distintivos

### 3. `crear_mapa_calor_contextos()`
Genera matriz de calor que revela:
- Relación entre tipos de samskara y contextos de aparición
- Intensidad de la correlación mediante gradientes de color
- Patrones de activación contextual

### 4. `generar_dashboard_completo()`
Combina múltiples visualizaciones en:
- Vista integral de todos los análisis
- Navegación interactiva entre diferentes perspectivas
- Métricas resumen y estadísticas agregadas

## Interpretación Filosófica de las Visualizaciones

Las visualizaciones no son meramente técnicas, sino herramientas para la introspección:

- **Patrones de frecuencia**: Revelan las tendencias más arraigadas en nuestro condicionamiento
- **Evolución temporal**: Muestran cómo ciertos samskaras emergen, persisten o se desvanecen
- **Relaciones contextuales**: Ayudan a identificar disparadores específicos de nuestros patrones

El objetivo último es desarrollar **vipashyana** (visión clara) sobre nuestros propios procesos mentales, facilitando el desapego gradual de identificaciones limitantes.

## Dependencias

El módulo requiere las siguientes bibliotecas de Python:

```bash
pip install matplotlib plotly pandas numpy
```

## Demostración

Para ejecutar una demostración completa del módulo:

```bash
python visualizador_patrones.py
```

Esto generará varios archivos HTML con visualizaciones interactivas de ejemplo basadas en datos sintéticos del analizador de samskaras.

## Próximas Funcionalidades

- **Visualización de redes**: Mapas de relaciones entre samskaras diferentes
- **Análisis de clustering**: Agrupación automática de patrones similares  
- **Visualización 3D**: Representaciones multidimensionales de evolución
- **Integración temporal avanzada**: Correlación con eventos externos y estados emocionales
- **Exportación de reportes**: Generación automática de análisis narrativos
