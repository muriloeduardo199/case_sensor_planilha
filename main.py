from airflow.sensors.base import BaseSensorOperator



class GoogleSheetsChangeSensor(BaseSensorOperator):
    """
    Sensor do Airflow para detectar mudanças em um intervalo específico de uma planilha do Google Sheets.
    
    Este sensor monitora periodicamente os dados em um intervalo de uma planilha e detecta mudanças
    usando um hash dos dados. Ele é útil para disparar workflows no Airflow com base em alterações feitas
    em planilhas colaborativas.

    Parâmetros:
    ----------
    spreadsheet_id : str
        O identificador único da planilha do Google Sheets a ser monitorada. 
        Este ID é obtido da URL da planilha (ex.: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/...).
    range_name : str
        O intervalo a ser monitorado na planilha (ex.: "Sheet1!A1:C10").
    credentials : dict
        As credenciais da conta de serviço para acessar a API do Google Sheets.
        Geralmente, é um dicionário carregado de um arquivo JSON com as chaves necessárias.
    *args : list
        Argumentos adicionais para o construtor da classe `BaseSensorOperator`.
    **kwargs : dict
        Argumentos nomeados adicionais para o construtor da classe `BaseSensorOperator`.

    Atributos:
    ----------
    last_hash : str ou None
        Armazena o hash da última execução. Inicialmente é None até a primeira execução do sensor.
    
    Métodos:
    --------
    poke(context: dict) -> bool
        Método que verifica continuamente se houve mudanças nos dados do intervalo monitorado.
        Retorna True se os dados tiverem mudado desde a última execução, caso contrário, False.
    
    Exceções:
    ---------
    O método `poke` pode lançar exceções relacionadas à autenticação ou à API do Google Sheets,
    como `googleapiclient.errors.HttpError`, caso algo falhe na solicitação à API.

    Exemplo de Uso:
    ---------------
    # Exemplo em um DAG do Airflow
    from airflow import DAG
    from airflow.utils.dates import days_ago

    default_args = {
        'owner': 'airflow',
        'start_date': days_ago(1),
    }

    dag = DAG(
        'google_sheets_change_sensor_dag',
        default_args=default_args,
        schedule_interval='@hourly',
    )

    google_sheets_sensor = GoogleSheetsChangeSensor(
        task_id='monitor_google_sheet',
        spreadsheet_id='sua_planilha_id_aqui',
        range_name='Sheet1!A1:C10',
        credentials={'tipo_credenciais': 'detalhes_aqui'},
        dag=dag
    )
    """
    
    def __init__(self, spreadsheet_id, range_name, credentials, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spreadsheet_id = spreadsheet_id
        self.range_name = range_name
        self.credentials = credentials
        self.last_hash = None  # Para armazenar o hash dos dados

    def poke(self, context):
        """
        Método principal que verifica mudanças nos dados do Google Sheets.

        Parâmetros:
        ----------
        context : dict
            O contexto fornecido pelo Airflow durante a execução da tarefa.

        Retorno:
        -------
        bool
            True se os dados no intervalo monitorado mudaram desde a última execução.
            False caso contrário.
        """
        # Autenticar usando as credenciais do Google
        creds = Credentials.from_service_account_info(self.credentials)
        service = build('sheets', 'v4', credentials=creds)

        # Obter os dados da planilha
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=self.spreadsheet_id,
            range=self.range_name
        ).execute()

        # Criar um hash dos dados
        current_data = result.get('values', [])
        current_hash = hashlib.md5(str(current_data).encode()).hexdigest()

        # Verificar se os dados mudaram
        if self.last_hash is None:
            self.last_hash = current_hash
            self.log.info("Primeira execução. Nenhuma mudança detectada ainda.")
            return False
        elif current_hash != self.last_hash:
            self.log.info("Mudança detectada na planilha!")
            return True

        return False
