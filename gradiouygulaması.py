from nicegui import ui
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Tarihleri otomatik hesaplayan fonksiyon
def calculate_dates(time_range):
    today = datetime.today()
    if time_range == "Son 6 Ay":
        start_date = (today - timedelta(days=182)).strftime("%Y-%m-%d")
    elif time_range == "Son 1 Yıl":
        start_date = (today - timedelta(days=365)).strftime("%Y-%m-%d")
    elif time_range == "Son 2 Yıl":
        start_date = (today - timedelta(days=730)).strftime("%Y-%m-%d")
    elif time_range == "Son 5 Yıl":
        start_date = (today - timedelta(days=1825)).strftime("%Y-%m-%d")   
    else:
        start_date = ""
    end_date = today.strftime("%Y-%m-%d")
    return start_date, end_date

# Buy/Sell noktalarını belirleyen fonksiyon
def identify_signals(closing_prices, short_term_ma, long_term_ma):
    signals = pd.DataFrame(index=closing_prices.index)
    signals['Buy'] = (short_term_ma > long_term_ma) & (short_term_ma.shift(1) <= long_term_ma.shift(1))
    signals['Sell'] = (short_term_ma < long_term_ma) & (short_term_ma.shift(1) >= long_term_ma.shift(1))
    return signals

# Veriyi işleyip grafiği oluşturan fonksiyon
def handle_inputs(time_range, start_date, end_date, stock_symbol):
    if time_range != "Manuel":
        start_date, end_date = calculate_dates(time_range)

    try:
        t1 = datetime.strptime(start_date, "%Y-%m-%d")
        t2 = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        return "Lütfen tarih formatını (YYYY-MM-DD) doğru girin.", None

    if t1 > t2:
        return "Başlangıç tarihi bitiş tarihinden büyük olamaz.", None

    if stock_symbol.strip():
        try:
            stock = yf.Ticker(stock_symbol)
            hist = stock.history(start=start_date, end=end_date)
            closing_prices = hist['Close']
        except Exception as e:
            return f"Veri çekilirken hata oluştu: {str(e)}", None
    else:
        return "Lütfen geçerli bir hisse senedi sembolü girin.", None

    if closing_prices.empty:
        return "Belirtilen tarih aralığında veri bulunamadı.", None

    # Hareketli ortalamaları hesapla
    short_term_ma = closing_prices.rolling(window=20).mean()
    long_term_ma = closing_prices.rolling(window=50).mean()

    # Buy/Sell sinyalleri belirle
    signals = identify_signals(closing_prices, short_term_ma, long_term_ma)

    # Grafik oluşturma
    plt.figure(figsize=(14, 8))
    plt.plot(closing_prices, label=f'{stock_symbol} Closing Prices', color='blue')
    plt.plot(short_term_ma, label='20-Day Moving Average', color='orange')
    plt.plot(long_term_ma, label='50-Day Moving Average', color='green')

    # Buy/Sell noktalarını işaretle
    buy_signals = closing_prices[signals['Buy']]
    sell_signals = closing_prices[signals['Sell']]
    plt.scatter(buy_signals.index, buy_signals, label='Buy Signal', marker='^', color='green', s=100)
    plt.scatter(sell_signals.index, sell_signals, label='Sell Signal', marker='v', color='red', s=100)

    plt.title(f'{stock_symbol} Closing Prices with Buy/Sell Signals')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.grid()

    # Her analiz için yeni grafik kaydetme
    grafik_dosyasi = f"grafik_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(grafik_dosyasi)
    plt.close()

    return f"Başlangıç Tarihi: {start_date}\nBitiş Tarihi: {end_date}", grafik_dosyasi

# NiceGUI arayüzü
with ui.page(path="/") as page:  # path parametresi eklenmiştir
    with ui.column().classes("bg-gray-100 p-8 rounded shadow-lg max-w-screen-md mx-auto"):
        ui.label("Hisse Senedi Analiz Uygulaması").classes('text-3xl font-bold text-blue-600 mb-4 text-center')

        with ui.card().classes("p-4 bg-white shadow-md"):
            ui.label("Zaman Aralığını Seçin").classes("text-lg font-semibold")
            time_range = ui.radio(
                options=["Son 6 Ay", "Son 1 Yıl", "Son 2 Yıl", "Manuel"]
            ).classes("my-4")

        with ui.card().classes("p-4 bg-white shadow-md"):
            ui.label("Tarih Bilgileri").classes("text-lg font-semibold mb-2")
            start_date = ui.input(label="Başlangıç Tarihi (YYYY-MM-DD)").classes("w-full mb-2")
            end_date = ui.input(label="Bitiş Tarihi (YYYY-MM-DD)").classes("w-full mb-4")

        with ui.card().classes("p-4 bg-white shadow-md"):
            ui.label("Hisse Senedi Bilgileri").classes("text-lg font-semibold mb-2")
            stock_symbol = ui.input(label="Hisse Senedi Sembolü (Örn: MSFT, AAPL)").classes("w-full mb-4")

        result = ui.label("").classes("text-red-500 font-semibold mt-4")
        grafik = ui.image().style('max-height: 500px;').classes("my-4")

        def run_analysis():
            result_text, grafik_dosyasi = handle_inputs(
                time_range.value, start_date.value, end_date.value, stock_symbol.value
            )
            result.set_text(result_text)
            if grafik_dosyasi:
                grafik.set_source(grafik_dosyasi)

        ui.button("Analizi Çalıştır", on_click=run_analysis).classes('bg-blue-600 text-white p-4 rounded shadow-lg hover:bg-blue-700 mt-4')

ui.run()
