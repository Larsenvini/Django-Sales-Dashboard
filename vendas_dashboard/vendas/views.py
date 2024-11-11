from django.shortcuts import render
from .models import Venda
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from io import BytesIO
from django.http import JsonResponse
import base64
import io
import urllib
import matplotlib.pyplot as plt
import json


def dashboard_view(request):
    # Sample data (replace these with actual data from your database or calculations)
    total_sales = 15000  # Total sales amount
    total_orders = 120    # Total number of orders
    avg_sale_value = total_sales / total_orders if total_orders > 0 else 0

    # Data for charts
    dates = ["2024-10-01", "2024-10-02", "2024-10-03"]  # Example dates for line chart
    totals = [5000, 7000, 3000]                          # Corresponding sales totals

    regioes = ["North", "South", "East", "West"]
    regioes_totals = [3000, 4000, 2000, 6000]            # Corresponding sales by region

    # Preparing data for template
    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_sale_value': avg_sale_value,
        'vendas': {
            'dates': json.dumps(dates),             # Convert list to JSON
            'totals': json.dumps(totals),           # Convert list to JSON
            'regioes': json.dumps(regioes),         # Convert list to JSON
            'regioes_totals': json.dumps(regioes_totals)  # Convert list to JSON
        }
    }

    return render(request, 'dashboard.html', context)


def forecast_sales(request):
    # Obter dados de vendas do banco de dados
    vendas = Venda.objects.all().values('data', 'total_vendas')
    df = pd.DataFrame(list(vendas))
    
    # Configurar o índice como a data
    df['data'] = pd.to_datetime(df['data'])
    df.set_index('data', inplace=True)
    
    # Ajustar o modelo ARIMA
    model = ARIMA(df['total_vendas'], order=(5, 1, 3))  # Ajuste os parâmetros conforme necessário
    model_fit = model.fit()

    # Fazer previsões
    forecast = model_fit.forecast(steps=10)  # Prever os próximos 10 períodos

    # Transformar previsões em um DataFrame para passar ao template
    forecast_df = pd.DataFrame(forecast, columns=['Previsão'])
    forecast_df.index = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=len(forecast), freq='D')

    # Gerar gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['total_vendas'], label='Vendas Passadas', color='blue')
    plt.plot(forecast_df.index, forecast_df['Previsão'], label='Previsão', color='red', linestyle='--')
    plt.title('Previsão de Vendas')
    plt.xlabel('Data')
    plt.ylabel('Total de Vendas')
    plt.legend()
    plt.grid()

    # Salvar o gráfico em um buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graphic = urllib.parse.quote(buf.getvalue())

    return render(request, 'vendas/forecast.html', {'forecast': forecast_df, 'graphic': graphic})

def plot_arima_forecast():
    
    import matplotlib
    matplotlib.use('Agg')

    # Exemplo de dados (substitua com seus dados reais)
    data = [100, 102, 104, 108, 110, 112, 115, 117, 120, 125]
    data_series = pd.Series(data)
    
    # Configura o modelo ARIMA
    model = ARIMA(data_series, order=(2, 1, 2))  # Ordem (p, d, q)
    model_fit = model.fit()
    
    # Faz a previsão para os próximos passos
    forecast = model_fit.forecast(steps=5)  # Exemplo: previsão para os próximos 5 períodos

    # Plotar os dados e a previsão
    plt.figure(figsize=(10, 5))
    plt.plot(data_series, label='Dados Originais')
    plt.plot(range(len(data_series), len(data_series) + len(forecast)), forecast, label='Previsão ARIMA', color='orange')
    plt.xlabel("Período")
    plt.ylabel("Valor")
    plt.title("Previsão ARIMA")
    plt.legend()

    # Salvar o gráfico em um formato que pode ser exibido no template
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(1)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    # Codificar a imagem para exibir no HTML
    graphic = base64.b64encode(image_png).decode("utf-8")
    return graphic

def sales_prevision(request):
    # Gera o gráfico de previsão ARIMA
    arima_graphic = plot_arima_forecast()
    return JsonResponse({"arima_graphic": arima_graphic})
