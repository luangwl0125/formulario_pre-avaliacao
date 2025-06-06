...import streamlit as st
from docx import Document
import smtplib
from email.message import EmailMessage
import os

st.set_page_config(page_title="Pré-Avaliação Neuropsicológica - Adulto", page_icon="🧠")
st.title("Formulário de Pré-Avaliação Neuropsicológica - Adulto")

st.markdown("**Finalidade:** Este questionário tem por objetivo levantar dados sobre o desenvolvimento, histórico médico, desempenho acadêmico e profissional do(a) avaliado(a), a fim de subsidiar a análise neuropsicológica.")

st.header("Dados de Identificação")
nome = st.text_input("Nome")
data_avaliacao = st.date_input("Data")
tipo_avaliado = st.radio("Tipo de respondente", ["Paciente", "Outro"], index=0)
grau_parentesco = ""
if tipo_avaliado == "Outro":
    grau_parentesco = st.text_input("Grau de parentesco")

telefone = st.text_input("Telefone")
data_nascimento = st.date_input("Data de nascimento")
idade = st.number_input("Idade", min_value=0, max_value=120)
sexo = st.text_input("Sexo")
endereco = st.text_input("Endereço")
cidade_estado = st.text_input("Cidade/Estado de nascimento")
mao_dominante = st.radio("Mão dominante", ["Direita", "Esquerda"])
outro_idioma = st.checkbox("Fala outro idioma?")
idiomas = ""
if outro_idioma:
    idiomas = st.text_input("Quais idiomas?")

diagnosticos = st.text_area("Diagnóstico(s) médico(s)")
encaminhado_por = st.text_input("Encaminhado por")
data_acidente = st.date_input("Data do acidente/início da doença (se aplicável)")
possui_cuidador = st.checkbox("Possui cuidador?")
cuidador_grau = ""
if possui_cuidador:
    cuidador_grau = st.text_input("Grau de parentesco do cuidador")

st.header("Seção 1: Funcionamento Físico")
sintomas_fisicos = st.multiselect("Sintomas físicos", [
    "Dor de cabeça", "Tontura", "Vômitos", "Cansaço excessivo", "Incontinência urinária",
    "Intestino", "Equilíbrio", "Controle motor fino", "Fraqueza: Dir", "Fraqueza: Esq", "Fraqueza: Ambos",
    "Tremor: Dir", "Tremor: Esq", "Tremor: Ambos", "Tiques", "Bate em objetos", "Desmaios"])
outros_fisico = st.text_input("Outros sintomas físicos")

st.header("Seção 2: Funcionamento Sensorial")
sensoriais = st.multiselect("Sintomas sensoriais", [
    "Dormência/Formigamento: Dir", "Dormência/Formigamento: Esq", "Dormência/Formigamento: Ambos",
    "Discriminação térmica prejudicada", "Visão: Borra", "Visão: Luz forte", "Visão: Cegueira parcial",
    "Visão: Vê coisas irreais", "Audição: Perda auditiva", "Audição: Aparelho auditivo",
    "Paladar e Olfato: Alterados", "Paladar e Olfato: Inalterados"])
outros_sens = st.text_input("Outros sintomas sensoriais")

st.header("Seção 3: Cognição")
cognicao = st.multiselect("Dificuldades cognitivas", [
    "Dificuldade em aprender coisas novas", "Resolver problemas", "Planejamento",
    "Flexibilidade cognitiva", "Pensamento rápido", "Raciocínio sequencial"])
obs_cognicao = st.text_area("Observações cognitivas")

st.header("Seção 4: Linguagem e Matemática")
linguagem = st.multiselect("Dificuldades em linguagem/matemática", [
    "Nomear objetos", "Ser compreendido", "Sons incomuns", "Expressar pensamentos",
    "Entender fala", "Entender leitura", "Escrever (sem alteração motora)", "Operações matemáticas"])
outros_ling = st.text_input("Outros aspectos de linguagem")

st.header("Seção 5: Habilidades Não Verbais")
nverbais = st.multiselect("Habilidades não verbais", [
    "Lateralidade (dir/esq)", "Desenhar/copiar", "Vestir-se (sem alteração motora)",
    "Hábitos automatizados (ex: escovar os dentes)", "Rota habitual"])
outros_nv = st.text_input("Outros aspectos não verbais")

st.warning("Este documento é um modelo automatizado e deve ser revisado pelo(a) psicólogo(a) responsável.")

if st.button("Enviar"):
    doc = Document()
    doc.add_heading("Formulário de Pré-Avaliação Neuropsicológica - Adulto", 0)
    doc.add_paragraph(f"Nome: {nome}")
    doc.add_paragraph(f"Data: {data_avaliacao}")
    doc.add_paragraph(f"Tipo de respondente: {tipo_avaliado} {grau_parentesco}")
    doc.add_paragraph(f"Telefone: {telefone}, Nascimento: {data_nascimento}, Idade: {idade}, Sexo: {sexo}")
    doc.add_paragraph(f"Endereço: {endereco}, Cidade/Estado: {cidade_estado}, Mão dominante: {mao_dominante}")
    doc.add_paragraph(f"Idiomas: {idiomas}")
    doc.add_paragraph(f"Diagnóstico(s): {diagnosticos}, Encaminhado por: {encaminhado_por}, Acidente: {data_acidente}")
    doc.add_paragraph(f"Cuidador: {cuidador_grau}")
    doc.add_heading("Funcionamento Físico", level=1)
    doc.add_paragraph(", ".join(sintomas_fisicos) + ". Outros: " + outros_fisico)
    doc.add_heading("Funcionamento Sensorial", level=1)
    doc.add_paragraph(", ".join(sensoriais) + ". Outros: " + outros_sens)
    doc.add_heading("Cognição", level=1)
    doc.add_paragraph(", ".join(cognicao) + ". Observações: " + obs_cognicao)
    doc.add_heading("Linguagem e Matemática", level=1)
    doc.add_paragraph(", ".join(linguagem) + ". Outros: " + outros_ling)
    doc.add_heading("Habilidades Não Verbais", level=1)
    doc.add_paragraph(", ".join(nverbais) + ". Outros: " + outros_nv)

    filename = f"avaliacao_{nome.replace(' ', '_')}.docx"
    doc.save(filename)

    msg = EmailMessage()
    msg['Subject'] = 'Nova Avaliação Neuropsicológica - Adulto'
    msg['From'] = st.secrets["email"]["from"]
    msg['To'] = "luan.gama.psicologo@"
    msg.set_content(f"Formulário preenchido por {nome} em {data_avaliacao}.")

    with open(filename, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='vnd.openxmlformats-officedocument.wordprocessingml.document', filename=filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(st.secrets["email"]["from"], st.secrets["email"]["password"])
        smtp.send_message(msg)

    os.remove(filename)
    st.success("Formulário enviado com sucesso!")
