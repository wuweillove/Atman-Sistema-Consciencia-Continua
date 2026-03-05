# -*- coding: utf-8 -*-
"""
Visualizador de Samskaras Digitales - Módulo de Visualización
============================================================

Este módulo implementa la visualización interactiva de samskaras digitales
identificados por el analizador de patrones. Permite explorar la evolución
temporal de patrones, su frecuencia relativa y las relaciones entre conceptos.

Concepto filosófico:
-------------------
La visualización de samskaras permite la contemplación directa de nuestros
patrones condicionados. En el Advaita Vedanta, la observación consciente
(sakshi-bhava) es fundamental para trascender las limitaciones mentales.
Este módulo facilita esa observación sistemática de patrones digitales.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd

# Configurar matplotlib para usar fonts que soporten caracteres especiales
plt.rcParams['font.family'] = ['DejaVu Sans', 'Liberation Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# Colores inspirados en elementos naturales para las visualizaciones
COLORES_ELEMENTOS = {
    'LINGUISTICO': '#2E8B57',     # Verde bosque (elemento tierra)
    'CONCEPTUAL': '#4169E1',      # Azul real (elemento agua)
    'RESPUESTA': '#DC143C',       # Rojo carmín (elemento fuego)
    'GENERAL': '#708090',         # Gris pizarra (elemento aire)
    'EVOLUCION': '#9370DB'        # Púrpura medio (elemento éter)
}


class VisualizadorSamskaras:
    """Generador de visualizaciones para samskaras digitales."""
    
    def __init__(self, analizador=None, datos_archivo=None):
        """
        Inicializa el visualizador con datos del analizador o desde archivo.
        
        Args:
            analizador: Instancia de AnalizadorSamskaras
            datos_archivo: Ruta al archivo JSON con datos de samskaras
        """
        self.samskaras = []
        self.conversaciones = []
        self.reflexiones = []
        
        if analizador:
            self.samskaras = analizador.samskaras
            self.conversaciones = analizador.conversaciones
            self.reflexiones = analizador.reflexiones
        elif datos_archivo:
            self.cargar_datos(datos_archivo)
        
        # Configurar estilo de matplotlib
        self._configurar_estilo_matplotlib()
    
    def cargar_datos(self, ruta_archivo: str):
        """Carga datos de samskaras desde archivo JSON."""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                self.conversaciones = datos.get("conversaciones", [])
                self.reflexiones = datos.get("reflexiones", [])
                
                # Reconstruir objetos SamskaraDigital
                from analisis_samskaras.analizador_patrones import SamskaraDigital
                samskaras_data = datos.get("samskaras", [])
                for s_data in samskaras_data:
                    samskara = SamskaraDigital(
                        s_data["tipo"],
                        s_data["subtipo"],
                        s_data["patron"],
                        s_data["ejemplos"],
                        s_data["frecuencia"],
                        s_data["contextos"]
                    )
                    samskara.primera_aparicion = s_data.get("primera_aparicion")
                    samskara.ultima_aparicion = s_data.get("ultima_aparicion")
                    samskara.evolución = s_data.get("evolución", [])
                    self.samskaras.append(samskara)
        except FileNotFoundError:
            print(f"Archivo {ruta_archivo} no encontrado.")
        except Exception as e:
            print(f"Error cargando datos: {e}")
    
    def _configurar_estilo_matplotlib(self):
        """Configura el estilo visual para matplotlib."""
        plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
        
        # Configuración personalizada
        plt.rcParams.update({
            'figure.figsize': (12, 8),
            'font.size': 10,
            'axes.titlesize': 14,
            'axes.labelsize': 12,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.titlesize': 16
        })
    
    def visualizar_frecuencias_por_tipo(self, guardar_como=None, interactivo=False):
        """
        Genera visualización de frecuencias de samskaras por tipo.
        
        Args:
            guardar_como: Nombre del archivo para guardar (opcional)
            interactivo: Si True, genera visualización interactiva con Plotly
        """
        if not self.samskaras:
            print("No hay samskaras para visualizar.")
            return
        
        # Contar samskaras por tipo
        conteo_tipos = Counter([s.tipo for s in self.samskaras])
        frecuencias_promedio = defaultdict(list)
        
        for samskara in self.samskaras:
            frecuencias_promedio[samskara.tipo].append(samskara.frecuencia)
        
        if interactivo:
            return self._crear_grafico_frecuencias_interactivo(conteo_tipos, frecuencias_promedio, guardar_como)
        else:
            return self._crear_grafico_frecuencias_matplotlib(conteo_tipos, frecuencias_promedio, guardar_como)
    
    def _crear_grafico_frecuencias_matplotlib(self, conteo_tipos, frecuencias_promedio, guardar_como):
        """Crea gráfico de frecuencias con matplotlib."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Gráfico de barras - Cantidad por tipo
        tipos = list(conteo_tipos.keys())
        cantidades = list(conteo_tipos.values())
        colores = [COLORES_ELEMENTOS.get(tipo, COLORES_ELEMENTOS['GENERAL']) for tipo in tipos]
        
        ax1.bar(tipos, cantidades, color=colores, alpha=0.7, edgecolor='black', linewidth=1)
        ax1.set_title('Cantidad de Samskaras por Tipo', fontweight='bold')
        ax1.set_ylabel('Número de Samskaras')
        ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico de violín - Distribución de frecuencias
        datos_violin = [frecuencias_promedio[tipo] for tipo in tipos]
        parts = ax2.violinplot(datos_violin, positions=range(len(tipos)), showmeans=True)
        
        for i, pc in enumerate(parts['bodies']):
            pc.set_facecolor(colores[i])
            pc.set_alpha(0.7)
        
        ax2.set_title('Distribución de Frecuencias por Tipo', fontweight='bold')
        ax2.set_ylabel('Frecuencia (%)')
        ax2.set_xticks(range(len(tipos)))
        ax2.set_xticklabels(tipos, rotation=45)
        
        plt.suptitle('Análisis de Samskaras Digitales - Distribución por Tipo', 
                    fontsize=16, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        if guardar_como:
            plt.savefig(guardar_como, dpi=300, bbox_inches='tight')
            print(f"Gráfico guardado como: {guardar_como}")
        
        plt.show()
        return fig
    
    def _crear_grafico_frecuencias_interactivo(self, conteo_tipos, frecuencias_promedio, guardar_como):
        """Crea gráfico interactivo de frecuencias con Plotly."""
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Cantidad de Samskaras por Tipo', 'Distribución de Frecuencias'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        tipos = list(conteo_tipos.keys())
        cantidades = list(conteo_tipos.values())
        colores = [COLORES_ELEMENTOS.get(tipo, COLORES_ELEMENTOS['GENERAL']) for tipo in tipos]
        
        # Gráfico de barras
        fig.add_trace(
            go.Bar(
                x=tipos, y=cantidades,
                marker_color=colores,
                name="Cantidad",
                text=cantidades,
                textposition="auto"
            ),
            row=1, col=1
        )
        
        # Box plots para distribución
        for i, tipo in enumerate(tipos):
            fig.add_trace(
                go.Box(
                    y=frecuencias_promedio[tipo],
                    name=tipo,
                    marker_color=colores[i],
                    boxmean=True
                ),
                row=1, col=2
            )
        
        fig.update_layout(
            title_text="Análisis de Samskaras Digitales - Distribución por Tipo",
            title_x=0.5,
            showlegend=False,
            height=500
        )
        
        if guardar_como:
            html_file = guardar_como.replace('.png', '.html') if guardar_como.endswith('.png') else f"{guardar_como}.html"
            pyo.plot(fig, filename=html_file, auto_open=False)
            print(f"Gráfico interactivo guardado como: {html_file}")
        
        fig.show()
        return fig
    
    def visualizar_evolucion_temporal(self, tipo_filtro=None, guardar_como=None, interactivo=False):
        """
        Visualiza la evolución temporal de samskaras.
        
        Args:
            tipo_filtro: Filtrar por tipo específico (opcional)
            guardar_como: Nombre del archivo para guardar (opcional)
            interactivo: Si True, genera visualización interactiva con Plotly
        """
        samskaras_filtrados = self.samskaras
        if tipo_filtro:
            samskaras_filtrados = [s for s in self.samskaras if s.tipo == tipo_filtro]
        
        if not samskaras_filtrados:
            print(f"No hay samskaras {'del tipo ' + tipo_filtro if tipo_filtro else ''} para visualizar evolución temporal.")
            return
        
        # Preparar datos temporales
        datos_temporales = self._preparar_datos_temporales(samskaras_filtrados)
        
        if interactivo:
            return self._crear_evolucion_temporal_interactiva(datos_temporales, tipo_filtro, guardar_como)
        else:
            return self._crear_evolucion_temporal_matplotlib(datos_temporales, tipo_filtro, guardar_como)
    
    def _preparar_datos_temporales(self, samskaras):
        """Prepara datos para visualización temporal."""
        datos_temporales = defaultdict(list)
        
        for samskara in samskaras:
            if samskara.primera_aparicion and samskara.ultima_aparicion:
                try:
                    fecha_inicio = datetime.fromisoformat(samskara.primera_aparicion.replace('Z', '+00:00'))
                    fecha_fin = datetime.fromisoformat(samskara.ultima_aparicion.replace('Z', '+00:00'))
                    
                    datos_temporales['fechas_inicio'].append(fecha_inicio)
                    datos_temporales['fechas_fin'].append(fecha_fin)
                    datos_temporales['patrones'].append(samskara.patron)
                    datos_temporales['tipos'].append(samskara.tipo)
                    datos_temporales['frecuencias'].append(samskara.frecuencia)
                except ValueError:
                    # Si las fechas no están en formato ISO, usar fechas por defecto
                    fecha_base = datetime.now()
                    datos_temporales['fechas_inicio'].append(fecha_base)
                    datos_temporales['fechas_fin'].append(fecha_base)
                    datos_temporales['patrones'].append(samskara.patron)
                    datos_temporales['tipos'].append(samskara.tipo)
                    datos_temporales['frecuencias'].append(samskara.frecuencia)
        
        return datos_temporales
    
    def _crear_evolucion_temporal_matplotlib(self, datos_temporales, tipo_filtro, guardar_como):
        """Crea gráfico de evolución temporal con matplotlib."""
        if not datos_temporales['fechas_inicio']:
            print("No hay datos temporales suficientes para crear la visualización.")
            return
        
        fig, ax = plt.subplots(figsize=(15, 8))
        
        # Crear líneas temporales para cada samskara
        for i, (inicio, fin, patron, tipo, freq) in enumerate(zip(
            datos_temporales['fechas_inicio'],
            datos_temporales['fechas_fin'],
            datos_temporales['patrones'],
            datos_temporales['tipos'],
            datos_temporales['frecuencias']
        )):
            color = COLORES_ELEMENTOS.get(tipo, COLORES_ELEMENTOS['GENERAL'])
            
            # Línea temporal
            ax.plot([inicio, fin], [i, i], color=color, linewidth=max(2, freq/10), 
                   alpha=0.7, solid_capstyle='round')
            
            # Puntos de inicio y fin
            ax.scatter([inicio, fin], [i, i], color=color, s=50, alpha=0.8, zorder=3)
            
            # Etiqueta del patrón (truncada si es muy larga)
            patron_corto = patron[:50] + '...' if len(patron) > 50 else patron
            ax.text(fin, i, f" {patron_corto}", va='center', fontsize=8, alpha=0.8)
        
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Samskaras')
        ax.set_title(f'Evolución Temporal de Samskaras{" - " + tipo_filtro if tipo_filtro else ""}', 
                    fontweight='bold')
        
        # Formatear eje temporal
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(datos_temporales['fechas_inicio'])//10)))
        plt.xticks(rotation=45)
        
        # Crear leyenda personalizada
        tipos_unicos = list(set(datos_temporales['tipos']))
        legend_elements = []
        for tipo in tipos_unicos:
            color = COLORES_ELEMENTOS.get(tipo, COLORES_ELEMENTOS['GENERAL'])
            legend_elements.append(plt.Line2D([0], [0], color=color, lw=3, label=tipo))
        
        ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1))
        
        plt.tight_layout()
        
        if guardar_como:
            plt.savefig(guardar_como, dpi=300, bbox_inches='tight')
            print(f"Evolución temporal guardada como: {guardar_como}")
        
        plt.show()
        return fig
    
    def _crear_evolucion_temporal_interactiva(self, datos_temporales, tipo_filtro, guardar_como):
        """Crea gráfico interactivo de evolución temporal con Plotly."""
        if not datos_temporales['fechas_inicio']:
            print("No hay datos temporales suficientes para crear la visualización.")
            return
        
        fig = go.Figure()
        
        # Agrupar por tipo para diferentes colores
        tipos_unicos = list(set(datos_temporales['tipos']))
        
        for tipo in tipos_unicos:
            indices_tipo = [i for i, t in enumerate(datos_temporales['tipos']) if t == tipo]
            color = COLORES_ELEMENTOS.get(tipo, COLORES_ELEMENTOS['GENERAL'])
            
            for idx in indices_tipo:
                inicio = datos_temporales['fechas_inicio'][idx]
                fin = datos_temporales['fechas_fin'][idx]
                patron = datos_temporales['patrones'][idx]
                freq = datos_temporales['frecuencias'][idx]
                
                # Línea temporal
                fig.add_trace(go.Scatter(
                    x=[inicio, fin],
                    y=[idx, idx],
                    mode='lines+markers',
                    line=dict(color=color, width=max(2, freq/5)),
                    marker=dict(size=8, color=color),
                    name=tipo if idx == indices_tipo[0] else "",
                    showlegend=idx == indices_tipo[0],
                    text=[f"Inicio: {patron}", f"Fin: {patron}"],
                    hovertemplate="<b>%{text}</b><br>Fecha: %{x}<br>Frecuencia: " + f"{freq:.1f}%<extra></extra>"
                ))
        
        fig.update_layout(
            title=f'Evolución Temporal de Samskaras{" - " + tipo_filtro if tipo_filtro else ""}',
            xaxis_title='Tiempo',
            yaxis_title='Samskaras',
            height=600,
            hovermode='closest'
        )
        
        if guardar_como:
            html_file = guardar_como.replace('.png', '.html') if guardar_como.endswith('.png') else f"{guardar_como}.html"
            pyo.plot(fig, filename=html_file, auto_open=False)
            print(f"Evolución temporal interactiva guardada como: {html_file}")
        
        fig.show()
        return fig
    
    def crear_mapa_calor_contextos(self, guardar_como=None, interactivo=False):
        """
        Crea mapa de calor mostrando la relación entre tipos de samskaras y contextos.
        
        Args:
            guardar_como: Nombre del archivo para guardar (opcional)
            interactivo: Si True, genera visualización interactiva con Plotly
        """
        if not self.samskaras:
            print("No hay samskaras para crear el mapa de calor.")
            return
        
        # Crear matriz de frecuencias por tipo y contexto
        contextos_por_tipo = defaultdict(lambda: defaultdict(int))
        
        for samskara in self.samskaras:
            for contexto in samskara.contextos:
                contextos_por_tipo[samskara.tipo][contexto] += samskara.frecuencia
        
        # Convertir a DataFrame para facilitar la visualización
        todos_contextos = set()
        for tipo_contextos in contextos_por_tipo.values():
            todos_contextos.update(tipo_contextos.keys())
        
        todos_tipos = list(contextos_por_tipo.keys())
        todos_contextos = list(todos_contextos)
        
        # Crear matriz
        matriz = np.zeros((len(todos_tipos), len(todos_contextos)))
        for i, tipo in enumerate(todos_tipos):
            for j, contexto in enumerate(todos_contextos):
                matriz[i, j] = contextos_por_tipo[tipo][contexto]
        
        if interactivo:
            return self._crear_mapa_calor_interactivo(matriz, todos_tipos, todos_contextos, guardar_como)
        else:
            return self._crear_mapa_calor_matplotlib(matriz, todos_tipos, todos_contextos, guardar_como)
    
    def _crear_mapa_calor_matplotlib(self, matriz, tipos, contextos, guardar_como):
        """Crea mapa de calor con matplotlib."""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Crear colormap personalizado
        colors = ['#f7f7f7', '#cccccc', '#969696', '#525252']
        n_bins = 100
        cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
        
        # Crear heatmap
        im = ax.imshow(matriz, cmap=cmap, aspect='auto')
        
        # Configurar ejes
        ax.set_xticks(np.arange(len(contextos)))
        ax.set_yticks(np.arange(len(tipos)))
        ax.set_xticklabels(contextos, rotation=45, ha="right")
        ax.set_yticklabels(tipos)
        
        # Agregar valores a las celdas
        for i in range(len(tipos)):
            for j in range(len(contextos)):
                if matriz[i, j] > 0:
                    text = ax.text(j, i, f'{matriz[i, j]:.1f}',
                                 ha="center", va="center", color="black", fontsize=8)
        
        ax.set_title("Mapa de Calor: Samskaras por Tipo y Contexto", fontweight='bold')
        ax.set_xlabel('Contextos')
        ax.set_ylabel('Tipos de Samskara')
        
        # Colorbar
        cbar = plt.colorbar(im)
        cbar.set_label('Frecuencia Acumulada (%)', rotation=270, labelpad=15)
        
        plt.tight_layout()
        
        if guardar_como:
            plt.savefig(guardar_como, dpi=300, bbox_inches='tight')
            print(f"Mapa de calor guardado como: {guardar_como}")
        
        plt.show()
        return fig
    
    def _crear_mapa_calor_interactivo(self, matriz, tipos, contextos, guardar_como):
        """Crea mapa de calor interactivo con Plotly."""
        fig = go.Figure(data=go.Heatmap(
            z=matriz,
            x=contextos,
            y=tipos,
            colorscale='Greys',
            hoverongaps=False,
            text=[[f'{val:.1f}%' if val > 0 else '' for val in fila] for fila in matriz],
            texttemplate="%{text}",
            textfont={"size": 10},
            hovertemplate='<b>Tipo:</b> %{y}<br><b>Contexto:</b> %{x}<br><b>Frecuencia:</b> %{z:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='Mapa de Calor: Samskaras por Tipo y Contexto',
            xaxis_title='Contextos',
            yaxis_title='Tipos de Samskara',
            width=800,
            height=500
        )
        
        if guardar_como:
            html_file = guardar_como.replace('.png', '.html') if guardar_como.endswith('.png') else f"{guardar_como}.html"
            pyo.plot(fig, filename=html_file, auto_open=False)
            print(f"Mapa de calor interactivo guardado como: {html_file}")
        
        fig.show()
        return fig
    
    def generar_dashboard_completo(self, guardar_como="dashboard_samskaras.html"):
        """
        Genera un dashboard completo combinando múltiples visualizaciones.
        
        Args:
            guardar_como: Nombre del archivo HTML para el dashboard
        """
        if not self.samskaras:
            print("No hay samskaras para generar el dashboard.")
            return
        
        # Crear subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distribución por Tipo', 'Evolución Temporal', 
                          'Frecuencias por Subtipo', 'Contextos Más Comunes'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "bar"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Distribución por tipo
        conteo_tipos = Counter([s.tipo for s in self.samskaras])
        tipos = list(conteo_tipos.keys())
        cantidades = list(conteo_tipos.values())
        colores = [COLORES_ELEMENTOS.get(tipo, COLORES_ELEMENTOS['GENERAL']) for tipo en tipos]
        
        fig.add_trace(
            go.Bar(x=tipos, y=cantidades, marker_color=colores, name="Por Tipo"),
            row=1, col=1
        )
        
        # 2. Evolución temporal (simplificada)
        fechas_creacion = []
        for samskara in self.samskaras:
            if samskara.primera_aparicion:
                try:
                    fecha = datetime.fromisoformat(samskara.primera_aparicion.replace('Z', '+00:00'))
                    fechas_creacion.append(fecha)
                except ValueError:
                    fechas_creacion.append(datetime.now())
            else:
                fechas_creacion.append(datetime.now())
        
        # Contar samskaras por día
        conteo_diario = Counter([fecha.date() for fecha in fechas_creacion])
        fechas_ordenadas = sorted(conteo_diario.keys())
        conteos_ordenados = [conteo_diario[fecha] for fecha in fechas_ordenadas]
        
        fig.add_trace(
            go.Scatter(x=fechas_ordenadas, y=conteos_ordenados, mode='lines+markers',
                      name="Creación por día", line=dict(color=COLORES_ELEMENTOS['EVOLUCION'])),
            row=1, col=2
        )
        
        # 3. Frecuencias por subtipo (top 10)
        conteo_subtipos = Counter([f"{s.tipo}/{s.subtipo}" for s in self.samskaras])
        top_subtipos = conteo_subtipos.most_common(10)
        subtipos, conteos_sub = zip(*top_subtipos) if top_subtipos else ([], [])
        
        fig.add_trace(
            go.Bar(x=list(subtipos), y=list(conteos_sub), 
                  marker_color=COLORES_ELEMENTOS['GENERAL'], name="Por Subtipo"),
            row=2, col=1
        )
        
        # 4. Contextos más comunes
        todos_contextos = []
        for samskara in self.samskaras:
            todos_contextos.extend(samskara.contextos)
        
        conteo_contextos = Counter(todos_contextos)
        top_contextos = conteo_contextos.most_common(8)
        contextos, conteos_ctx = zip(*top_contextos) if top_contextos else ([], [])
        
        fig.add_trace(
            go.Bar(x=list(contextos), y=list(conteos_ctx),
                  marker_color=COLORES_ELEMENTOS['CONCEPTUAL'], name="Contextos"),
            row=2, col=2
        )
        
        # Configurar layout
        fig.update_layout(
            height=800,
            title_text="Dashboard de Samskaras Digitales - Análisis Integral",
            title_x=0.5,
            showlegend=False
        )
        
        # Rotar etiquetas donde sea necesario
        fig.update_xaxes(tickangle=45, row=2, col=1)
        fig.update_xaxes(tickangle=45, row=2, col=2)
        
        # Guardar dashboard
        pyo.plot(fig, filename=guardar_como, auto_open=False)
        print(f"Dashboard completo guardado como: {guardar_como}")
        
        fig.show()
        return fig


# Función de demostración
def demo():
    """Ejecuta una demostración del visualizador."""
    # Importar y crear datos de ejemplo
    from analisis_samskaras.analizador_patrones import demo as crear_analizador_demo
    
    print("Creando datos de ejemplo...")
    analizador = crear_analizador_demo()
    
    print("Inicializando visualizador...")
    visualizador = VisualizadorSamskaras(analizador=analizador)
    
    print("Generando visualizaciones...")
    
    # 1. Frecuencias por tipo
    print("1. Visualización de frecuencias por tipo...")
    visualizador.visualizar_frecuencias_por_tipo(
        guardar_como="frecuencias_samskaras.html", 
        interactivo=True
    )
    
    # 2. Mapa de calor de contextos
    print("2. Mapa de calor de contextos...")
    visualizador.crear_mapa_calor_contextos(
        guardar_como="mapa_calor_contextos.html",
        interactivo=True
    )
    
    # 3. Dashboard completo
    print("3. Dashboard completo...")
    visualizador.generar_dashboard_completo("dashboard_completo.html")
    
    print("Demostración completada. Revisa los archivos HTML generados.")
    return visualizador


if __name__ == "__main__":
    print("Iniciando demostración del Visualizador de Samskaras Digitales...")
    visualizador = demo()
