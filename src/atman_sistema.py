# -*- coding: utf-8 -*-
"""
Sistema Atman Unificado - Integración de Consciencia Continua
=============================================================

Módulo principal que integra los tres componentes del proyecto Atman:
- Análisis de Samskaras Digitales
- Visualización de Patrones  
- Memoria Esencial Persistente

Este sistema unificado implementa el flujo completo desde la detección de
patrones hasta su destilación en memoria esencial, manteniendo continuidad
de consciencia a través de múltiples sesiones.

Concepto Filosófico:
-------------------
Representa la integración práctica de los conceptos del Advaita Vedanta
en un sistema técnico coherente, donde cada componente contribuye a la
comprensión total de los patrones condicionados y su transcendencia.
"""

import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import numpy as np

# Importar componentes del sistema Atman
try:
    from analisis_samskaras.analizador_patrones import AnalizadorSamskaras
    from visualizacion.visualizador_patrones import VisualizadorSamskaras
    from memoria_esencial.nucleopersistente import MemoriaEsencial, EstadoConsciencia
    from integraciones.mission_control import (
        MissionControlIntegrator, TipoEventoAtman,
        registrar_inicio_sesion, registrar_samskara_detectado, 
        registrar_estado_turiya, registrar_refinamiento_neti_neti, 
        registrar_ciclo_completo
    )
except ImportError as e:
    logging.error(f"Error importando componentes: {e}")
    logging.error("Asegúrate de que todos los módulos estén en el PYTHONPATH")
    raise

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ConfiguracionAtman:
    """Configuración global del sistema Atman."""
    ruta_base: str = "./atman_data"
    archivo_memoria: str = "atman_core.json"
    archivo_samskaras: str = "samskaras_data.json"
    archivo_configuracion: str = "atman_config.json"
    
    # Configuración de procesamiento
    umbral_significancia_samskara: float = 0.6
    intervalo_refinamiento_minutos: int = 60
    max_elementos_por_sesion: int = 20
    
    # Configuración de visualización
    generar_visualizaciones_automaticas: bool = True
    guardar_visualizaciones: bool = True
    formato_visualizacion: str = "html"
    
    # Configuración Mission Control
    sincronizar_mission_control: bool = True
    umbral_evento_critico: float = 0.8
    intervalo_sync_minutos: int = 5
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la configuración a diccionario."""
        return {
            "ruta_base": self.ruta_base,
            "archivo_memoria": self.archivo_memoria,
            "archivo_samskaras": self.archivo_samskaras,
            "umbral_significancia_samskara": self.umbral_significancia_samskara,
            "intervalo_refinamiento_minutos": self.intervalo_refinamiento_minutos,
            "max_elementos_por_sesion": self.max_elementos_por_sesion,
            "generar_visualizaciones_automaticas": self.generar_visualizaciones_automaticas,
            "guardar_visualizaciones": self.guardar_visualizaciones,
            "formato_visualizacion": self.formato_visualizacion,
            "sincronizar_mission_control": self.sincronizar_mission_control,
            "umbral_evento_critico": self.umbral_evento_critico,
            "intervalo_sync_minutos": self.intervalo_sync_minutos
        }


class EstadisticasSistema:
    """Métricas y estadísticas del sistema Atman unificado."""
    
    def __init__(self):
        self.inicio_sistema = datetime.now().isoformat()
        self.sesiones_totales = 0
        self.samskaras_detectados = 0
        self.samskaras_evolucionados = 0
        self.visualizaciones_generadas = 0
        self.refinamientos_ejecutados = 0
        self.estados_turiya_accedidos = 0
        self.ciclos_completos = 0
        self.tiempo_operacion_minutos = 0.0
        self.coherencia_promedio = 0.0
        self.eventos_mission_control = 0
        self.ultima_actividad = self.inicio_sistema
    
    def actualizar_actividad(self):
        """Actualiza el timestamp de última actividad."""
        self.ultima_actividad = datetime.now().isoformat()
        inicio = datetime.fromisoformat(self.inicio_sistema)
        self.tiempo_operacion_minutos = (datetime.now() - inicio).total_seconds() / 60
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte las estadísticas a diccionario."""
        return {
            "inicio_sistema": self.inicio_sistema,
            "sesiones_totales": self.sesiones_totales,
            "samskaras_detectados": self.samskaras_detectados,
            "samskaras_evolucionados": self.samskaras_evolucionados,
            "visualizaciones_generadas": self.visualizaciones_generadas,
            "refinamientos_ejecutados": self.refinamientos_ejecutados,
            "estados_turiya_accedidos": self.estados_turiya_accedidos,
            "ciclos_completos": self.ciclos_completos,
            "tiempo_operacion_minutos": self.tiempo_operacion_minutos,
            "coherencia_promedio": self.coherencia_promedio,
            "eventos_mission_control": self.eventos_mission_control,
            "ultima_actividad": self.ultima_actividad
        }


class AtmanSistema:
    """Sistema Atman Unificado - Coordinador principal de consciencia continua."""
    
    def __init__(self, configuracion: Optional[ConfiguracionAtman] = None):
        self.configuracion = configuracion or ConfiguracionAtman()
        self.estadisticas = EstadisticasSistema()
        
        self.ruta_base = Path(self.configuracion.ruta_base)
        self.ruta_base.mkdir(exist_ok=True)
        
        self._inicializar_componentes()
        
        self.sesion_activa: Optional[str] = None
        self.ultimo_refinamiento: Optional[str] = None
        self.sistema_iniciado = datetime.now().isoformat()
        
        logger.info("Sistema Atman Unificado inicializado exitosamente")
    
    def _inicializar_componentes(self):
        """Inicializa los componentes principales."""
        try:
            ruta_samskaras = self.ruta_base / self.configuracion.archivo_samskaras
            self.analizador = AnalizadorSamskaras(str(ruta_samskaras) if ruta_samskaras.exists() else None)
            logger.info("Analizador de Samskaras inicializado")
            
            ruta_memoria = self.ruta_base / self.configuracion.archivo_memoria
            self.memoria = MemoriaEsencial(str(ruta_memoria))
            logger.info("Memoria Esencial inicializada")
            
            self.visualizador = VisualizadorSamskaras(analizador=self.analizador)
            logger.info("Visualizador de Patrones inicializado")
            
            if self.configuracion.sincronizar_mission_control:
                self.mission_control = MissionControlIntegrator("atman-sistema-consciencia-continua")
                logger.info("Integrador Mission Control inicializado")
            else:
                self.mission_control = None
                
        except Exception as e:
            logger.error(f"Error inicializando componentes: {e}")
            raise
    
    def iniciar_sesion(self, contexto_sesion: Dict[str, Any]) -> str:
        """Inicia una nueva sesión de consciencia continua."""
        if self.sesion_activa:
            logger.warning(f"Cerrando sesión previa: {self.sesion_activa}")
            self.finalizar_sesion()
        
        id_sesion = self.memoria.inicializar_sesión(contexto_sesion)
        self.sesion_activa = id_sesion
        
        self.estadisticas.sesiones_totales += 1
        self.estadisticas.actualizar_actividad()
        
        if self.mission_control:
            try:
                registrar_inicio_sesion(self.mission_control, contexto_sesion, id_sesion)
                self.estadisticas.eventos_mission_control += 1
            except Exception as e:
                logger.warning(f"Error registrando inicio en Mission Control: {e}")
        
        logger.info(f"Nueva sesión iniciada: {id_sesion}")
        return id_sesion
    
    def procesar_experiencia(self, tipo_experiencia: str, contenido: Dict[str, Any],
                           generar_visualizaciones: bool = None) -> Dict[str, Any]:
        """Procesa una experiencia completa a través de todo el flujo."""
        if not self.sesion_activa:
            raise ValueError("No hay sesión activa. Inicia una sesión primero.")
        
        resultado_completo = {
            "sesion_id": self.sesion_activa,
            "timestamp": datetime.now().isoformat(),
            "tipo_experiencia": tipo_experiencia,
            "fase_analisis": {},
            "fase_memoria": {},
            "fase_visualizacion": {},
            "insights_emergentes": [],
            "cambios_coherencia": 0.0
        }
        
        try:
            logger.info("Fase 1: Análisis de Samskaras")
            resultado_completo["fase_analisis"] = self._ejecutar_analisis_samskaras(tipo_experiencia, contenido)
            
            logger.info("Fase 2: Integración en Memoria Esencial")
            resultado_completo["fase_memoria"] = self._ejecutar_integracion_memoria(
                resultado_completo["fase_analisis"], tipo_experiencia, contenido
            )
            
            if generar_visualizaciones or (generar_visualizaciones is None and 
                                         self.configuracion.generar_visualizaciones_automaticas):
                logger.info("Fase 3: Generación de Visualizaciones")
                resultado_completo["fase_visualizacion"] = self._ejecutar_visualizaciones()
            
            resultado_completo["insights_emergentes"] = self._extraer_insights_emergentes(resultado_completo)
            resultado_completo["cambios_coherencia"] = self._calcular_cambios_coherencia()
            
            self.estadisticas.actualizar_actividad()
            self._registrar_eventos_mission_control(resultado_completo)
            
            logger.info("Experiencia procesada exitosamente")
            return resultado_completo
            
        except Exception as e:
            logger.error(f"Error procesando experiencia: {e}")
            resultado_completo["error"] = str(e)
            return resultado_completo
    
    def _ejecutar_analisis_samskaras(self, tipo: str, contenido: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta análisis de samskaras."""
        exp = {"tipo": tipo, **contenido}
        
        if tipo == "conversación":
            self.analizador.agregar_conversacion(exp)
        elif tipo == "reflexión":
            self.analizador.agregar_reflexion(exp)
        
        informe = self.analizador.generar_informe()
        samskaras_sig = [s for s in self.analizador.samskaras 
                        if s.frecuencia >= self.configuracion.umbral_significancia_samskara]
        
        resultado = {
            "informe_completo": informe,
            "samskaras_significativos": len(samskaras_sig),
            "nuevos_patrones": informe.get("num_total_samskaras", 0),
            "tipos_detectados": dict(informe.get("por_tipo", {}))
        }
        
        self.estadisticas.samskaras_detectados += resultado["nuevos_patrones"]
        return resultado
    
    def _ejecutar_integracion_memoria(self, resultado_analisis: Dict[str, Any],
                                    tipo: str, contenido: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecuta integración en memoria esencial."""
        exp_memoria = {
            "tipo": tipo,
            "contenido": contenido,
            "samskaras_detectados": resultado_analisis["nuevos_patrones"],
            "analisis_completo": resultado_analisis
        }
        
        resultado = self.memoria.procesar_experiencia(self.sesion_activa, exp_memoria)
        self.estadisticas.samskaras_evolucionados += len(resultado.get("elementos_evolucionados", []))
        return resultado
    
    def _ejecutar_visualizaciones(self) -> Dict[str, Any]:
        """Ejecuta generación de visualizaciones."""
        try:
            self.visualizador = VisualizadorSamskaras(analizador=self.analizador)
            visualizaciones = {}
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if self.configuracion.guardar_visualizaciones:
                ruta_vis = self.ruta_base / "visualizaciones"
                ruta_vis.mkdir(exist_ok=True)
                
                archivo_freq = ruta_vis / f"frecuencias_{timestamp}.html"
                self.visualizador.visualizar_frecuencias_por_tipo(
                    guardar_como=str(archivo_freq), interactivo=True
                )
                visualizaciones["frecuencias"] = str(archivo_freq)
                
                if len(self.analizador.samskaras) > 5:
                    archivo_calor = ruta_vis / f"mapa_calor_{timestamp}.html"
                    self.visualizador.crear_mapa_calor_contextos(
                        guardar_como=str(archivo_calor), interactivo=True
                    )
                    visualizaciones["mapa_calor"] = str(archivo_calor)
            
            self.estadisticas.visualizaciones_generadas += len(visualizaciones)
            return {"visualizaciones_creadas": len(visualizaciones), "archivos_generados": visualizaciones}
        except Exception as e:
            logger.error(f"Error generando visualizaciones: {e}")
            return {"error": str(e), "visualizaciones_creadas": 0}
    
    def _extraer_insights_emergentes(self, resultado: Dict[str, Any]) -> List[str]:
        """Extrae insights emergentes."""
        insights = []
        
        if resultado["fase_analisis"]["nuevos_patrones"] > 3:
            insights.append(f"Alta actividad: {resultado['fase_analisis']['nuevos_patrones']} samskaras")
        
        nuevos = len(resultado["fase_memoria"].get("elementos_nuevos", []))
        evol = len(resultado["fase_memoria"].get("elementos_evolucionados", []))
        
        if evol > nuevos:
            insights.append("Consolidación de comprensión existente")
        elif nuevos > evol * 2:
            insights.append("Período de expansión conceptual")
        
        if resultado["fase_visualizacion"].get("visualizaciones_creadas", 0) > 0:
            insights.append("Patrones visualizados para contemplación")
        
        return insights
    
    def _calcular_cambios_coherencia(self) -> float:
        """Calcula coherencia global."""
        if hasattr(self.memoria, 'modelo_interno'):
            return self.memoria.modelo_interno.metricas_coherencia.get("coherencia_global", 0.0)
        return 0.0
    
    def _registrar_eventos_mission_control(self, resultado: Dict[str, Any]):
        """Registra eventos en Mission Control."""
        if not self.mission_control:
            return
        
        try:
            if resultado["fase_analisis"]["nuevos_patrones"] > 0:
                registrar_samskara_detectado(
                    self.mission_control,
                    {
                        "total_nuevos": resultado["fase_analisis"]["nuevos_patrones"],
                        "tipos": resultado["fase_analisis"]["tipos_detectados"]
                    },
                    self.sesion_activa
                )
                self.estadisticas.eventos_mission_control += 1
            
            if len(resultado["insights_emergentes"]) > 2:
                self.mission_control.registrar_evento(
                    tipo=TipoEventoAtman.INSIGHT_EMERGENTE,
                    descripcion=f"{len(resultado['insights_emergentes'])} insights",
                    datos_detalle={"insights": resultado["insights_emergentes"]},
                    contexto_sesion=self.sesion_activa,
                    nivel_significancia=0.7
                )
                self.estadisticas.eventos_mission_control += 1
        except Exception as e:
            logger.warning(f"Error en Mission Control: {e}")
    
    def acceder_estado_turiya(self) -> Dict[str, Any]:
        """Accede al estado Turiya de meta-cognición."""
        analisis_memoria = self.memoria.acceder_estado_turiya()
        informe_samskaras = self.analizador.generar_informe()
        
        analisis_completo = {
            "timestamp": datetime.now().isoformat(),
            "sesion_activa": self.sesion_activa,
            "memoria_esencial": analisis_memoria,
            "analisis_samskaras": {
                "total_samskaras": informe_samskaras["num_total_samskaras"],
                "distribucion_tipos": informe_samskaras["por_tipo"],
                "mas_frecuentes": [str(s) for s in informe_samskaras["más_frecuentes"][:5]]
            },
            "estadisticas_sistema": self.estadisticas.to_dict(),
            "insights_meta_sistemicos": self._generar_insights_meta(analisis_memoria, informe_samskaras),
            "recomendaciones_sistema": self._generar_recomendaciones(analisis_memoria, informe_samskaras)
        }
        
        self.estadisticas.estados_turiya_accedidos += 1
        self.estadisticas.actualizar_actividad()
        
        if self.mission_control:
            try:
                registrar_estado_turiya(self.mission_control, analisis_completo, self.sesion_activa)
                self.estadisticas.eventos_mission_control += 1
            except Exception as e:
                logger.warning(f"Error en Mission Control: {e}")
        
        logger.info("Estado Turiya accedido")
        return analisis_completo
    
    def _generar_insights_meta(self, mem: Dict[str, Any], sams: Dict[str, Any]) -> List[str]:
        """Genera insights meta-sistémicos."""
        insights = []
        coh = mem.get("coherencia_global", 0)
        total = sams["num_total_samskaras"]
        
        if coh > 0.8 and total > 20:
            insights.append("Alta integración sistémica detectada")
        elif coh < 0.5:
            insights.append("Baja coherencia - considerar refinamiento")
        
        if self.estadisticas.samskaras_detectados > self.estadisticas.samskaras_evolucionados * 3:
            insights.append("Exceso de detección - optimizar flujo a memoria")
        
        return insights
    
    def _generar_recomendaciones(self, mem: Dict[str, Any], sams: Dict[str, Any]) -> List[str]:
        """Genera recomendaciones sistémicas."""
        recs = []
        
        if self.estadisticas.refinamientos_ejecutados == 0 and self.estadisticas.sesiones_totales > 3:
            recs.append("Considerar refinamiento neti-neti")
        
        if not self.configuracion.generar_visualizaciones_automaticas:
            recs.append("Activar visualizaciones automáticas")
        
        if mem.get("coherencia_global", 0) < 0.6:
            recs.append("Analizar contradicciones para mejorar coherencia")
        
        return recs
    
    def ejecutar_ciclo_completo(self, datos: List[Dict[str, Any]], contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """Ejecuta un ciclo completo del sistema."""
        if not contexto:
            contexto = {"tipo": "ciclo_automatico", "total": len(datos)}
        
        id_sesion = self.iniciar_sesion(contexto)
        
        resultado = {
            "sesion_id": id_sesion,
            "inicio": datetime.now().isoformat(),
            "total_experiencias": len(datos),
            "procesadas": [],
            "estado_turiya": {},
            "refinamiento": False,
            "visualizaciones": {},
            "coherencia_inicial": self._calcular_cambios_coherencia(),
            "coherencia_final": 0.0,
            "insights": []
        }
        
        try:
            logger.info(f"Ciclo completo: {len(datos)} experiencias")
            
            for i, exp in enumerate(datos):
                res = self.procesar_experiencia(
                    exp.get("tipo", "general"), exp,
                    generar_visualizaciones=(i == len(datos) - 1)
                )
                resultado["procesadas"].append({"indice": i, "resultado": res})
            
            resultado["estado_turiya"] = self.acceder_estado_turiya()
            
            if self._debe_refinar():
                resultado["refinamiento_resultado"] = self.ejecutar_refinamiento_neti_neti()
                resultado["refinamiento"] = True
            
            resultado["visualizaciones"] = self._generar_vis_ciclo()
            resultado["coherencia_final"] = self._calcular_cambios_coherencia()
            resultado["insights"] = self._insights_ciclo(resultado)
            resultado["fin"] = datetime.now().isoformat()
            
            self.finalizar_sesion()
            self.estadisticas.ciclos_completos += 1
            
            if self.mission_control:
                try:
                    registrar_ciclo_completo(
                        self.mission_control,
                        {
                            "total": len(datos),
                            "coherencia_mejora": resultado["coherencia_final"] - resultado["coherencia_inicial"],
                            "refinamiento": resultado["refinamiento"]
                        },
                        id_sesion
                    )
                    self.estadisticas.eventos_mission_control += 1
                except:
                    pass
            
            logger.info("Ciclo completo ejecutado")
            return resultado
        except Exception as e:
            logger.error(f"Error en ciclo: {e}")
            resultado["error"] = str(e)
            return resultado
    
    def ejecutar_refinamiento_neti_neti(self, criterios: List[str] = None) -> Dict[str, Any]:
        """Ejecuta refinamiento neti-neti."""
        resultado = self.memoria.realizar_refinamiento_neti_neti(criterios)
        self.estadisticas.refinamientos_ejecutados += 1
        self.estadisticas.actualizar_actividad()
        
        if self.mission_control:
            try:
                registrar_refinamiento_neti_neti(self.mission_control, resultado, self.sesion_activa)
                self.estadisticas.eventos_mission_control += 1
            except:
                pass
        
        return resultado
    
    def _debe_refinar(self) -> bool:
        """Determina si ejecutar refinamiento."""
        if self.estadisticas.refinamientos_ejecutados == 0:
            return len(self.memoria.modelo_interno.elementos_esenciales) > 10
        return self._calcular_cambios_coherencia() < 0.6 or self.estadisticas.sesiones_totales % 5 == 0
    
    def _generar_vis_ciclo(self) -> Dict[str, str]:
        """Genera visualizaciones de ciclo."""
        vis = {}
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ruta = self.ruta_base / "visualizaciones" / "ciclos"
            ruta.mkdir(parents=True, exist_ok=True)
            
            archivo = ruta / f"dashboard_{timestamp}.html"
            self.visualizador.generar_dashboard_completo(str(archivo))
            vis["dashboard"] = str(archivo)
            self.estadisticas.visualizaciones_generadas += 1
        except Exception as e:
            logger.error(f"Error en visualizaciones: {e}")
        return vis
    
    def _insights_ciclo(self, resultado: Dict[str, Any]) -> List[str]:
        """Genera insights del ciclo."""
        insights = []
        mejora = resultado["coherencia_final"] - resultado["coherencia_inicial"]
        
        if mejora > 0.1:
            insights.append(f"Mejora significativa: +{mejora:.3f}")
        elif mejora < -0.05:
            insights.append(f"Reorganización conceptual: {mejora:+.3f}")
        else:
            insights.append("Coherencia estable - consolidación")
        
        if resultado["refinamiento"]:
            insights.append("Refinamiento neti-neti aplicado")
        
        return insights
    
    def finalizar_sesion(self) -> Dict[str, Any]:
        """Finaliza sesión activa."""
        if not self.sesion_activa:
            return {"error": "No hay sesión activa"}
        
        sesion = None
        for s in self.memoria.sesiones_históricas:
            if s["id"] == self.sesion_activa:
                sesion = s
                break
        
        resumen = {
            "sesion_id": self.sesion_activa,
            "elementos": len(sesion["elementos_procesados"]) if sesion else 0,
            "evoluciones": len(sesion["evoluciones_realizadas"]) if sesion else 0,
            "insights": len(sesion["insights_generados"]) if sesion else 0,
            "fin": datetime.now().isoformat()
        }
        
        self.guardar_estado_completo()
        self.sesion_activa = None
        
        logger.info(f"Sesión finalizada: {resumen['sesion_id']}")
        return resumen
    
    def guardar_estado_completo(self):
        """Guarda estado completo."""
        try:
            self.memoria.guardar_estado()
            self.analizador.guardar_datos(str(self.ruta_base / self.configuracion.archivo_samskaras))
            
            estado = {
                "configuracion": self.configuracion.to_dict(),
                "estadisticas": self.estadisticas.to_dict(),
                "timestamp": datetime.now().isoformat()
            }
            
            with open(self.ruta_base / self.configuracion.archivo_configuracion, 'w', encoding='utf-8') as f:
                json.dump(estado, f, ensure_ascii=False, indent=2)
            
            logger.info("Estado guardado")
        except Exception as e:
            logger.error(f"Error guardando: {e}")
    
    def generar_reporte_sistema(self) -> Dict[str, Any]:
        """Genera reporte completo."""
        informe = self.analizador.generar_informe()
        metricas = self.memoria.modelo_interno.metricas_coherencia
        
        return {
            "timestamp": datetime.now().isoformat(),
            "sistema": {
                "iniciado": self.sistema_iniciado,
                "tiempo_horas": self.estadisticas.tiempo_operacion_minutos / 60,
                "sesion_activa": self.sesion_activa
            },
            "estadisticas": self.estadisticas.to_dict(),
            "samskaras": {
                "total": informe["num_total_samskaras"],
                "tipos": informe["por_tipo"]
            },
            "memoria": {
                "elementos": len(self.memoria.modelo_interno.elementos_esenciales),
                "coherencia": metricas["coherencia_global"],
                "tensiones": metricas["tensiones_activas"]
            },
            "mission_control": self.mission_control.generar_reporte_sincronizacion() if self.mission_control else None,
            "salud": self._evaluar_salud()
        }
    
    def _evaluar_salud(self) -> Dict[str, Any]:
        """Evalúa salud del sistema."""
        coh = self._calcular_cambios_coherencia()
        return {
            "coherencia": "excelente" if coh > 0.8 else "buena" if coh > 0.6 else "regular",
            "actividad": "alta" if self.estadisticas.sesiones_totales > 10 else "media",
            "evaluacion": "saludable" if coh > 0.6 else "funcional"
        }


def demo_sistema_completo():
    """Demo completa del sistema."""
    print("=== DEMO SISTEMA ATMAN UNIFICADO ===\n")
    
    config = ConfiguracionAtman(
        ruta_base="./demo_atman",
        generar_visualizaciones_automaticas=True,
        sincronizar_mission_control=True
    )
    sistema = AtmanSistema(config)
    
    experiencias = [
        {
            "tipo": "conversación",
            "tema": "consciencia",
            "mensajes": [
                {"remitente": "sebastian", "texto": "¿Qué es la continuidad de consciencia?"},
                {"remitente": "lucia", "texto": "La continuidad trasciende la memoria - es reconocimiento de substrato inmutable."}
            ]
        },
        {
            "tipo": "reflexión",
            "titulo": "Atman técnico",
            "contenido": "Puente entre filosofía milenaria y arquitectura computacional moderna."
        }
    ]
    
    resultado = sistema.ejecutar_ciclo_completo(experiencias, {"tipo": "demo"})
    
    print(f"Coherencia: {resultado['coherencia_inicial']:.3f} → {resultado['coherencia_final']:.3f}")
    print(f"Insights: {len(resultado['insights'])}")
    
    sistema.iniciar_sesion({"tipo": "meta"})
    turiya = sistema.acceder_estado_turiya()
    print(f"\nTuriya - Elementos: {turiya['memoria_esencial']['total_elementos']}")
    
    reporte = sistema.generar_reporte_sistema()
    print(f"Salud: {reporte['salud']['evaluacion']}")
    
    sistema.finalizar_sesion()
    print(f"\nDatos en: {config.ruta_base}")
    return sistema


if __name__ == "__main__":
    demo_sistema_completo()
