import subprocess
import sys
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════
#  CONFIGURAÇÃO
# ═══════════════════════════════════════════════════════
PASTA = Path(r"C:\Users\rault\Documents\Dev\portal-1ecbm")

# ═══════════════════════════════════════════════════════
#  SCRIPT — não alterar abaixo
# ═══════════════════════════════════════════════════════

def rodar(comando, pasta):
    resultado = subprocess.run(
        comando,
        cwd=pasta,
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if resultado.returncode != 0:
        print(f"ERRO: {resultado.stderr.strip()}")
        sys.exit(1)
    return resultado.stdout.strip()

def publicar():
    print("=" * 50)
    print("  Portal 1ª ECBM — Publicação GitHub Pages")
    print("=" * 50)

    # Verificar se a pasta existe
    if not PASTA.exists():
        print(f"ERRO: Pasta não encontrada: {PASTA}")
        sys.exit(1)

    # Verificar se o index.html existe
    if not (PASTA / "index.html").exists():
        print(f"ERRO: index.html não encontrado em {PASTA}")
        sys.exit(1)

    print(f"\n📁 Pasta: {PASTA}")
    print(f"🕐 Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # Git add
    print("\n⏳ Preparando arquivos...")
    rodar(["git", "add", "."], PASTA)

    # Verificar se há mudanças
    status = rodar(["git", "status", "--porcelain"], PASTA)
    if not status:
        print("✅ Nenhuma alteração detectada. O site já está atualizado.")
        return

    # Git commit
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    mensagem = f"Atualização do portal - {agora}"
    print(f"📝 Commit: {mensagem}")
    rodar(["git", "commit", "-m", mensagem], PASTA)

    # Git push
    print("🚀 Publicando no GitHub Pages...")
    rodar(["git", "push", "origin", "main"], PASTA)

    print("\n✅ Portal publicado com sucesso!")
    print("🌐 Acesse: https://cbmpb.github.io/1ecbm")
    print("\nAguarde cerca de 1 minuto para o site atualizar.")

if __name__ == "__main__":
    publicar()
