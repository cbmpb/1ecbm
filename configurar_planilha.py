"""Popula a planilha Google Sheets do Portal 1ª ECBM com abas, cabeçalhos e dados de exemplo."""

import sys

import gspread
from google.oauth2.service_account import Credentials

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CREDENCIAIS = "credenciais.json"
PLANILHA_ID = "112htcChpKcOm-jy_p_nBOq6c0hDOOM_qr6CMht7KWGg"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

ABAS = {
    "formularios": {
        "cabecalho": ["titulo", "descricao", "link", "ativo"],
        "linhas": [
            ["Matrícula — Novo Aluno", "Requerimento de matrícula para novos alunos. Documentação obrigatória listada ao final.", "https://forms.gle/exemplo-matricula", "SIM"],
            ["Solicitação de Impressão", "Requisição de impressão de provas, listas e materiais pedagógicos para professores.", "https://forms.gle/exemplo-impressao", "SIM"],
            ["Declaração de Vínculo", "Solicitação de declaração de matrícula ativa para fins de comprovação.", "", "NÃO"],
        ],
    },
    "agendamentos": {
        "cabecalho": ["titulo", "descricao", "link", "icone"],
        "linhas": [
            ["Biblioteca", "Agendamento do espaço e acervo da biblioteca escolar para uso por turmas ou pesquisa individual.", "https://forms.gle/exemplo-biblioteca", "📚"],
            ["Robótica", "Agendamento do laboratório de robótica para atividades pedagógicas e projetos.", "https://forms.gle/exemplo-robotica", "🤖"],
            ["Quadra Poliesportiva", "Agendamento da quadra para aulas, treinos e eventos internos.", "https://forms.gle/exemplo-quadra", "🏀"],
        ],
    },
    "avisos": {
        "cabecalho": ["dia", "mes", "titulo", "texto"],
        "linhas": [
            ["20", "JUN", "Entrega de Boletins", "Boletins do 1º bimestre disponíveis na secretaria. Retirada de seg a sex, das 7h às 17h."],
            ["18", "JUN", "Ponto Facultativo", "Não haverá aula no dia 24/06 (São João). Atividade de reposição a definir."],
            ["10", "JUN", "Prazo de Matrícula", "Encerra em 30/06 o prazo para regularização de documentação de matrícula."],
        ],
    },
    "agenda": {
        "cabecalho": ["mes", "descricao"],
        "linhas": [
            ["JUL", "01 a 31 — Férias de julho"],
            ["AGO", "01 — Início do 2º semestre"],
            ["SET", "07 — Desfile Cívico-Militar"],
        ],
    },
    "telefones": {
        "cabecalho": ["setor", "numero"],
        "linhas": [
            ["Secretaria Escolar", "(83) 3341-1234"],
            ["Direção da 1ª ECBM", "(83) 3341-1235"],
            ["2º CRBM — Campina Grande", "(83) 3341-1236"],
        ],
    },
    "downloads": {
        "cabecalho": ["nome", "tipo", "link"],
        "linhas": [
            ["Regimento Escolar Interno 2026", "PDF", "https://drive.google.com/exemplo-regimento"],
            ["Calendário Letivo 2026", "PDF", "https://drive.google.com/exemplo-calendario"],
            ["Requerimento de Matrícula", "DOCX", "https://drive.google.com/exemplo-requerimento"],
        ],
    },
    "redes": {
        "cabecalho": ["nome", "link", "tipo"],
        "linhas": [
            ["@1ecbm_oficial", "https://instagram.com/1ecbm_oficial", "instagram"],
            ["1ª ECBM Campina Grande", "https://facebook.com/1ecbmcg", "facebook"],
        ],
    },
    "fotos": {
        "cabecalho": ["url"],
        "linhas": [
            ["https://drive.google.com/uc?export=view&id=exemplo-foto-1"],
            ["https://drive.google.com/uc?export=view&id=exemplo-foto-2"],
        ],
    },
}


def conectar():
    credenciais = Credentials.from_service_account_file(CREDENCIAIS, scopes=SCOPES)
    cliente = gspread.authorize(credenciais)
    return cliente.open_by_key(PLANILHA_ID)


def preencher_aba(planilha, nome_aba, cabecalho, linhas):
    try:
        aba = planilha.worksheet(nome_aba)
    except gspread.WorksheetNotFound:
        aba = planilha.add_worksheet(title=nome_aba, rows=max(len(linhas) + 1, 10), cols=len(cabecalho))

    aba.clear()
    aba.update(values=[cabecalho] + linhas, range_name="A1")
    print(f"  ✓ Aba '{nome_aba}' preenchida ({len(linhas)} linhas de exemplo)")


def main():
    print("Conectando à planilha do Portal 1ª ECBM...")
    planilha = conectar()
    print(f"Conectado: {planilha.title}\n")

    for nome_aba, conteudo in ABAS.items():
        preencher_aba(planilha, nome_aba, conteudo["cabecalho"], conteudo["linhas"])

    print("\nConcluído. Todas as abas foram configuradas com cabeçalhos e dados de exemplo.")


if __name__ == "__main__":
    main()
