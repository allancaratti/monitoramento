# 🖥️ Monitoramento de Servidores e Serviços
## 📌 Descrição

Script em Python para monitoramento básico de infraestrutura.

Verifica disponibilidade (ping).

Testa portas abertas.

Mede latência de resposta.

Gera relatórios em CSV/Excel.

Envia alertas por e-mail, Telegram ou Slack.

## ⚙️ Funcionalidades

 * Ping em hosts locais ou remotos

 * Verificação de portas TCP (ex: 22, 80, 443, 3389)

 * Log automático em CSV

 * Alertas por e-mail (futuro upgrade)

 * Alertas por Telegram/Slack (futuro upgrade)

 * Dashboard Web (Flask) (futuro upgrade)

 
 ## 📂 Estrutura do Projeto
monitoring-tool/
│── data/               # pasta para arquivos de log e demais
    │──status.csv       # Relatórios salvos (Log)
│── monitor.py          # Código principal
│── config.json         # Configuração de hosts e portas
│── requirements.txt    # Dependências
│── README.md           # Documentação
│── LICENSE.md          # Arquivo de licença


## 📊 Exemplo de Saída (CSV)
DataHora,Host,IP,Porta,Status,Latencia
2025-09-24 13:30,PC de Casa,192.168.0.10,22,OK,35ms
2025-09-24 13:30,Roteador,192.168.0.1,80,FALHA,-

## 🚀 Como rodar

Clone o repositório:
 ```bash
git clone https://github.com/seuusuario/monitoring-tool.git
cd monitoring-tool
```

Instale as dependências: `pip install -r requirements.txt`


Configure os hosts no config.json

Execute o script: `python monitor.py`


## 📌 Próximos Passos

 Implementar envio de relatórios por e-mail

 Adicionar integração com Telegram/Slack

 Criar dashboard web em Flask/Chart.js