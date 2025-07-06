
import streamlit as st
import pandas as pd
import openai
from datetime import datetime
import os

st.set_page_config(page_title="Gerador de Prompts com IA", layout="centered")

# Estilo claro e moderno
st.markdown("""
    <style>
        body, .stApp {
            background-color: #f5f7fa;
            color: #000000;
            font-family: 'Segoe UI', sans-serif;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            border: 1px solid #cccccc;
        }
    </style>
""", unsafe_allow_html=True)

st.title("✨ Gerador de Prompts com IA")
st.markdown("Preencha os campos, escolha o tipo de vídeo e gere automaticamente um prompt criativo com ou sem inteligência artificial.")

# 🔐 Campo para colar API Key (opcional)
api_key = st.text_input("🔑 API Key da OpenAI (opcional para usar IA):", type="password")

# Tipos de vídeo
tipos = {
    "Fusão de Personagens": ["Personagem 1", "Personagem 2", "Ambiente"],
    "Estilo Bíblico": ["Personagem", "Ação", "Emoção"],
    "Estilo Científico": ["Assunto", "Estilo Visual", "Paleta de Cores"],
    "Estilo Podcast": ["Tema", "Convidado", "Tom da conversa"],
    "Estilo Vlog POV": ["Ação", "Local", "Sensação"],
    "Comercial de Produto": ["Produto", "Público-alvo", "Estilo visual"],
    "Motivacional": ["Mensagem central", "Tom", "Cenário"],
    "Educacional": ["Tema", "Público-alvo", "Formato"],
    "Infantil": ["Personagem", "História", "Ambiente"],
    "Curta Animado": ["Enredo", "Estilo gráfico", "Mensagem"],
    "Bíblico Apocalíptico": ["Profecia", "Ambiente", "Mensagem"],
    "Científico Fantástico": ["Experimento", "Personagem", "Resultado"],
    "Comédia Criativa": ["Situação", "Personagem", "Reviravolta"],
    "Estilo Documentário": ["Tema", "Época", "Narrador"]
}

tipo_escolhido = st.selectbox("🎞️ Tipo de vídeo:", list(tipos.keys()))
campos = tipos[tipo_escolhido]
entradas = [st.text_input(campo) for campo in campos]
extra = st.text_input("📝 Extra (opcional):")
usar_ia = st.checkbox("Usar IA para gerar o prompt")

# Geração manual (fallback)
def gerar_prompt_manual(tipo, campos, extra):
    if tipo == "Fusão de Personagens":
        return f"A fusion between {campos[0]} and {campos[1]} in a {campos[2]} environment. {extra}"
    elif tipo == "Estilo Bíblico":
        return f"A biblical scene of {campos[0]} {campos[1]}, in a {campos[2]} mood. {extra}"
    elif tipo == "Estilo Científico":
        return f"A scientific visual of {campos[0]}, in {campos[1]} style, using a {campos[2]} color palette. {extra}"
    elif tipo == "Estilo Podcast":
        return f"A podcast scene about {campos[0]} with a {campos[1]}, in a {campos[2]} tone. {extra}"
    elif tipo == "Estilo Vlog POV":
        return f"A first-person POV video of {campos[0]} in a {campos[1]} setting, feeling {campos[2]}. {extra}"
    elif tipo == "Comercial de Produto":
        return f"A commercial showcasing {campos[0]} for {campos[1]}, in a {campos[2]} visual style. {extra}"
    elif tipo == "Motivacional":
        return f"A motivational message: '{campos[0]}' in a {campos[1]} tone, set in a {campos[2]} scene. {extra}"
    elif tipo == "Educacional":
        return f"An educational video about {campos[0]} for {campos[1]}, presented in a {campos[2]} format. {extra}"
    elif tipo == "Infantil":
        return f"A children's story about {campos[0]}, where {campos[1]} happens in a {campos[2]} setting. {extra}"
    elif tipo == "Curta Animado":
        return f"An animated short featuring {campos[0]}, drawn in {campos[1]} style, conveying the message: {campos[2]}. {extra}"
    elif tipo == "Bíblico Apocalíptico":
        return f"A biblical apocalyptic scene portraying {campos[0]} in a {campos[1]} setting. Message: {campos[2]}. {extra}"
    elif tipo == "Científico Fantástico":
        return f"A fantastic experiment where {campos[0]} meets {campos[1]}, resulting in {campos[2]}. {extra}"
    elif tipo == "Comédia Criativa":
        return f"A funny situation: {campos[0]}, featuring {campos[1]}, ending with {campos[2]}. {extra}"
    elif tipo == "Estilo Documentário":
        return f"A documentary about {campos[0]}, set in {campos[1]}, narrated by {campos[2]}. {extra}"
    else:
        return "Tipo não encontrado."

# IA com OpenAI
def gerar_com_openai(prompt_base):
    openai.api_key = api_key
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um gerador de prompts criativos para vídeos."},
            {"role": "user", "content": prompt_base}
        ],
        temperature=0.8,
        max_tokens=300
    )
    return resposta['choices'][0]['message']['content'].strip()

# Botão para gerar
if st.button("🚀 Gerar Prompt"):
    if all(entradas):
        prompt_base = f"Crie um prompt criativo para um vídeo do tipo '{tipo_escolhido}' com os seguintes elementos: " + ", ".join(entradas)
        if extra:
            prompt_base += f". Extra: {extra}"

        try:
            if usar_ia and api_key:
                prompt = gerar_com_openai(prompt_base)
                st.success("✅ Prompt gerado com IA!")
            else:
                prompt = gerar_prompt_manual(tipo_escolhido, entradas, extra)
                st.success("✅ Prompt gerado manualmente!")
        except Exception as e:
            prompt = gerar_prompt_manual(tipo_escolhido, entradas, extra)
            st.warning(f"⚠️ Erro com IA, usando versão manual: {e}")

        st.text_area("📋 Prompt gerado:", prompt, height=200)
        st.markdown(f'<button onclick="navigator.clipboard.writeText('{prompt}')" style="padding:8px 16px; margin-top:10px;">📋 Copiar Prompt</button>', unsafe_allow_html=True)

        # Salvar no histórico Excel
        df = pd.DataFrame([{
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Tipo": tipo_escolhido,
            "Campos": ", ".join(entradas),
            "Extra": extra,
            "Usou IA": "Sim" if usar_ia and api_key else "Não",
            "Prompt": prompt
        }])
        historico_path = "historico_prompts.xlsx"
        if os.path.exists(historico_path):
            df_existente = pd.read_excel(historico_path)
            df = pd.concat([df_existente, df], ignore_index=True)
        df.to_excel(historico_path, index=False)
        st.info("💾 Prompt salvo em 'historico_prompts.xlsx'")
    else:
        st.warning("⚠️ Preencha todos os campos obrigatórios.")
