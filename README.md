
# GoogleSheetsChangeSensor

## Descrição
O **GoogleSheetsChangeSensor** é um sensor customizado para o Apache Airflow que monitora mudanças em um intervalo específico de uma planilha do Google Sheets. Ele é útil para automatizar workflows que dependem de alterações em planilhas colaborativas, como disparar pipelines de ETL ou notificações quando novos dados são inseridos.

---

## Funcionalidades
- Monitora alterações em intervalos específicos do Google Sheets.
- Detecta mudanças comparando um hash dos dados anteriores com os novos.
- Integra-se facilmente ao Airflow como um `BaseSensorOperator`.
- Autentica via contas de serviço do Google.

---

## Requisitos

### Ferramentas e Bibliotecas
- Apache Airflow 2.x ou superior
- Python 3.7 ou superior
- Dependências do Google API:
  ```bash
  pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
  ```

### Credenciais
Para usar o sensor, você precisará:
1. Uma conta de serviço no Google Cloud.
2. Um arquivo de credenciais JSON da conta de serviço com permissões para acessar o Google Sheets.
3. Compartilhar a planilha com o e-mail da conta de serviço.

---

## Instalação

### Clone o repositório:
```bash
git clone https://github.com/seu-usuario/nome-repositorio.git
```

### Instale as dependências mencionadas:
```bash
pip install -r requirements.txt
```

### Configure suas credenciais e use no DAG:
- Configure o ID da planilha e o intervalo a ser monitorado.

---

## Uso

### Classe `GoogleSheetsChangeSensor`
Aqui está um exemplo de como usar o sensor em um DAG do Airflow:

```python
from airflow import DAG
from airflow.utils.dates import days_ago
from seu_modulo.google_sheets_sensor import GoogleSheetsChangeSensor

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
}

dag = DAG(
    'google_sheets_monitoring_dag',
    default_args=default_args,
    schedule_interval='@hourly',
)

google_sheets_sensor = GoogleSheetsChangeSensor(
    task_id='monitor_google_sheet',
    spreadsheet_id='SEU_SPREADSHEET_ID',
    range_name='Sheet1!A1:C10',
    credentials={
        # Credenciais como dicionário
        # Exemplo: json.loads('{"tipo": "conta de serviço"...}')
    },
    dag=dag
)
```

---

### Parâmetros da Classe

| Parâmetro          | Tipo   | Descrição                                                                 |
|---------------------|--------|---------------------------------------------------------------------------|
| `spreadsheet_id`    | `str`  | ID da planilha a ser monitorada.                                          |
| `range_name`        | `str`  | Intervalo de células no formato `Sheet1!A1:C10`.                         |
| `credentials`       | `dict` | Credenciais da conta de serviço no formato JSON.                         |
| `*args`, `**kwargs` | `list` | Argumentos adicionais para o `BaseSensorOperator`.                       |

---

### Resultado
- **`True`**: Se os dados no intervalo da planilha mudaram.
- **`False`**: Se não houver alterações.

---

## Desenvolvimento

Se você deseja contribuir, siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie um branch para suas alterações:
   ```bash
   git checkout -b minha-nova-funcionalidade
   ```
3. Commit suas alterações:
   ```bash
   git commit -m "Adicionei uma nova funcionalidade"
   ```
4. Faça o push do branch:
   ```bash
   git push origin minha-nova-funcionalidade
   ```
5. Abra um Pull Request.

---

## Licença
Este projeto está licenciado sob a **MIT License**.

---

## Contato
Murilo Eduardo dos Santos Lima  

