import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import os

# Configuración de la página en modo ancho (horizontal) con márgenes nativos
st.set_page_config(page_title="Calculadora de Proyección Multi-Producto Edega", layout="wide")

# --- ENCABEZADO CON LOGO Y TÍTULOS ORIGINALES ---
ruta_logo = "edega logo.png"
col_logo, col_titulo = st.columns([1, 7])

with col_logo:
    if os.path.exists(ruta_logo):
        imagen = Image.open(ruta_logo)
        st.image(imagen)  # Removido el límite de ancho forzado
    else:
        st.caption("⚠️ Logo no encontrado")

with col_titulo:
    st.title("📊 Proyecta tu Crecimiento")
    st.markdown("### Descubre tu potencial de ganancia distribuyendo nuestros productos.")
    st.write("Ajusta los valores a la izquierda para ver inmediatamente tus proyecciones a la derecha.")

st.divider()

# --- DISEÑO HORIZONTAL DE LA CALCULADORA ---
col_izquierda, col_derecha = st.columns([1, 2], gap="large")

# Definición global de los escenarios de unidades
unidades = [10, 30, 50, 100, 200, 300]

# --- COLUMNA IZQUIERDA: Configuración de los 5 Productos ---
with col_izquierda:
    st.markdown("## 🛠️ Configuración")
    
    # Creación de las 5 pestañas para los productos
    tab_llantas, tab_mecanica, tab_premium, tab_movpro, tab_gap = st.tabs([
        "🛞 Llantas", "🔧 Mecánica", "🚗  Premium", "📱 Mov Pro", "🛡️ GAP"
    ])
    
    # --- 1. LLANTAS ---
    with tab_llantas:
        st.markdown("### Configuración de Llantas")
        activa_llantas = st.checkbox("Incluir Llantas", value=True, key="act_llantas")
        if activa_llantas:
            c_llantas = st.number_input("Costo por unidad ($)", min_value=0.0, value=1625.0, step=100.0, key="c_ll")
            modo_ll = st.radio("Definir precio mediante:", ["Precio Publico manual", "Margen de ganancia (%) sobre costo"], horizontal=False, key="m_ll")
            
            if modo_ll == "Precio Publico manual":
                p_llantas = st.number_input("Precio Publico Sugerido ($)", min_value=0.0, value=3250.0, step=100.0, key="p_ll")
                if c_llantas > 0:
                    margen_calc = ((p_llantas - c_llantas) / c_llantas) * 100
                    st.info(f"Margen obtenido: {margen_calc:.1f}% sobre el costo.")
            else:
                m_ll = st.number_input("Margen deseado (%)", min_value=0.0, value=50.0, step=5.0, key="mg_ll")
                p_llantas = c_llantas * (1 + (m_ll / 100))
                st.success(f"Precio calculado automáticamente: ${p_llantas:,.2f}")
                
            ut_llantas = max(0.0, p_llantas - c_llantas)
            st.metric("Utilidad neta por unidad", f"${ut_llantas:,.2f}")
        else:
            ut_llantas = 0.0

    # --- 2. MECÁNICA ---
    with tab_mecanica:
        st.markdown("### Configuración de Mecánica")
        activa_mecanica = st.checkbox("Incluir Mecánica", value=False, key="act_mec")
        if activa_mecanica:
            c_mecanica = st.number_input("Costo por unidad ($)", min_value=0.0, value=3725.0, step=50.0, key="c_me")
            modo_me = st.radio("Definir precio mediante:", ["Precio Publico manual", "Margen de ganancia (%) sobre costo"], horizontal=False, key="m_me")
            
            if modo_me == "Precio Publico manual":
                p_mecanica = st.number_input("Precio Publico Sugerido ($)", min_value=0.0, value=7450.0, step=50.0, key="p_me")
                if c_mecanica > 0:
                    margen_calc = ((p_mecanica - c_mecanica) / c_mecanica) * 100
                    st.info(f"Margen obtenido: {margen_calc:.1f}% sobre el costo.")
            else:
                m_me = st.number_input("Margen deseado (%)", min_value=0.0, value=125.0, step=5.0, key="mg_me")
                p_mecanica = c_mecanica * (1 + (m_me / 100))
                st.success(f"Precio calculado automáticamente: ${p_mecanica:,.2f}")
                
            ut_mecanica = max(0.0, p_mecanica - c_mecanica)
            st.metric("Utilidad neta por unidad", f"${ut_mecanica:,.2f}")
        else:
            ut_mecanica = 0.0

    # --- 3. PREMIUM ---
    with tab_premium:
        st.markdown("### Configuración de Premium")
        activa_premium = st.checkbox("Incluir Premium", value=False, key="act_prem")
        if activa_premium:
            c_premium = st.number_input("Costo por unidad ($)", min_value=0.0, value=2175.0, step=200.0, key="c_pr")
            modo_pr = st.radio("Definir precio mediante:", ["Precio Publico manual", "Margen de ganancia (%) sobre costo"], horizontal=False, key="m_pr")
            
            if modo_pr == "Precio Publico manual":
                p_premium = st.number_input("Precio Publico Sugerido ($)", min_value=0.0, value=4350.0, step=200.0, key="p_pr")
                if c_premium > 0:
                    margen_calc = ((p_premium - c_premium) / c_premium) * 100
                    st.info(f"Margen obtenido: {margen_calc:.1f}% sobre el costo.")
            else:
                m_pr = st.number_input("Margen deseado (%)", min_value=0.0, value=75.0, step=5.0, key="mg_pr")
                p_premium = c_premium * (1 + (m_pr / 100))
                st.success(f"Precio calculated automáticamente: ${p_premium:,.2f}")
                
            ut_premium = max(0.0, p_premium - c_premium)
            st.metric("Utilidad neta por unidad", f"${ut_premium:,.2f}")
        else:
            ut_premium = 0.0

    # --- 4. MOV PRO ---
    with tab_movpro:
        st.markdown("### Configuración de Mov Pro")
        activa_movpro = st.checkbox("Incluir Mov Pro", value=False, key="act_mov")
        if activa_movpro:
            c_movpro = st.number_input("Costo por unidad ($)", min_value=0.0, value=1275.0, step=50.0, key="c_mo")
            modo_mo = st.radio("Definir precio mediante:", ["Precio Publico manual", "Margen de ganancia (%) sobre costo"], horizontal=False, key="m_mo")
            
            if modo_mo == "Precio Publico manual":
                p_movpro = st.number_input("Precio Publico Sugerido ($)", min_value=0.0, value=2750.0, step=50.0, key="p_mo")
                if c_movpro > 0:
                    margen_calc = ((p_movpro - c_movpro) / c_movpro) * 100
                    st.info(f"Margen obtenido: {margen_calc:.1f}% sobre el costo.")
            else:
                m_mo = st.number_input("Margen deseado (%)", min_value=0.0, value=83.3, step=5.0, key="mg_mo")
                p_movpro = c_movpro * (1 + (m_mo / 100))
                st.success(f"Precio calculated automáticamente: ${p_movpro:,.2f}")
                
            ut_movpro = max(0.0, p_movpro - c_movpro)
            st.metric("Utilidad neta por unidad", f"${ut_movpro:,.2f}")
        else:
            ut_movpro = 0.0

    # --- 5. GAP ---
    with tab_gap:
        st.markdown("### Configuración de GAP")
        activa_gap = st.checkbox("Incluir GAP", value=False, key="act_gap")
        if activa_gap:
            c_gap = st.number_input("Costo por unidad ($)", min_value=0.0, value=3735.0, step=50.0, key="c_ga")
            modo_ga = st.radio("Definir precio mediante:", ["Precio Publico manual", "Margen de ganancia (%) sobre costo"], horizontal=False, key="m_ga")
            
            if modo_ga == "Precio Publico manual":
                p_gap = st.number_input("Precio Publico Sugerido ($)", min_value=0.0, value=7450.0, step=50.0, key="p_ga")
                if c_gap > 0:
                    margen_calc = ((p_gap - c_gap) / c_gap) * 100
                    st.info(f"Margen obtenido: {margen_calc:.1f}% sobre el costo.")
            else:
                m_ga = st.number_input("Margen deseado (%)", min_value=0.0, value=133.3, step=5.0, key="mg_ga")
                p_gap = c_gap * (1 + (m_ga / 100))
                st.success(f"Precio calculated automáticamente: ${p_gap:,.2f}")
                
            ut_gap = max(0.0, p_gap - c_gap)
            st.metric("Utilidad neta por unidad", f"${ut_gap:,.2f}")
        else:
            ut_gap = 0.0

    st.write("---")
    temporalidad = st.radio("Si logras vender este volumen de forma...", ["Semanal", "Mensual", "Anual"], horizontal=True)

# --- COLUMNA DERECHA: Resultados Consolidados (Suma Total) ---
with col_derecha:
    utilidad_combinada_total = ut_llantas + ut_mecanica + ut_premium + ut_movpro + ut_gap
    
    st.markdown("## 📊 Proyección de Utilidades")
    
    # DataFrame Maestro con volúmenes basados en la suma total
    df = pd.DataFrame({"Unidades": [str(u) for u in unidades]})
    
    df["Proyección Semanal"] = [u * utilidad_combinada_total for u in unidades]
    df["Proyección Mensual"] = [u * utilidad_combinada_total * 4 for u in unidades]
    df["Proyección Anual"] = [u * utilidad_combinada_total * 52 for u in unidades]
    
    if temporalidad == "Semanal":
        y_column = "Proyección Semanal"
    elif temporalidad == "Mensual":
        y_column = "Proyección Mensual"
    else:
        y_column = "Proyección Anual"
        
    valores_actuales = df[y_column].tolist()
    
    # Formateo visual estricto para la tabla
    df_display = df.copy()
    for col in ["Proyección Semanal", "Proyección Mensual", "Proyección Anual"]:
        df_display[col] = df_display[col].apply(lambda x: f"${x:,.2f}")
        
    st.dataframe(df_display, hide_index=True, use_container_width=True)
    st.divider()
    
    # --- SELECTOR DE TIPO DE GRÁFICO ---
    tipo_grafico = st.selectbox(
        "Visualización estratégica:",
        [
            "Gráfico de Cascada (Ganancia Acumulada)", 
            "Gráfico de Barras Original", 
            "Gráfico de Pirámide (Metas de Distribución)", 
            "Gráfico de Área (Crecimiento Orgánico)"
        ], index=0
    )
    
    # Paleta Corporativa Edega
    color_edega_azul = "#0E5EB9"
    color_edega_oscuro = "#0D2C41"
    color_edega_gris = "#878787"
    color_edega_carbon = "#333333"
    paleta_priorizada = [color_edega_azul, color_edega_oscuro, color_edega_azul, color_edega_gris, color_edega_azul, color_edega_carbon]
    
    fig = go.Figure()
    
    # OP-1: GRÁFICO DE CASCADA
    if tipo_grafico == "Gráfico de Cascada (Ganancia Acumulada)":
        valores_cascada = []
        for i in range(len(valores_actuales)):
            if i == 0:
                valores_cascada.append(valores_actuales[i])
            else:
                valores_cascada.append(valores_actuales[i] - valores_actuales[i-1])
        
        fig.add_trace(go.Waterfall(
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
            yaxis=dict(title="Utilidad Acumulada ($)"),
        )

    # OP-2: GRÁFICO DE BARRAS ORIGINAL
    elif tipo_grafico == "Gráfico de Barras Original":
        fig.add_trace(go.Bar(
            x=df["Unidades"], y=valores_actuales,
            text=valores_actuales, texttemplate='$%{text:,.2s}',
            textposition='outside', marker_color=paleta_priorizada[:len(df)]
        ))
        fig.update_layout(
            xaxis=dict(type='category', title="Unidades Vendidas"),
            yaxis=dict(title="Utilidad ($)", showgrid=True),
        )

    # OP-3: GRÁFICO DE PIRÁMIDE (FUNNEL)
    elif tipo_grafico == "Gráfico de Pirámide (Metas de Distribución)":
        fig.add_trace(go.Funnel(
            y=df["Unidades"], x=valores_actuales,
            textinfo="value", texttemplate='$%{value:,.2s}',
            marker=dict(color=paleta_priorizada[:len(df)])
        ))
        fig.update_layout(
            yaxis=dict(title="Nivel por Unidades"),
            xaxis=dict(title="Utilidad ($)"),
        )

    # OP-4: GRÁFICO DE ÁREA ACUMULADA
    else:
        fig.add_trace(go.Scatter(
            x=df["Unidades"], y=valores_actuales,
            mode='lines+markers+text', text=valores_actuales,
            texttemplate='$%{text:,.2s}', textposition='top center',
            fill='tozeroy', fillcolor='rgba(14, 94, 185, 0.25)', 
            line=dict(color=color_edega_azul, width=4), 
            marker=dict(size=8, color=color_edega_oscuro)
        ))
        fig.update_layout(
            xaxis=dict(type='category', title="Unidades Vendidas"),
            yaxis=dict(title="Utilidad ($)", showgrid=True),
        )
    
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True, key=f"grafico_{temporalidad}_{tipo_grafico}")
