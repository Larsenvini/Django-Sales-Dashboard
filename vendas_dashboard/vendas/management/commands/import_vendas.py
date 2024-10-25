import pandas as pd
from django.core.management.base import BaseCommand
from vendas.models import Venda

class Command(BaseCommand):
    help = 'Testa inserção no banco de dados'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Caminho para o arquivo CSV de vendas')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        self.test_database_insertion(file_path)

    def test_database_insertion(self, file_path):
        try:
            # Lendo o CSV
            df = pd.read_csv(file_path)

            # Converter colunas para os tipos corretos (float para decimais)
            df['Quantidade'] = df['Quantidade'].astype(float)
            df['Preço'] = df['Preço'].astype(float)
            df['Total de Vendas'] = df['Total de Vendas'].astype(float)

            row = df.iloc[0]  # Pega a primeira linha do CSV

            # Tenta criar uma venda no banco de dados
            venda = Venda.objects.create(
                data_venda=pd.to_datetime(row['Data da Venda']),
                produto=row['Produto'],
                quantidade=row['Quantidade'],
                preco=row['Preço'],
                regiao=row['Região'],
                vendedor=row['Vendedor'],
                total_vendas=row['Total de Vendas']
            )
            self.stdout.write(self.style.SUCCESS(f"Venda inserida com sucesso: {venda}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro ao inserir no banco de dados: {str(e)}"))
