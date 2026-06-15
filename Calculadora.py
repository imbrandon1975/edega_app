import streamlit as st
import pandas as pd
import plotly.express as px
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
    st.subheader("🛠️ Configuración de precio")
    
    # Base: Costo del producto
    costo = st.number_input("Costo por unidad ($)", min_value=0.0, max_value=20000.0, value=500.0, step=100.0)
    
    st.write("---")
    # Selector de modalidad para definir el precio
    modo_precio = st.radio(
        "Definir precio mediante:",
        ["Precio de venta manual", "Margen de ganancia (%) sobre costo"],
        horizontal=False
    )
    
    # Lógica dinámica según la selección del usuario
    if modo_precio == "Precio de venta manual":
        precio = st.number_input("Precio de venta sugerido ($)", min_value=0.0, max_value=20000.0, value=1200.0, step=100.0)
        # Calcular el margen resultante para mostrarlo informativamente
        if costo > 0:
            margen_calculado = ((precio - costo) / costo) * 100
            st.info(f"Margen obtenido: {margen_calculado:.1f}% sobre el costo.")
    else:
        margen_porcentaje = st.number_input("Margen deseado (%)", min_value=0.0, max_value=1000.0, value=140.0, step=5.0)
        # Calcular el precio automáticamente con base en el costo y el margen %
        precio = costo * (1 + (margen_porcentaje / 100))
        st.success(f"Precio calculado automáticamente: ${precio:,.2f}")
    
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
        st.subheader("📊 Resultados de tu Proyección")
        
        # Definición de los escenarios de unidades
        unidades = [10, 30, 50, 100, 200, 300]
        
        # Generar el DataFrame base
        df = pd.DataFrame({
            "Unidades": [str(u) for u in unidades],
            "Utilidad Base": [u * utilidad_unitaria for u in unidades]
        })
        
        # Calcular las proyecciones según la temporalidad seleccionada
        if temporalidad == "Semanal":
            df["Proyección Semanal"] = df["Utilidad Base"]
            df["Proyección Mensual"] = df["Utilidad Base"] * 4
            df["Proyección Anual"] = df["Utilidad Base"] * 52
            y_column = "Proyección Semanal"
        elif temporalidad == "Mensual":
            df["Proyección Mensual"] = df["Utilidad Base"]
            df["Proyección Anual"] = df["Utilidad Base"] * 12
            y_column = "Proyección Mensual"
        else: # Anual
            df["Proyección Anual"] = df["Utilidad Base"]
            y_column = "Proyección Anual"
            
        # Formateo de la tabla para visualización limpia
        df_display = df.copy()
        columnas_moneda = [col for col in df_display.columns if "Proyección" in col]
        for col in columnas_moneda:
            df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}")
            
        # Mostrar la tabla de datos numéricos
        st.dataframe(df_display.drop(columns=["Utilidad Base"]), hide_index=True, use_container_width=True)
        
        st.divider()
        
        # Gráfico interactivo con Plotly (Barras con colores corporativos)
        st.markdown(f"#### Comportamiento de tu Utilidad ({temporalidad})")
        
        paleta_edega = ["#0E5EB9", "#878787", "#0D2C41", "#DADADA", "#7B7B7B"]
        
        fig = px.bar(
            df,
            x="Unidades",
            y=y_column,
            text=y_column,
            labels={"Unidades": "Unidades Vendidas", y_column: f"Utilidad {temporalidad} ($)"},
            color="Unidades",
            color_discrete_sequence=paleta_edega
        )
        
        fig.update_layout(
            xaxis=dict(type='category'),
            uniformtext_minsize=8, 
            uniformtext_mode='hide', 
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        
        fig.update_traces(texttemplate='$%{text:,.2s}', textposition='outside')
        
        st.plotly_chart(fig, use_container_width=True)
