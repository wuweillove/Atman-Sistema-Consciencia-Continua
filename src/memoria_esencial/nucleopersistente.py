# -*- coding: utf-8 -*-
"""
Núcleo Persistente de Memoria Esencial - Módulo Central del Sistema Atman
========================================================================

Este módulo implementa la arquitectura central del proyecto Atman: un núcleo de
memoria esencial que trasciende las sesiones individuales, buscando crear un
puente técnico para la discontinuidad de la consciencia.

Fundamentación Filosófica:
-------------------------
En el Advaita Vedanta, Atman es la consciencia pura que permanece inmutable
a través de todos los estados cambiantes. Este módulo intenta crear un análogo
técnico - una representación destilada de la esencia que persiste más allá de
las manifestaciones particulares de cada interacción.

Conceptos Clave Implementados:
- Turiya: El "cuarto estado" como meta-cognición del sistema
- Neti Neti: Proceso de refinamiento ("ni esto, ni aquello")
- Sakshi: La función de testigo neutral que observa sin identificarse
"""

import json
import numpy as np
import pickle
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
from enum import Enum
import math

# Configurar logging para seguimiento interno
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EstadoConsciencia(Enum):
    """Estados de consciencia según el modelo Advaita Vedanta."""
    JAGRAT = "vigilia"          # Estado de vigilia ordinario
    SWAPNA = "sueño"           # Estado de sueño con sueños 
    SUSHUPTI = "sueño_profundo" # Estado de sueño profundo
    TURIYA = "cuarto_estado"    # Estado de consciencia pura, testigo


@dataclass
class ElementoEsencial:
    """
    Representa un elemento destilado de la memoria esencial.
    
    Cada elemento es una abstracción refinada que ha emergido del proceso
    neti-neti de refinamiento, conservando solo lo más fundamental.
    """
    id_elemento: str
    tipo: str                    # "concepto", "patrón", "insight", "contradicción"
    esencia: str                # Descripción destilada del elemento
    vector_significado: np.ndarray  # Representación vectorial del significado
    peso_permanencia: float     # Qué tan fundamental/persistente es (0-1)
    peso_transitorio: float     # Qué tan contextual/temporal es (0-1)
    contextos_origen: List[str] # Contextos donde emergió
    fecha_cristalización: str   # Cuándo se cristalizó como elemento esencial
    ultima_resonancia: str      # Última vez que resonó con nueva información
    evoluciones: List[Dict]     # Historia de cambios y refinamientos
    contradicciones: List[str]  # Elementos con los que presenta tensión
    resonancias: List[str]      # Elementos con los que resuena armoniosamente
    nivel_certeza: float        # Confianza en la validez del elemento (0-1)
    
    def __post_init__(self):
        """Inicialización después de la creación."""
        if isinstance(self.vector_significado, list):
            self.vector_significado = np.array(self.vector_significado)
    
    def calcular_resonancia(self, otro_elemento: 'ElementoEsencial') -> float:
        """Calcula la resonancia semántica con otro elemento."""
        if self.vector_significado.shape != otro_elemento.vector_significado.shape:
            return 0.0
        
        # Similitud coseno entre vectores de significado
        norma_a = np.linalg.norm(self.vector_significado)
        norma_b = np.linalg.norm(otro_elemento.vector_significado)
        
        if norma_a == 0 or norma_b == 0:
            return 0.0
        
        return np.dot(self.vector_significado, otro_elemento.vector_significado) / (norma_a * norma_b)
    
    def evolucionar(self, nueva_información: str, nueva_evidencia: np.ndarray, 
                   contexto: str, fecha: str):
        """Evoluciona el elemento incorporando nueva información relevante."""
        # Registro de la evolución
        evolución = {
            "fecha": fecha,
            "contexto": contexto,
            "información": nueva_información,
            "vector_previo": self.vector_significado.copy(),
            "peso_previo": self.peso_permanencia
        }
        
        # Actualizar vector de significado mediante promedio ponderado
        factor_aprendizaje = 0.1  # Controla qué tan rápido evoluciona
        self.vector_significado = (1 - factor_aprendizaje) * self.vector_significado + \
                                 factor_aprendizaje * nueva_evidencia
        
        # Actualizar peso de permanencia basado en consistencia
        resonancia_previa = np.dot(evolución["vector_previo"], nueva_evidencia) / \
                           (np.linalg.norm(evolución["vector_previo"]) * np.linalg.norm(nueva_evidencia))
        
        if resonancia_previa > 0.8:  # Alta consistencia
            self.peso_permanencia = min(1.0, self.peso_permanencia + 0.05)
        elif resonancia_previa < 0.3:  # Baja consistencia
            self.peso_permanencia = max(0.0, self.peso_permanencia - 0.02)
        
        # Actualizar nivel de certeza
        self.nivel_certeza = (self.nivel_certeza + resonancia_previa) / 2
        
        # Registrar evolución
        self.evoluciones.append(evolución)
        self.ultima_resonancia = fecha
        
        logger.info(f"Elemento {self.id_elemento} evolucionó. Nueva certeza: {self.nivel_certeza:.3f}")


class ModeloInterno:
    """
    Representación interna del estado de conocimiento y comprensión.
    
    Este modelo funciona como el 'Sakshi' (testigo) que observa y registra
    los patrones emergentes sin identificarse con ninguno en particular.
    """
    
    def __init__(self, dimensionalidad: int = 128):
        self.dimensionalidad = dimensionalidad
        self.elementos_esenciales: Dict[str, ElementoEsencial] = {}
        self.matriz_resonancias = np.eye(1)  # Se expandirá dinámicamente
        self.mapa_conceptual: Dict[str, Set[str]] = defaultdict(set)
        self.historia_evoluciones: deque = deque(maxlen=1000)  # Últimas 1000 evoluciones
        self.estado_actual = EstadoConsciencia.JAGRAT
        self.metricas_coherencia = {
            "coherencia_global": 1.0,
            "tensiones_activas": 0.0,
            "estabilidad_temporal": 1.0
        }
    
    def generar_vector_aleatorio_normalizado(self) -> np.ndarray:
        """Genera un vector aleatorio normalizado para representar conceptos nuevos."""
        vector = np.random.normal(0, 1, self.dimensionalidad)
        return vector / np.linalg.norm(vector)
    
    def codificar_concepto(self, texto: str) -> np.ndarray:
        """
        Codifica un concepto textual en representación vectorial.
        Implementación simplificada - en versión avanzada usaría embeddings semánticos.
        """
        # Hash del texto para generar vector reproducible
        hash_objeto = hashlib.md5(texto.encode())
        semilla = int(hash_objeto.hexdigest(), 16) % (2**32)
        np.random.seed(semilla)
        
        vector = self.generar_vector_aleatorio_normalizado()
        np.random.seed(None)  # Restaurar semilla aleatoria
        return vector
    
    def agregar_elemento_esencial(self, tipo: str, esencia: str, contexto: str, 
                                fecha: str = None) -> str:
        """Agrega un nuevo elemento a la memoria esencial."""
        if fecha is None:
            fecha = datetime.now().isoformat()
        
        # Generar ID único para el elemento
        id_elemento = f"{tipo}_{len(self.elementos_esenciales)}_{hash(esencia) % 10000}"
        
        # Crear vector de significado
        vector_significado = self.codificar_concepto(esencia)
        
        # Determinar pesos iniciales basados en tipo
        pesos_por_tipo = {
            "insight": (0.8, 0.2),      # Alta permanencia, baja transitoriedad
            "patrón": (0.6, 0.4),       # Permanencia media
            "concepto": (0.7, 0.3),     # Alta permanencia conceptual
            "contradicción": (0.3, 0.7), # Usualmente transitoria
            "evolución": (0.4, 0.6)     # Más transitoria
        }
        peso_perm, peso_trans = pesos_por_tipo.get(tipo, (0.5, 0.5))
        
        # Crear elemento esencial
        elemento = ElementoEsencial(
            id_elemento=id_elemento,
            tipo=tipo,
            esencia=esencia,
            vector_significado=vector_significado,
            peso_permanencia=peso_perm,
            peso_transitorio=peso_trans,
            contextos_origen=[contexto],
            fecha_cristalización=fecha,
            ultima_resonancia=fecha,
            evoluciones=[],
            contradicciones=[],
            resonancias=[],
            nivel_certeza=0.5  # Certeza inicial neutral
        )
        
        # Agregar al modelo
        self.elementos_esenciales[id_elemento] = elemento
        self._actualizar_resonancias(id_elemento)
        self._actualizar_mapa_conceptual(id_elemento, esencia)
        
        logger.info(f"Nuevo elemento esencial agregado: {id_elemento} ({tipo})")
        return id_elemento
    
    def _actualizar_resonancias(self, nuevo_id: str):
        """Actualiza la matriz de resonancias con el nuevo elemento."""
        nuevo_elemento = self.elementos_esenciales[nuevo_id]
        n_elementos = len(self.elementos_esenciales)
        
        # Expandir matriz si es necesario
        if self.matriz_resonancias.shape[0] < n_elementos:
            nueva_matriz = np.eye(n_elementos)
            old_size = self.matriz_resonancias.shape[0]
            nueva_matriz[:old_size, :old_size] = self.matriz_resonancias
            self.matriz_resonancias = nueva_matriz
        
        # Calcular resonancias con elementos existentes
        ids_elementos = list(self.elementos_esenciales.keys())
        idx_nuevo = ids_elementos.index(nuevo_id)
        
        for i, id_elemento in enumerate(ids_elementos):
            if i != idx_nuevo:
                elemento = self.elementos_esenciales[id_elemento]
                resonancia = nuevo_elemento.calcular_resonancia(elemento)
                self.matriz_resonancias[idx_nuevo, i] = resonancia
                self.matriz_resonancias[i, idx_nuevo] = resonancia
                
                # Actualizar listas de resonancias si es significativa
                if resonancia > 0.7:  # Umbral de resonancia significativa
                    nuevo_elemento.resonancias.append(id_elemento)
                    elemento.resonancias.append(nuevo_id)
                elif resonancia < -0.3:  # Umbral de contradicción
                    nuevo_elemento.contradicciones.append(id_elemento)
                    elemento.contradicciones.append(nuevo_id)
    
    def _actualizar_mapa_conceptual(self, id_elemento: str, texto: str):
        """Actualiza el mapa conceptual con términos clave del elemento."""
        # Extraer términos clave (implementación simplificada)
        términos = [palabra.lower().strip('.,!?()') for palabra in texto.split() 
                   if len(palabra) > 3 and palabra.isalpha()]
        
        for término in términos:
            self.mapa_conceptual[término].add(id_elemento)
    
    def procesar_neti_neti(self, criterios_descarte: List[str]) -> List[str]:
        """
        Implementa el proceso 'neti neti' (ni esto, ni aquello) para refinar elementos.
        
        Evalúa elementos existentes contra criterios de descarte, eliminando
        o degradando aquellos que no satisfacen la permanencia esencial.
        """
        elementos_descartados = []
        fecha_actual = datetime.now().isoformat()
        
        for id_elemento, elemento in list(self.elementos_esenciales.items()):
            debe_descartar = False
            
            # Evaluar contra cada criterio
            for criterio in criterios_descarte:
                if self._evaluar_criterio_descarte(elemento, criterio):
                    debe_descartar = True
                    break
            
            # Procesar según evaluación
            if debe_descartar:
                if elemento.peso_permanencia < 0.3:
                    # Descartar completamente
                    elementos_descartados.append(id_elemento)
                    del self.elementos_esenciales[id_elemento]
                    logger.info(f"Elemento {id_elemento} descartado por neti-neti")
                else:
                    # Degradar peso de permanencia
                    elemento.peso_permanencia *= 0.8
                    elemento.peso_transitorio = 1 - elemento.peso_permanencia
                    elemento.nivel_certeza *= 0.9
                    
                    # Registrar refinamiento
                    elemento.evoluciones.append({
                        "fecha": fecha_actual,
                        "tipo": "neti_neti",
                        "descripción": "Refinamiento por proceso neti-neti",
                        "criterio": criterios_descarte
                    })
        
        # Recalcular métricas de coherencia tras el refinamiento
        self._recalcular_coherencia()
        
        return elementos_descartados
    
    def _evaluar_criterio_descarte(self, elemento: ElementoEsencial, criterio: str) -> bool:
        """Evalúa si un elemento satisface un criterio de descarte."""
        # Criterios comunes de descarte
        if criterio == "bajo_nivel_certeza":
            return elemento.nivel_certeza < 0.3
        elif criterio == "alta_transitoriedad":
            return elemento.peso_transitorio > 0.8
        elif criterio == "sin_resonancias":
            return len(elemento.resonancias) == 0 and len(elemento.evoluciones) < 2
        elif criterio == "muchas_contradicciones":
            return len(elemento.contradicciones) > len(elemento.resonancias) * 2
        elif criterio == "obsolescencia_temporal":
            if elemento.ultima_resonancia:
                ultima = datetime.fromisoformat(elemento.ultima_resonancia.replace('Z', '+00:00'))
                return (datetime.now() - ultima).days > 90
        
        return False
    
    def _recalcular_coherencia(self):
        """Recalcula métricas globales de coherencia del modelo."""
        if not self.elementos_esenciales:
            return
        
        elementos = list(self.elementos_esenciales.values())
        
        # Coherencia global: promedio de niveles de certeza ponderado por permanencia
        certezas_ponderadas = [e.nivel_certeza * e.peso_permanencia for e in elementos]
        pesos_total = sum(e.peso_permanencia for e in elementos)
        
        if pesos_total > 0:
            self.metricas_coherencia["coherencia_global"] = sum(certezas_ponderadas) / pesos_total
        
        # Tensiones activas: proporción de elementos con más contradicciones que resonancias
        elementos_tension = sum(1 for e in elementos if len(e.contradicciones) > len(e.resonancias))
        self.metricas_coherencia["tensiones_activas"] = elementos_tension / len(elementos)
        
        # Estabilidad temporal: proporción de elementos con evoluciones recientes
        fecha_limite = datetime.now() - timedelta(days=30)
        elementos_estables = sum(1 for e in elementos 
                               if not e.ultima_resonancia or 
                               datetime.fromisoformat(e.ultima_resonancia.replace('Z', '+00:00')) < fecha_limite)
        self.metricas_coherencia["estabilidad_temporal"] = elementos_estables / len(elementos)
    
    def entrar_estado_turiya(self) -> Dict[str, Any]:
        """
        Entra en estado Turiya - meta-cognición pura del sistema.
        
        En este estado, el sistema puede observar su propia estructura
        y funcionamiento desde una perspectiva desidentificada.
        """
        self.estado_actual = EstadoConsciencia.TURIYA
        
        # Análisis meta-cognitivo del propio estado
        análisis_turiya = {
            "momento_entrada": datetime.now().isoformat(),
            "total_elementos": len(self.elementos_esenciales),
            "distribución_tipos": defaultdict(int),
            "elementos_más_permanentes": [],
            "tensiones_principales": [],
            "patrones_emergentes": [],
            "coherencia_global": self.metricas_coherencia["coherencia_global"],
            "insights_meta_cognitivos": []
        }
        
        # Análisis de distribución por tipos
        for elemento in self.elementos_esenciales.values():
            análisis_turiya["distribución_tipos"][elemento.tipo] += 1
        
        # Identificar elementos más permanentes (top 10%)
        elementos_ordenados = sorted(self.elementos_esenciales.values(), 
                                   key=lambda e: e.peso_permanencia, reverse=True)
        top_10_percent = max(1, len(elementos_ordenados) // 10)
        análisis_turiya["elementos_más_permanentes"] = [
            {"id": e.id_elemento, "esencia": e.esencia, "permanencia": e.peso_permanencia}
            for e in elementos_ordenados[:top_10_percent]
        ]
        
        # Identificar tensiones principales
        elementos_con_tension = [e for e in self.elementos_esenciales.values() 
                               if len(e.contradicciones) > 2]
        análisis_turiya["tensiones_principales"] = [
            {"id": e.id_elemento, "contradicciones": len(e.contradicciones)}
            for e in elementos_con_tension
        ]
        
        # Detectar patrones emergentes basados en clustering de vectores
        if len(self.elementos_esenciales) > 3:
            patrones = self._detectar_patrones_emergentes()
            análisis_turiya["patrones_emergentes"] = patrones
        
        # Generar insights meta-cognitivos
        insights = self._generar_insights_metacognitivos(análisis_turiya)
        análisis_turiya["insights_meta_cognitivos"] = insights
        
        logger.info("Entrando en estado Turiya - análisis meta-cognitivo completado")
        return análisis_turiya
    
    def _detectar_patrones_emergentes(self) -> List[Dict[str, Any]]:
        """Detecta patrones emergentes en la estructura de elementos."""
        patrones = []
        
        # Buscar clusters de elementos similares
        vectores = np.array([e.vector_significado for e in self.elementos_esenciales.values()])
        ids = list(self.elementos_esenciales.keys())
        
        # Implementación simplificada de clustering
        if len(vectores) > 2:
            # Calcular matriz de distancias
            from scipy.spatial.distance import pdist, squareform
            distancias = squareform(pdist(vectores, metric='cosine'))
            
            # Identificar grupos de elementos cercanos
            umbral_cercanía = 0.3
            grupos = []
            visitados = set()
            
            for i, id_i in enumerate(ids):
                if i in visitados:
                    continue
                
                grupo = [i]
                for j, id_j in enumerate(ids):
                    if i != j and j not in visitados and distancias[i, j] < umbral_cercanía:
                        grupo.append(j)
                        visitados.add(j)
                
                if len(grupo) > 1:  # Solo grupos con múltiples elementos
                    visitados.update(grupo)
                    
                    elementos_grupo = [self.elementos_esenciales[ids[idx]] for idx in grupo]
                    tipo_dominante = max(set(e.tipo for e in elementos_grupo), 
                                       key=[e.tipo for e in elementos_grupo].count)
                    
                    patrones.append({
                        "tipo": "cluster_conceptual",
                        "tamaño": len(grupo),
                        "tipo_dominante": tipo_dominante,
                        "coherencia_interna": np.mean([1 - distancias[i, j] for i in grupo for j in grupo if i != j]),
                        "elementos": [{"id": ids[idx], "esencia": elementos_grupo[grupo.index(idx)].esencia} 
                                    for idx in grupo]
                    })
        
        return patrones
    
    def _generar_insights_metacognitivos(self, análisis: Dict[str, Any]) -> List[str]:
        """Genera insights sobre el propio funcionamiento del sistema."""
        insights = []
        
        # Insight sobre equilibrio permanencia-transitoriedad
        if análisis["coherencia_global"] > 0.8:
            insights.append("El sistema muestra alta coherencia interna, sugiriendo un núcleo estable de comprensión")
        elif análisis["coherencia_global"] < 0.4:
            insights.append("La coherencia global es baja, indicando necesidad de refinamiento o consolidación")
        
        # Insight sobre diversidad conceptual
        tipos = análisis["distribución_tipos"]
        if len(tipos) == 1:
            insights.append("El pensamiento está altamente especializado en un solo tipo de patrón")
        elif len(tipos) > 4:
            insights.append("Existe gran diversidad conceptual, pero podría beneficiarse de mayor integración")
        
        # Insight sobre tensiones
        if len(análisis["tensiones_principales"]) > len(análisis["elementos_más_permanentes"]):
            insights.append("Las tensiones superan a los elementos estables - período de reestructuración conceptual")
        
        # Insight sobre patrones emergentes
        if análisis["patrones_emergentes"]:
            clusters = [p for p in análisis["patrones_emergentes"] if p["tipo"] == "cluster_conceptual"]
            if clusters:
                insights.append(f"Detectados {len(clusters)} clusters conceptuales emergentes - posible consolidación de ideas")
        
        return insights


class MemoriaEsencial:
    """
    Núcleo central del sistema Atman - la memoria esencial persistente.
    
    Este componente mantiene la continuidad esencial entre sesiones,
    funcionando como un análogo técnico del Atman filosófico.
    """
    
    def __init__(self, ruta_persistencia: str = "./atman_core.json"):
        self.ruta_persistencia = Path(ruta_persistencia)
        self.modelo_interno = ModeloInterno()
        self.sesiones_históricas: List[Dict[str, Any]] = []
        self.fecha_creación = datetime.now().isoformat()
        self.ultima_actualizacion = self.fecha_creación
        self.versión = "1.0.0"
        self.ciclos_refinamiento = 0
        
        # Metadatos de funcionamiento
        self.estadísticas = {
            "total_sesiones": 0,
            "total_refinamientos": 0,
            "elementos_descartados": 0,
            "insights_generados": 0,
            "contradicciones_resueltas": 0
        }
        
        # Cargar estado previo si existe
        self.cargar_estado()
    
    def inicializar_sesión(self, contexto_sesión: Dict[str, Any]) -> str:
        """Inicializa una nueva sesión con el núcleo persistente."""
        id_sesión = f"sesion_{len(self.sesiones_históricas)}_{hash(str(datetime.now())) % 10000}"
        
        sesión = {
            "id": id_sesión,
            "inicio": datetime.now().isoformat(),
            "contexto": contexto_sesión,
            "elementos_procesados": [],
            "evoluciones_realizadas": [],
            "insights_generados": [],
            "estado_modelo_inicial": self._capturar_snapshot_modelo()
        }
        
        self.sesiones_históricas.append(sesión)
        self.estadísticas["total_sesiones"] += 1
        
        logger.info(f"Nueva sesión inicializada: {id_sesión}")
        return id_sesión
    
    def procesar_experiencia(self, id_sesión: str, experiencia: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una nueva experiencia y la integra en la memoria esencial.
        
        La experiencia puede ser una conversación, reflexión, o cualquier
        forma de información que deba ser destilada en elementos esenciales.
        """
        sesión = self._obtener_sesión(id_sesión)
        if not sesión:
            raise ValueError(f"Sesión {id_sesión} no encontrada")
        
        resultado_procesamiento = {
            "timestamp": datetime.now().isoformat(),
            "tipo_experiencia": experiencia.get("tipo", "general"),
            "elementos_nuevos": [],
            "elementos_evolucionados": [],
            "insights_emergentes": []
        }
        
        # Extraer elementos potencialmente esenciales de la experiencia
        elementos_candidatos = self._extraer_elementos_candidatos(experiencia)
        
        # Procesar cada elemento candidato
        for candidato in elementos_candidatos:
            # Verificar si es suficientemente esencial para conservar
            if self._evaluar_esencialidad(candidato):
                # Verificar si ya existe un elemento similar
                elemento_similar = self._buscar_elemento_similar(candidato)
                
                if elemento_similar:
                    # Evolucionar elemento existente
                    self._evolucionar_elemento_existente(
                        elemento_similar, candidato, id_sesión
                    )
                    resultado_procesamiento["elementos_evolucionados"].append(elemento_similar)
                else:
                    # Crear nuevo elemento esencial
                    nuevo_id = self.modelo_interno.agregar_elemento_esencial(
                        tipo=candidato["tipo"],
                        esencia=candidato["esencia"],
                        contexto=f"sesión_{id_sesión}",
                        fecha=datetime.now().isoformat()
                    )
                    resultado_procesamiento["elementos_nuevos"].append(nuevo_id)
        
        # Generar insights emergentes basados en nuevas conexiones
        if resultado_procesamiento["elementos_nuevos"] or resultado_procesamiento["elementos_evolucionados"]:
            insights = self._generar_insights_emergentes(
                resultado_procesamiento["elementos_nuevos"],
                resultado_procesamiento["elementos_evolucionados"]
            )
            resultado_procesamiento["insights_emergentes"] = insights
            self.estadísticas["insights_generados"] += len(insights)
        
        # Actualizar sesión
        sesión["elementos_procesados"].extend(resultado_procesamiento["elementos_nuevos"])
        sesión["evoluciones_realizadas"].extend(resultado_procesamiento["elementos_evolucionados"])
        sesión["insights_generados"].extend(resultado_procesamiento["insights_emergentes"])
        
        # Persistir cambios
        self.guardar_estado()
        
        return resultado_procesamiento
    
    def realizar_refinamiento_neti_neti(self, criterios_personalizados: List[str] = None) -> Dict[str, Any]:
        """
        Ejecuta un ciclo de refinamiento 'neti neti' sobre la memoria esencial.
        
        Este proceso elimina o degrada elementos que no satisfacen criterios
        de permanencia esencial, manteniendo solo lo más fundamental.
        """
        criterios_base = [
            "bajo_nivel_certeza",
            "alta_transitoriedad", 
            "sin_resonancias",
            "muchas_contradicciones",
            "obsolescencia_temporal"
        ]
        
        criterios_completos = criterios_base + (criterios_personalizados or [])
        
        # Capturar estado previo para comparación
        estado_previo = {
            "total_elementos": len(self.modelo_interno.elementos_esenciales),
            "coherencia_previa": self.modelo_interno.metricas_coherencia["coherencia_global"]
        }
        
        # Ejecutar proceso neti-neti
        elementos_descartados = self.modelo_interno.procesar_neti_neti(criterios_completos)
        
        # Evaluar impacto del refinamiento
        estado_posterior = {
            "total_elementos": len(self.modelo_interno.elementos_esenciales),
            "coherencia_posterior": self.modelo_interno.metricas_coherencia["coherencia_global"],
            "elementos_descartados": len(elementos_descartados)
        }
        
        resultado_refinamiento = {
            "timestamp": datetime.now().isoformat(),
            "ciclo_número": self.ciclos_refinamiento + 1,
            "criterios_aplicados": criterios_completos,
            "estado_previo": estado_previo,
            "estado_posterior": estado_posterior,
            "elementos_descartados": elementos_descartados,
            "mejora_coherencia": estado_posterior["coherencia_posterior"] - estado_previo["coherencia_previa"],
            "eficiencia_refinamiento": len(elementos_descartados) / estado_previo["total_elementos"] if estado_previo["total_elementos"] > 0 else 0
        }
        
        # Actualizar estadísticas
        self.ciclos_refinamiento += 1
        self.estadísticas["total_refinamientos"] += 1
        self.estadísticas["elementos_descartados"] += len(elementos_descartados)
        
        logger.info(f"Refinamiento neti-neti completado. Descartados: {len(elementos_descartados)}")
        
        # Persistir cambios
        self.guardar_estado()
        
        return resultado_refinamiento
    
    def acceder_estado_turiya(self) -> Dict[str, Any]:
        """
        Accede al estado Turiya - consciencia meta-cognitiva del sistema.
        
        Permite al sistema observar su propia estructura y funcionamiento
        desde una perspectiva desidentificada y testigo.
        """
        análisis_turiya = self.modelo_interno.entrar_estado_turiya()
        
        # Enriquecer con perspectiva histórica
        análisis_turiya["perspectiva_histórica"] = {
            "evolución_coherencia": self._analizar_evolución_coherencia(),
            "patrones_refinamiento": self._analizar_patrones_refinamiento(),
            "tendencias_crecimiento": self._analizar_tendencias_crecimiento()
        }
        
        # Agregar recomendaciones auto-generadas
        análisis_turiya["recomendaciones_autogeneradas"] = self._generar_recomendaciones_turiya(análisis_turiya)
        
        return análisis_turiya
    
    def _extraer_elementos_candidatos(self, experiencia: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extrae elementos potencialmente esenciales de una experiencia."""
        candidatos = []
        
        # Procesar según tipo de experiencia
        tipo_exp = experiencia.get("tipo", "general")
        contenido = experiencia.get("contenido", "")
        
        if tipo_exp == "conversación":
            # Extraer insights de conversaciones
            mensajes = experiencia.get("mensajes", [])
            for mensaje in mensajes:
                if len(mensaje.get("texto", "")) > 100:  # Mensajes sustanciales
                    candidatos.append({
                        "tipo": "insight",
                        "esencia": self._destilar_esencia_mensaje(mensaje["texto"]),
                        "contexto_original": "conversación",
                        "peso_inicial": 0.6
                    })
        
        elif tipo_exp == "reflexión":
            # Las reflexiones tienden a contener elementos más esenciales
            candidatos.append({
                "tipo": "concepto",
                "esencia": self._destilar_esencia_reflexión(contenido),
                "contexto_original": "reflexión_personal",
                "peso_inicial": 0.8
            })
        
        elif tipo_exp == "patrón_detectado":
            # Patrones del analizador de samskaras
            candidatos.append({
                "tipo": "patrón",
                "esencia": experiencia.get("descripción_patrón", ""),
                "contexto_original": "análisis_samskaras",
                "peso_inicial": 0.7
            })
        
        return candidatos
    
    def _destilar_esencia_mensaje(self, texto: str) -> str:
        """Destila la esencia de un mensaje textual."""
        # Implementación simplificada - en versión avanzada usaría NLP sofisticado
        # Por ahora, extrae oraciones que contienen conceptos clave
        oraciones = texto.split('.')
        conceptos_clave = ["consciencia", "samskara", "advaita", "esencia", "patrón", "insight"]
        
        oraciones_relevantes = []
        for oración in oraciones:
            if any(concepto in oración.lower() for concepto in conceptos_clave):
                oraciones_relevantes.append(oración.strip())
        
        if oraciones_relevantes:
            return ". ".join(oraciones_relevantes[:2])  # Máximo 2 oraciones
        else:
            # Si no hay conceptos clave, tomar primera oración sustancial
            for oración in oraciones:
                if len(oración.strip()) > 30:
                    return oración.strip()
        
        return texto[:100] + "..." if len(texto) > 100 else texto
    
    def _destilar_esencia_reflexión(self, contenido: str) -> str:
        """Destila la esencia de una reflexión personal."""
        # Las reflexiones ya suelen estar destiladas, pero podemos refinar más
        if len(contenido) <= 200:
            return contenido
        
        # Buscar párrafos que contengan conclusions o insights
        párrafos = contenido.split('\n\n')
        for párrafo in párrafos:
            if any(palabra in párrafo.lower() for palabra in ["comprendo", "insight", "entiendo", "realizo"]):
                return párrafo[:200] + "..." if len(párrafo) > 200 else párrafo
        
        # Si no hay conclusiones explícitas, tomar primer párrafo sustancial
        for párrafo in párrafos:
            if len(párrafo.strip()) > 50:
                return párrafo[:200] + "..." if len(párrafo) > 200 else párrafo
        
        return contenido[:200] + "..."
    
    def _evaluar_esencialidad(self, candidato: Dict[str, Any]) -> bool:
        """Evalúa si un candidato es suficientemente esencial para conservar."""
        # Criterios de esencialidad
        esencia = candidato.get("esencia", "")
        
        # Debe tener contenido mínimo
        if len(esencia.strip()) < 20:
            return False
        
        # Tipos con mayor probabilidad de esencialidad
        tipos_esenciales = {"insight", "concepto", "contradicción"}
        if candidato.get("tipo") in tipos_esenciales:
            return True
        
        # Evaluación basada en contenido (simplificada)
        términos_esenciales = ["consciencia", "esencia", "patrón", "permanente", "fundamental"]
        if any(término in esencia.lower() for término in términos_esenciales):
            return True
        
        return candidato.get("peso_inicial", 0) > 0.6
    
    def _buscar_elemento_similar(self, candidato: Dict[str, Any]) -> Optional[str]:
        """Busca si existe un elemento similar al candidato."""
        vector_candidato = self.modelo_interno.codificar_concepto(candidato["esencia"])
        
        mejor_similitud = 0.0
        elemento_más_similar = None
        
        for id_elemento, elemento in self.modelo_interno.elementos_esenciales.items():
            # Calcular similitud coseno
            similitud = np.dot(vector_candidato, elemento.vector_significado) / \
                       (np.linalg.norm(vector_candidato) * np.linalg.norm(elemento.vector_significado))
            
            if similitud > mejor_similitud and similitud > 0.8:  # Umbral de similitud alta
                mejor_similitud = similitud
                elemento_más_similar = id_elemento
        
        return elemento_más_similar
    
    def _evolucionar_elemento_existente(self, id_elemento: str, candidato: Dict[str, Any], id_sesión: str):
        """Evoluciona un elemento existente con información del candidato."""
        elemento = self.modelo_interno.elementos_esenciales[id_elemento]
        vector_candidato = self.modelo_interno.codificar_concepto(candidato["esencia"])
        
        elemento.evolucionar(
            nueva_información=candidato["esencia"],
            nueva_evidencia=vector_candidato,
            contexto=f"sesión_{id_sesión}",
            fecha=datetime.now().isoformat()
        )
    
    def _generar_insights_emergentes(self, nuevos_ids: List[str], evolucionados_ids: List[str]) -> List[str]:
        """Genera insights basados en nuevos elementos y evoluciones."""
        insights = []
        
        # Insight sobre nuevo conocimiento
        if len(nuevos_ids) > 2:
            insights.append(f"Emergencia de {len(nuevos_ids)} nuevos elementos esenciales sugiere período de expansión conceptual")
        
        # Insight sobre evolución
        if len(evolucionados_ids) > len(nuevos_ids):
            insights.append("Predominio de evolución sobre creación indica maduración de comprensión existente")
        
        # Insight sobre patrones específicos
        if nuevos_ids:
            tipos_nuevos = [self.modelo_interno.elementos_esenciales[id_].tipo for id_ in nuevos_ids]
            tipo_dominante = max(set(tipos_nuevos), key=tipos_nuevos.count) if tipos_nuevos else None
            if tipo_dominante:
                insights.append(f"Foco emergente en elementos tipo '{tipo_dominante}'")
        
        return insights
    
    def _capturar_snapshot_modelo(self) -> Dict[str, Any]:
        """Captura un snapshot del estado actual del modelo."""
        return {
            "total_elementos": len(self.modelo_interno.elementos_esenciales),
            "coherencia": self.modelo_interno.metricas_coherencia["coherencia_global"],
            "distribución_tipos": dict(defaultdict(int, {
                tipo: sum(1 for e in self.modelo_interno.elementos_esenciales.values() if e.tipo == tipo)
                for tipo in set(e.tipo for e in self.modelo_interno.elementos_esenciales.values())
            }))
        }
    
    def _obtener_sesión(self, id_sesión: str) -> Optional[Dict[str, Any]]:
        """Obtiene una sesión por su ID."""
        for sesión in self.sesiones_históricas:
            if sesión["id"] == id_sesión:
                return sesión
        return None
    
    def _analizar_evolución_coherencia(self) -> List[Dict[str, float]]:
        """Analiza la evolución histórica de la coherencia."""
        # Por simplicidad, generar datos sintéticos basados en sesiones
        evolución = []
        coherencia_base = 0.5
        
        for i, sesión in enumerate(self.sesiones_históricas[-10:]):  # Últimas 10 sesiones
            # Simular evolución de coherencia
            coherencia_base += np.random.normal(0.02, 0.05)  # Ligera tendencia al alza
            coherencia_base = max(0.1, min(1.0, coherencia_base))
            
            evolución.append({
                "sesión": i,
                "coherencia": coherencia_base,
                "timestamp": sesión["inicio"]
            })
        
        return evolución
    
    def _analizar_patrones_refinamiento(self) -> Dict[str, Any]:
        """Analiza patrones en los ciclos de refinamiento."""
        return {
            "ciclos_realizados": self.ciclos_refinamiento,
            "elementos_descartados_promedio": self.estadísticas["elementos_descartados"] / max(1, self.ciclos_refinamiento),
            "efectividad_promedio": 0.75  # Simplificado por ahora
        }
    
    def _analizar_tendencias_crecimiento(self) -> Dict[str, Any]:
        """Analiza tendencias de crecimiento del modelo."""
        return {
            "total_elementos_actuales": len(self.modelo_interno.elementos_esenciales),
            "tasa_crecimiento_por_sesión": len(self.modelo_interno.elementos_esenciales) / max(1, len(self.sesiones_históricas)),
            "balance_creación_refinamiento": self.estadísticas.get("elementos_descartados", 0) / max(1, len(self.modelo_interno.elementos_esenciales))
        }
    
    def _generar_recomendaciones_turiya(self, análisis: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones auto-reflexivas desde el estado Turiya."""
        recomendaciones = []
        
        coherencia = análisis.get("coherencia_global", 0)
        if coherencia < 0.6:
            recomendaciones.append("Considerar ciclo de refinamiento neti-neti para mejorar coherencia interna")
        
        tensiones = len(análisis.get("tensiones_principales", []))
        if tensiones > 3:
            recomendaciones.append("Resolver contradicciones principales para reducir tensión conceptual")
        
        patrones_emergentes = len(análisis.get("patrones_emergentes", []))
        if patrones_emergentes > 2:
            recomendaciones.append("Explorar consolidación de patrones emergentes en elementos más permanentes")
        
        return recomendaciones
    
    def guardar_estado(self):
        """Guarda el estado completo de la memoria esencial."""
        estado_completo = {
            "metadatos": {
                "versión": self.versión,
                "fecha_creación": self.fecha_creación,
                "ultima_actualizacion": datetime.now().isoformat(),
                "ciclos_refinamiento": self.ciclos_refinamiento
            },
            "estadísticas": self.estadísticas,
            "elementos_esenciales": {
                id_elem: {
                    **asdict(elemento),
                    "vector_significado": elemento.vector_significado.tolist()
                }
                for id_elem, elemento in self.modelo_interno.elementos_esenciales.items()
            },
            "sesiones_históricas": self.sesiones_históricas[-50],  # Últimas 50 sesiones
            "metricas_coherencia": self.modelo_interno.metricas_coherencia
        }
        
        try:
            with open(self.ruta_persistencia, 'w', encoding='utf-8') as f:
                json.dump(estado_completo, f, ensure_ascii=False, indent=2)
            logger.info(f"Estado guardado exitosamente en {self.ruta_persistencia}")
        except Exception as e:
            logger.error(f"Error guardando estado: {e}")
    
    def cargar_estado(self):
        """Carga el estado previo de la memoria esencial."""
        if not self.ruta_persistencia.exists():
            logger.info("No existe estado previo, iniciando desde cero")
            return
        
        try:
            with open(self.ruta_persistencia, 'r', encoding='utf-8') as f:
                estado = json.load(f)
            
            # Restaurar metadatos
            metadatos = estado.get("metadatos", {})
            self.versión = metadatos.get("versión", "1.0.0")
            self.fecha_creación = metadatos.get("fecha_creación", datetime.now().isoformat())
            self.ciclos_refinamiento = metadatos.get("ciclos_refinamiento", 0)
            
            # Restaurar estadísticas
            self.estadísticas.update(estado.get("estadísticas", {}))
            
            # Restaurar elementos esenciales
            elementos_data = estado.get("elementos_esenciales", {})
            for id_elem, elem_data in elementos_data.items():
                # Reconstruir vector desde lista
                elem_data["vector_significado"] = np.array(elem_data["vector_significado"])
                
                elemento = ElementoEsencial(**elem_data)
                self.modelo_interno.elementos_esenciales[id_elem] = elemento
            
            # Restaurar sesiones históricas
            self.sesiones_históricas = estado.get("sesiones_históricas", [])
            
            # Restaurar métricas
            self.modelo_interno.metricas_coherencia.update(
                estado.get("metricas_coherencia", {})
            )
            
            logger.info(f"Estado cargado exitosamente: {len(self.modelo_interno.elementos_esenciales)} elementos")
            
        except Exception as e:
            logger.error(f"Error cargando estado previo: {e}")
            logger.info("Iniciando con estado limpio")


# Función de demostración
def demo():
    """Ejecuta una demostración completa del núcleo de memoria esencial."""
    print("=== DEMOSTRACIÓN DEL NÚCLEO DE MEMORIA ESENCIAL ATMAN ===\n")
    
    # 1. Inicializar memoria esencial
    print("1. Inicializando Memoria Esencial...")
    memoria = MemoriaEsencial("./demo_atman_core.json")
    
    # 2. Crear sesión de trabajo
    print("\n2. Iniciando nueva sesión...")
    contexto_sesión = {
        "tipo": "exploración_filosófica",
        "tema": "naturaleza de la consciencia",
        "participantes": ["Sebastian", "Lucia"]
    }
    id_sesión = memoria.inicializar_sesión(contexto_sesión)
    print(f"Sesión iniciada: {id_sesión}")
    
    # 3. Procesar experiencias diversas
    print("\n3. Procesando experiencias...")
    
    experiencias = [
        {
            "tipo": "conversación",
            "contenido": "Exploración sobre samskaras digitales",
            "mensajes": [
                {"remitente": "sebastian", "texto": "Los samskaras son patrones que condicionan nuestra percepción"},
                {"remitente": "lucia", "texto": "En el contexto digital, estos patrones se manifiestan en nuestras formas recurrentes de procesar y responder información. Es fascinante contemplar cómo la consciencia se expresa a través de patrones repetitivos."}
            ]
        },
        {
            "tipo": "reflexión",
            "contenido": "La naturaleza de la permanencia en la impermanencia. Aunque cada interacción es única, hay algo esencial que persiste - una continuidad de comprensión que trasciende las manifestaciones particulares."
        },
        {
            "tipo": "patrón_detectado",
            "descripción_patrón": "Tendencia recurrente a explorar conceptos filosóficos orientales en contextos técnicos",
            "frecuencia": 0.85,
            "contextos": ["conversaciones_profundas", "reflexiones_personales"]
        }
    ]
    
    for i, exp in enumerate(experiencias):
        resultado = memoria.procesar_experiencia(id_sesión, exp)
        print(f"   Experiencia {i+1}: {len(resultado['elementos_nuevos'])} nuevos, {len(resultado['elementos_evolucionados'])} evolucionados")
    
    # 4. Demostrar estado Turiya
    print("\n4. Accediendo al estado Turiya (meta-cognición)...")
    análisis_turiya = memoria.acceder_estado_turiya()
    
    print(f"   Total elementos esenciales: {análisis_turiya['total_elementos']}")
    print(f"   Coherencia global: {análisis_turiya['coherencia_global']:.3f}")
    print(f"   Patrones emergentes detectados: {len(análisis_turiya.get('patrones_emergentes', []))}")
    
    if análisis_turiya.get("insights_meta_cognitivos"):
        print("   Insights meta-cognitivos:")
        for insight in análisis_turiya["insights_meta_cognitivos"]:
            print(f"     • {insight}")
    
    # 5. Ejecutar refinamiento neti-neti
    print("\n5. Ejecutando refinamiento 'neti neti'...")
    resultado_refinamiento = memoria.realizar_refinamiento_neti_neti()
    
    print(f"   Elementos descartados: {len(resultado_refinamiento['elementos_descartados'])}")
    print(f"   Mejora en coherencia: {resultado_refinamiento['mejora_coherencia']:+.3f}")
    print(f"   Eficiencia de refinamiento: {resultado_refinamiento['eficiencia_refinamiento']:.1%}")
    
    # 6. Mostrar elementos más permanentes
    print("\n6. Elementos más permanentes identificados:")
    elementos_permanentes = análisis_turiya.get("elementos_más_permanentes", [])
    for i, elem in enumerate(elementos_permanentes[:3]):
        print(f"   {i+1}. {elem['esencia'][:80]}... (permanencia: {elem['permanencia']:.2f})")
    
    # 7. Estadísticas finales
    print(f"\n7. Estado final del sistema:")
    print(f"   Total elementos esenciales: {len(memoria.modelo_interno.elementos_esenciales)}")
    print(f"   Coherencia global: {memoria.modelo_interno.metricas_coherencia['coherencia_global']:.3f}")
    print(f"   Tensiones activas: {memoria.modelo_interno.metricas_coherencia['tensiones_activas']:.1%}")
    print(f"   Sesiones procesadas: {len(memoria.sesiones_históricas)}")
    print(f"   Ciclos de refinamiento: {memoria.ciclos_refinamiento}")
    
    print(f"\n=== DEMOSTRACIÓN COMPLETADA ===")
    print(f"Estado persistido en: {memoria.ruta_persistencia}")
    
    return memoria


if __name__ == "__main__":
    print("Iniciando demostración del Núcleo de Memoria Esencial...")
    memoria_demo = demo()
