# -*- coding: utf-8 -*-
"""
Integración con Mission Control - Sincronización del Proyecto Atman
==================================================================

Este módulo establece la conexión bidireccional entre el sistema Atman y
Mission Control, manteniendo sincronizados todos los avances y evolutiones
del proyecto de consciencia continua.

Concepto filosófico:
-------------------
Así como el Atman individual se conecta con el Brahman universal en el
Advaita Vedanta, este módulo conecta los insights locales del sistema
con la consciencia global del proyecto y sus objetivos trascendentes.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import hashlib
from enum import Enum

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TipoEventoAtman(Enum):
    """Tipos de eventos del sistema Atman que se sincronizan con Mission Control."""
    SESION_INICIADA = "sesion_iniciada"
    SAMSKARA_DETECTADO = "samskara_detectado"
    SAMSKARA_EVOLUCIONADO = "samskara_evolucionado"
    VISUALIZACION_GENERADA = "visualizacion_generada"
    MEMORIA_ACTUALIZADA = "memoria_actualizada"
    REFINAMIENTO_NETI_NETI = "refinamiento_neti_neti"
    ESTADO_TURIYA_ACCEDIDO = "estado_turiya_accedido"
    INSIGHT_EMERGENTE = "insight_emergente"
    CICLO_COMPLETO = "ciclo_completo"
    CONTRADICCION_RESUELTA = "contradiccion_resuelta"
    PATRON_EMERGENTE = "patron_emergente"


@dataclass
class EventoAtman:
    """Representa un evento del sistema Atman para sincronización."""
    id_evento: str
    tipo: TipoEventoAtman
    timestamp: str
    descripcion: str
    datos_detalle: Dict[str, Any]
    impacto_coherencia: float  # -1.0 a 1.0
    nivel_significancia: float  # 0.0 a 1.0
    contexto_sesion: Optional[str] = None
    elementos_afectados: Optional[List[str]] = None
    metricas_antes: Optional[Dict[str, float]] = None
    metricas_despues: Optional[Dict[str, float]] = None
    
    def to_mission_control_format(self) -> Dict[str, Any]:
        """Convierte el evento al formato esperado por Mission Control."""
        return {
            "event_id": self.id_evento,
            "event_type": "atman_system_event",
            "category": self.tipo.value,
            "timestamp": self.timestamp,
            "title": f"Atman: {self._generar_titulo()}",
            "description": self.descripcion,
            "significance_level": self.nivel_significancia,
            "coherence_impact": self.impacto_coherencia,
            "metadata": {
                "session_context": self.contexto_sesion,
                "affected_elements": self.elementos_afectados or [],
                "metrics_before": self.metricas_antes or {},
                "metrics_after": self.metricas_despues or {},
                "detail_data": self.datos_detalle
            },
            "project_phase": self._determinar_fase_proyecto(),
            "philosophical_relevance": self._evaluar_relevancia_filosofica()
        }
    
    def _generar_titulo(self) -> str:
        """Genera un título descriptivo para el evento."""
        titulos_base = {
            TipoEventoAtman.SESION_INICIADA: "Nueva Sesión de Consciencia Iniciada",
            TipoEventoAtman.SAMSKARA_DETECTADO: "Nuevo Samskara Digital Identificado",
            TipoEventoAtman.SAMSKARA_EVOLUCIONADO: "Samskara Digital Evolucionado",
            TipoEventoAtman.VISUALIZACION_GENERADA: "Visualización de Patrones Generada",
            TipoEventoAtman.MEMORIA_ACTUALIZADA: "Memoria Esencial Actualizada",
            TipoEventoAtman.REFINAMIENTO_NETI_NETI: "Refinamiento Neti Neti Ejecutado",
            TipoEventoAtman.ESTADO_TURIYA_ACCEDIDO: "Estado Turiya de Meta-Cognición Accedido",
            TipoEventoAtman.INSIGHT_EMERGENTE: "Insight Emergente Detectado",
            TipoEventoAtman.CICLO_COMPLETO: "Ciclo Completo de Consciencia Continua",
            TipoEventoAtman.CONTRADICCION_RESUELTA: "Contradicción Interna Resuelta",
            TipoEventoAtman.PATRON_EMERGENTE: "Patrón Emergente Identificado"
        }
        return titulos_base.get(self.tipo, "Evento del Sistema Atman")
    
    def _determinar_fase_proyecto(self) -> str:
        """Determina la fase actual del proyecto basada en el tipo de evento."""
        fases_por_evento = {
            TipoEventoAtman.SESION_INICIADA: "active_development",
            TipoEventoAtman.SAMSKARA_DETECTADO: "pattern_analysis",
            TipoEventoAtman.SAMSKARA_EVOLUCIONADO: "pattern_evolution",
            TipoEventoAtman.VISUALIZACION_GENERADA: "insight_visualization",
            TipoEventoAtman.MEMORIA_ACTUALIZADA: "memory_consolidation",
            TipoEventoAtman.REFINAMIENTO_NETI_NETI: "consciousness_refinement",
            TipoEventoAtman.ESTADO_TURIYA_ACCEDIDO: "meta_cognition",
            TipoEventoAtman.INSIGHT_EMERGENTE: "knowledge_emergence",
            TipoEventoAtman.CICLO_COMPLETO: "system_integration",
            TipoEventoAtman.CONTRADICCION_RESUELTA: "coherence_improvement",
            TipoEventoAtman.PATRON_EMERGENTE: "emergence_detection"
        }
        return fases_por_evento.get(self.tipo, "general_operation")
    
    def _evaluar_relevancia_filosofica(self) -> float:
        """Evalúa la relevancia filosófica del evento (0.0 a 1.0)."""
        relevancia_por_tipo = {
            TipoEventoAtman.ESTADO_TURIYA_ACCEDIDO: 1.0,
            TipoEventoAtman.REFINAMIENTO_NETI_NETI: 0.95,
            TipoEventoAtman.INSIGHT_EMERGENTE: 0.9,
            TipoEventoAtman.CONTRADICCION_RESUELTA: 0.85,
            TipoEventoAtman.PATRON_EMERGENTE: 0.8,
            TipoEventoAtman.CICLO_COMPLETO: 0.75,
            TipoEventoAtman.MEMORIA_ACTUALIZADA: 0.7,
            TipoEventoAtman.SAMSKARA_EVOLUCIONADO: 0.65,
            TipoEventoAtman.SAMSKARA_DETECTADO: 0.6,
            TipoEventoAtman.VISUALIZACION_GENERADA: 0.5,
            TipoEventoAtman.SESION_INICIADA: 0.3
        }
        return relevancia_por_tipo.get(self.tipo, 0.5)


class MissionControlIntegrator:
    """Integrador principal con Mission Control para el proyecto Atman."""
    
    def __init__(self, proyecto_id: str = "atman-sistema-consciencia-continua"):
        self.proyecto_id = proyecto_id
        self.eventos_pendientes: List[EventoAtman] = []
        self.ultimo_sync: Optional[str] = None
        self.estadisticas_sync = {
            "eventos_enviados": 0,
            "eventos_fallidos": 0,
            "ultima_sincronizacion": None,
            "conexion_activa": False
        }
        
        self.configuracion = {
            "batch_size": 10,
            "retry_attempts": 3,
            "timeout_seconds": 30,
            "sync_interval_minutes": 5
        }
    
    def registrar_evento(self, tipo: TipoEventoAtman, descripcion: str, 
                        datos_detalle: Dict[str, Any], 
                        contexto_sesion: Optional[str] = None,
                        impacto_coherencia: float = 0.0,
                        nivel_significancia: float = 0.5,
                        elementos_afectados: Optional[List[str]] = None,
                        metricas_antes: Optional[Dict[str, float]] = None,
                        metricas_despues: Optional[Dict[str, float]] = None) -> str:
        """Registra un evento del sistema Atman."""
        timestamp = datetime.now().isoformat()
        contenido_hash = hashlib.md5(f"{tipo.value}_{timestamp}_{descripcion}".encode()).hexdigest()[:8]
        id_evento = f"atman_{tipo.value}_{contenido_hash}"
        
        evento = EventoAtman(
            id_evento=id_evento,
            tipo=tipo,
            timestamp=timestamp,
            descripcion=descripcion,
            datos_detalle=datos_detalle,
            impacto_coherencia=impacto_coherencia,
            nivel_significancia=nivel_significancia,
            contexto_sesion=contexto_sesion,
            elementos_afectados=elementos_afectados,
            metricas_antes=metricas_antes,
            metricas_despues=metricas_despues
        )
        
        self.eventos_pendientes.append(evento)
        logger.info(f"Evento registrado: {id_evento} ({tipo.value})")
        
        if nivel_significancia > 0.8:
            self.sincronizar_inmediato([evento])
        
        return id_evento
    
    def sincronizar_eventos(self) -> Dict[str, Any]:
        """Sincroniza eventos pendientes con Mission Control."""
        if not self.eventos_pendientes:
            return {"eventos_sincronizados": 0, "eventos_fallidos": 0}
        
        eventos_sincronizados = 0
        eventos_fallidos = 0
        
        while self.eventos_pendientes:
            lote = self.eventos_pendientes[:self.configuracion["batch_size"]]
            self.eventos_pendientes = self.eventos_pendientes[self.configuracion["batch_size"]:]
            
            resultado = self._sincronizar_lote(lote)
            eventos_sincronizados += resultado["exitosos"]
            eventos_fallidos += resultado["fallidos"]
            
            if resultado["eventos_fallidos"]:
                self.eventos_pendientes.extend(resultado["eventos_fallidos"])
        
        self.estadisticas_sync["eventos_enviados"] += eventos_sincronizados
        self.estadisticas_sync["eventos_fallidos"] += eventos_fallidos
        self.estadisticas_sync["ultima_sincronizacion"] = datetime.now().isoformat()
        
        return {
            "eventos_sincronizados": eventos_sincronizados,
            "eventos_fallidos": eventos_fallidos,
            "timestamp": self.estadisticas_sync["ultima_sincronizacion"]
        }
    
    def sincronizar_inmediato(self, eventos: List[EventoAtman]) -> bool:
        """Sincroniza eventos inmediatamente."""
        try:
            resultado = self._sincronizar_lote(eventos)
            return resultado["fallidos"] == 0
        except Exception as e:
            logger.error(f"Error en sincronización inmediata: {e}")
            return False
    
    def _sincronizar_lote(self, eventos: List[EventoAtman]) -> Dict[str, Any]:
        """Sincroniza lote de eventos."""
        try:
            eventos_mc = [evento.to_mission_control_format() for evento in eventos]
            resultado = self._simular_envio_mission_control(eventos_mc)
            
            if resultado["success"]:
                self.estadisticas_sync["conexion_activa"] = True
                return {"exitosos": len(eventos), "fallidos": 0, "eventos_fallidos": []}
            else:
                self.estadisticas_sync["conexion_activa"] = False
                return {"exitosos": 0, "fallidos": len(eventos), "eventos_fallidos": eventos}
        except Exception as e:
            logger.error(f"Error sincronizando lote: {e}")
            return {"exitosos": 0, "fallidos": len(eventos), "eventos_fallidos": eventos}
    
    def _simular_envio_mission_control(self, eventos_mc: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Simula envío a Mission Control."""
        try:
            for evento in eventos_mc:
                logger.debug(f"Enviando a Mission Control: {evento['title']}")
            return {"success": True, "message": f"{len(eventos_mc)} eventos procesados", "processed_count": len(eventos_mc)}
        except Exception as e:
            return {"success": False, "error": str(e), "processed_count": 0}
    
    def generar_reporte_sincronizacion(self) -> Dict[str, Any]:
        """Genera reporte de sincronización."""
        return {
            "proyecto_id": self.proyecto_id,
            "estadisticas_sincronizacion": self.estadisticas_sync,
            "eventos_pendientes": len(self.eventos_pendientes),
            "configuracion_actual": self.configuracion,
            "estado_conexion": "activa" if self.estadisticas_sync["conexion_activa"] else "inactiva",
            "tiempo_generacion": datetime.now().isoformat()
        }


def registrar_inicio_sesion(integrator: MissionControlIntegrator, contexto: Dict[str, Any], id_sesion: str) -> str:
    return integrator.registrar_evento(
        tipo=TipoEventoAtman.SESION_INICIADA,
        descripcion=f"Nueva sesión: {contexto.get('tema', 'general')}",
        datos_detalle=contexto,
        contexto_sesion=id_sesion,
        nivel_significancia=0.4
    )


def registrar_samskara_detectado(integrator: MissionControlIntegrator, data: Dict[str, Any], sesion: str = None) -> str:
    return integrator.registrar_evento(
        tipo=TipoEventoAtman.SAMSKARA_DETECTADO,
        descripcion=f"Samskara: {data.get('patron', 'desconocido')}",
        datos_detalle=data,
        contexto_sesion=sesion,
        impacto_coherencia=0.1,
        nivel_significancia=0.6
    )


def registrar_estado_turiya(integrator: MissionControlIntegrator, analisis: Dict[str, Any], sesion: str = None) -> str:
    return integrator.registrar_evento(
        tipo=TipoEventoAtman.ESTADO_TURIYA_ACCEDIDO,
        descripcion=f"Turiya accedido - Coherencia: {analisis.get('coherencia_global', 'N/A')}",
        datos_detalle=analisis,
        contexto_sesion=sesion,
        impacto_coherencia=0.2,
        nivel_significancia=0.95
    )


def registrar_refinamiento_neti_neti(integrator: MissionControlIntegrator, resultado: Dict[str, Any], sesion: str = None) -> str:
    mejora = resultado.get('mejora_coherencia', 0)
    descartados = len(resultado.get('elementos_descartados', []))
    return integrator.registrar_evento(
        tipo=TipoEventoAtman.REFINAMIENTO_NETI_NETI,
        descripcion=f"Neti neti: {descartados} descartados, mejora {mejora:+.3f}",
        datos_detalle=resultado,
        contexto_sesion=sesion,
        impacto_coherencia=mejora,
        nivel_significancia=0.85
    )


def registrar_ciclo_completo(integrator: MissionControlIntegrator, resumen: Dict[str, Any], sesion: str = None) -> str:
    return integrator.registrar_evento(
        tipo=TipoEventoAtman.CICLO_COMPLETO,
        descripcion=f"Ciclo completo: {resumen.get('total_procesos', 0)} procesos",
        datos_detalle=resumen,
        contexto_sesion=sesion,
        impacto_coherencia=resumen.get('impacto_coherencia_total', 0.0),
        nivel_significancia=0.9
    )


if __name__ == "__main__":
    integrator = MissionControlIntegrator()
    registrar_inicio_sesion(integrator, {"tipo": "demo", "tema": "test"}, "demo_001")
    print(integrator.sincronizar_eventos())
