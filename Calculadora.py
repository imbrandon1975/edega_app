import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import os

# Configuración de la página en modo ancho (horizontal)
st.set_page_config(page_title="Calculadora de Proyección de Ventas", layout="wide")

# --- ENCABEZADO CON LOGO DE FORMA HORIZONTAL ---
ruta_logo = "edega logo.png"

col_logo, col_titulo = st.columns([1, 7])

with col_logo:
    if os.path.exists(ruta_logo):
        imagen = Image.open(ruta_logo)
        st.image(imagen, use_container_width=True)
    else:
        st.caption("⚠️ Logo no encontrado")

with col_titulo:
    st.title("📈 Proyecta tu Crecimiento")
    st.markdown("### Descubre tu potencial de ganancia distribuyendo nuestros productos.")
    st.write("Ajusta los valores a la izquierda para ver inmediatamente tus proyecciones a la derecha.")

st.divider()

# --- DISEÑO HORIZONTAL DE LA CALCULADORA ---
col_izquierda, col_derecha = st.columns([1, 2], gap="large")

# --- COLUMNA IZQUIERDA: Controles e Inputs ---
with col_izquierda:
    st.subheader("🛠️ Configuración de utilidad")
    
    # Base: Costo del producto
    costo = st.number_input("Costo por unidad ($)", min_value=0.0, max_value=20000.0, value=1625.0, step=100.0)
    
    st.write("---")
    # Selector de modalidad para definir el precio
    modo_precio = st.radio(
        "Definir precio mediante:",
        ["Precio Publico manual", "Margen de ganancia (%) sobre costo"],
        horizontal=False
    )
    
    # Lógica dinámica según la selección del usuario
    if modo_precio == "Precio Publico manual":
        precio = st.number_input("Precio Publico Sugerido ($)", min_value=0.0, max_value=20000.0, value=3250.0, step=100.0)
        if costo > 0:
            margen_calculado = ((precio - costo) / costo) * 100
            st.info(f"Margen obtenido: {margen_calculado:.1f}% sobre el costo.")
    else:
        margen_porcentaje = st.number_input("Margen deseado (%)", min_value=0.0, max_value=1000.0, value=100.0, step=5.0)
        precio = costo * (1 + (margen_porcentaje / 100))
        st.success(f"Precio calculated automáticamente: ${precio:,.2f}")
    
    st.write("---")
    
    # Cálculo de la utilidad unitaria final
    utilidad_unitaria = precio - costo
    st.metric(label="Utilidad neta por unidad", value=f"${utilidad_unitaria:,.2f}")
    
    st.divider()
    
    temporalidad = st.radio(
        "Si logras vender este volumen de forma...",
        ["Semanal", "Mensual", "Anual"],
        horizontal=False
    )

# --- COLUMNA DERECHA: Resultados numéricos y Gráfico ---
with col_derecha:
    if utilidad_unitaria <= 0:
        st.error("El precio de venta debe ser mayor al costo para generar utilidad. Ajusta los valores en el panel izquierdo.")
    else:
        st.subheader("📊 Proyección de Utilidades")
        
        # Definición de los escenarios de unidades
        unidades = [10, 30, 50, 100, 200, 300]
        
        # 1. Generar DataFrame con la utilidad base por el volumen vendido
        df = pd.DataFrame({
            "Unidades": [str(u) for u in unidades],
            "Utilidad Base": [u * utilidad_unitaria for u in unidades]
        })
        
        # 2. LÓGICA CORREGIDA: Calcular TODAS las columnas de forma matemática absoluta
        df["Proyección Semanal"] = df["Utilidad Base"]
        df["Proyección Mensual"] = df["Utilidad Base"] * 4
        df["Proyección Anual"] = df["Utilidad Base"] * 52
        
        # 3. Asignar la columna activa según el switch del usuario
        if temporalidad == "Semanal":
            y_column = "Proyección Semanal"
        elif temporalidad == "Mensual":
            y_column = "Proyección Mensual"
        else:
            y_column = "Proyección Anual"
            
        # Extraemos los valores numéricos correctos y escalados para Plotly
        valores_actuales = df[y_column].tolist()
        
        # Formateo de la tabla nativa para visualización limpia en pantalla
        df_display = df.copy()
        df_display = df_display.drop(columns=["Utilidad Base"])
        columnas_moneda = ["Proyección Semanal", "Proyección Mensual", "Proyección Anual"]
        for col in columnas_moneda:
            df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}")
            
        # Mostrar la tabla estándar de Streamlit
        st.dataframe(df_display, hide_index=True, use_container_width=True)
        
        st.divider()
        
        # --- SELECTOR DE TIPO DE GRÁFICO ---
        tipo_grafico = st.selectbox(
            "Visualización estratégica del gráfico:",
            [
                "Gráfico de Cascada (Ganancia Acumulada)", 
                "Gráfico de Barras", 
                "Gráfico de Área (Crecimiento Orgánico)"
            ],
            index=0
        )
        
        st.markdown(f"#### Comportamiento de tu Utilidad ({temporalidad})")
        
        # PALETA CORPORATIVA (Priorizando el azul de Edega)
        color_edega_azul = "#0E5EB9"      # Azul Principal Edega
        color_edega_oscuro = "#0D2C41"    # Azul Oscuro
        color_edega_gris = "#878787"      # Gris
        color_edega_carbon = "#333333"    # Carbón
        
        paleta_priorizada = [
            color_edega_azul,
            color_edega_oscuro,
            color_edega_azul,
            color_edega_gris,
            color_edega_azul,
            color_edega_carbon
        ]
        
        fig = go.Figure()
        
        # OP-1: GRÁFICO DE CASCADA (Calculado dinámicamente con valores_actuales)
        if tipo_grafico == "Gráfico de Cascada (Ganancia Acumulada)":
            valores_cascada = []
            for i in range(len(valores_actuales)):
                if i == 0:
                    valores_cascada.append(valores_actuales[i])
                else:
                    valores_cascada.append(valores_actuales[i] - valores_actuales[i-1])
            
            fig.add_trace(go.Waterfall(
                name="Incremento",
                orientation="v",
                measure=["relative"] * len(df),
                x=df["Unidades"],
                textposition="outside",
                text=valores_actuales, 
                texttemplate='$%{text:,.2s}',
                y=valores_cascada,
                increasing=dict(marker=dict(color=color_edega_azul)),
                connector=dict(line=dict(color=color_edega_gris, width=1, dash="dot"))
            ))
            fig.update_layout(
                xaxis=dict(type='category', title="Escalas de Unidades"),
                yaxis=dict(title=f"Utilidad Acumulada {temporalidad} ($)"),
                margin=dict(t=20, b=20, l=20, r=20),
                showlegend=False
            )

        # OP-2: GRÁFICO DE BARRAS ORIGINAL
        elif tipo_grafico == "Gráfico de Barras":
            fig.add_trace(go.Bar(
                x=df["Unidades"],
                y=valores_actuales,
                text=valores_actuales,
                texttemplate='$%{text:,.2s}',
                textposition='outside',
                marker_color=paleta_priorizada[:len(df)]
            ))
            fig.update_layout(
                xaxis=dict(type='category', title="Unidades Vendidas"),
                yaxis=dict(title=f"Utilidad {temporalidad} ($)", showgrid=True),
                margin=dict(t=20, b=20, l=20, r=20),
                showlegend=False
            )

        # OP-3: GRÁFICO DE ÁREA ACUMULADA
        else:
            fig.add_trace(go.Scatter(
                x=df["Unidades"],
                y=valores_actuales,
                mode='lines+markers+text',
                text=valores_actuales,
                texttemplate='$%{text:,.2s}',
                textposition='top center',
                fill='tozeroy', 
                fillcolor='rgba(14, 94, 185, 0.25)', 
                line=dict(color=color_edega_azul, width=4), 
                marker=dict(size=10, color=color_edega_oscuro)
            ))
            fig.update_layout(
                xaxis=dict(type='category', title="Unidades Vendidas"),
                yaxis=dict(title=f"Progreso de Utilidad {temporalidad} ($)", showgrid=True),
                margin=dict(t=30, b=20, l=20, r=20),
                showlegend=False
            )
        
        # Renderizado final con la clave dinámica para limpiar la caché visual
        st.plotly_chart(fig, use_container_width=True, key=f"grafico_{temporalidad}_{tipo_grafico}")
