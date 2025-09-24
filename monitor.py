"""
monitor.py - Versão 1.1 (logs em pasta `data`)
- Ping em hosts
- Checa portas TCP
- Gera log em data/status.csv
- Ignora hosts com "enabled": false no config.json
- By @allancaratti (GitHub) | 2025
"""

import os
import socket
import csv
import json
from datetime import datetime
from shutil import which
import subprocess as sp
import sys

print("🖥️ Monitoramento de Servidores e Serviços - By: @allancaratti (GitHub)")

CONFIG_FILE = "config.json" # arquivo de configuração dos hosts
DATA_DIR = "data" # pasta para salvar logs
LOG_FILE = os.path.join(DATA_DIR, "status.csv") # arquivo de log


def has_ping_command():
    """Verifica se o sistema tem o comando ping disponível."""
    return which("ping") is not None


def ping_host(ip):
    """
    Executa ping e retorna (bool_alive, latency_str).
    Usa o comando ping do OS para obter resultado e latência aproximada.
    """
    if not has_ping_command():
        # fallback: tentar socket connect em porta 80 como "ping" bruto (menos confiável)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect_ex((ip, 80))
            sock.close()
            return True, "-"
        except Exception:
            return False, "-"

    try:
        # -n (Windows) | -c (Linux/Mac)
        param = "-n" if os.name == "nt" else "-c"
        # usar subprocess para capturar saída
        completed = sp.run(["ping", param, "1", ip], capture_output=True, text=True, timeout=5)
        response = completed.stdout + completed.stderr

        if "ttl=" in response.lower() or "ttl=" in response:
            # tentar extrair tempo/latência
            lower = response.lower()
            # formatos possíveis: "time=12ms", "tempo=12ms"
            if "time=" in lower:
                try:
                    latency = lower.split("time=")[1].split("ms")[0].strip()
                    return True, f"{latency}ms"
                except Exception:
                    return True, "-"
            elif "tempo=" in lower:
                try:
                    latency = lower.split("tempo=")[1].split("ms")[0].strip()
                    return True, f"{latency}ms"
                except Exception:
                    return True, "-"
            else:
                return True, "-"
        else:
            return False, "-"
    except sp.TimeoutExpired:
        return False, "-"
    except Exception:
        return False, "-"


def check_port(ip, port, timeout=2):
    """Verifica se a porta TCP está aberta (True) ou fechada (False)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, int(port)))
        sock.close()
        return result == 0
    except Exception:
        return False


def load_config(path=CONFIG_FILE):
    """Carrega arquivo config.json e retorna dict."""
    if not os.path.isfile(path):
        print(f"❌ Arquivo de configuração não encontrado: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_log_row(row):
    """Grava uma linha no CSV de log (cria pasta data e cabeçalho quando necessário)."""
    os.makedirs(DATA_DIR, exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["DataHora", "Host", "Type", "IP", "Porta", "Status", "Latencia"])
        writer.writerow(row)


def main():
    config = load_config()
    hosts = config.get("hosts", [])

    # filtrar apenas os habilitados
    hosts_enabled = [h for h in hosts if h.get("enabled", True)]

    if not hosts_enabled:
        print("⚠️ Nenhum host habilitado encontrado no config.json. Verifique 'enabled: true'.")
        return

    for host in hosts_enabled:
        name = host.get("name", "unnamed")
        ip = host.get("ip")
        ports = host.get("ports", [])
        host_type = host.get("type", "unknown")

        if not ip:
            print(f"⚠️ Host '{name}' sem IP/hostname. Pulando.")
            continue

        print(f"\n🔎 {name} ({ip}) — tipo: {host_type}")

        alive, latency = ping_host(ip)
        print(f"   → Ping: {'ONLINE' if alive else 'OFFLINE'} | Latência: {latency}")

        # se não houver portas definidas, ainda registramos o ping (porta = '-')
        if not ports:
            status = "ONLINE" if alive else "OFFLINE"
            write_log_row([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                name,
                host_type,
                ip,
                "-",
                status,
                latency if alive else "-"
            ])
        else:
            for port in ports:
                port_status = "ABERTA" if (alive and check_port(ip, port)) else "FECHADA"
                if not alive:
                    port_status = "HOST_INDISPONÍVEL"
                print(f"   - Porta {port}: {port_status}")
                write_log_row([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    name,
                    host_type,
                    ip,
                    port,
                    port_status,
                    latency if alive else "-"
                ])

    print(f"\n✅ Monitoramento concluído. Log salvo em: {LOG_FILE}")


if __name__ == "__main__":
    main()
