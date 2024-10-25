from django.shortcuts import render
from .models import Venda
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import io
import urllib
import matplotlib.pyplot as plt


def dashboard_view(request):
    # Query all sales data
    vendas_data = Venda.objects.all()
    print(vendas_data)

    # Aggregate total sales and count orders
    total_sales = sum(venda.total_vendas for venda in vendas_data)
    total_orders = vendas_data.count()
    avg_sale_value = total_sales / total_orders if total_orders else 0

    # Aggregate data for the line chart
    dates = [venda.data_venda for venda in vendas_data]
    totals = [venda.total_vendas for venda in vendas_data]

    # Aggregate data for sales by region (pie chart)
    regioes = set(venda.regiao for venda in vendas_data)
    regioes_totals = {regiao: sum(v.total_vendas for v in vendas_data if v.regiao == regiao) for regiao in regioes}

    # Pass data to the template
    context = {
        'vendas': {
            'dates': dates,
            'totals': totals,
            'regioes': list(regioes),  # List of regions
            'regioes_totals': list(regioes_totals.values()),  # Sales totals by region
        },
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_sale_value': avg_sale_value,
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
    model = ARIMA(df['total_vendas'], order=(5, 1, 0))  # Ajuste os parâmetros conforme necessário
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