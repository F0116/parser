import requests
import sys

def get_weather_forecast(city: str, api_key: str) -> list:
    """Получает прогноз погоды на 5 дней (с шагом 3 часа) через OpenWeatherMap API."""
    
    # 1. Базовый URL эндпоинта прогноза
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    
    # 2. Параметры запроса
    params = {
        "q": city,          # Город
        "appid": api_key,   # Ваш API-ключ
        "lang": "ru",       # Язык описания погоды
        "units": "metric"   # Единицы измерения (°C, м/с)
    }
    
    try:
        # 3. Отправляем GET-запрос
        response = requests.get(base_url, params=params, timeout=10)
        
        # 4. Проверяем, что сервер вернул успешный статус (200-299)
        response.raise_for_status()
        
        # 5. Преобразуем ответ из JSON в Python-словарь
        data = response.json()
        
        # 6. Извлекаем список прогнозов
        forecast_list = data.get("list", [])
        if not forecast_list:
            print("⚠️ Прогноз не найден. Проверьте название города.")
            return []
        
        # 7. Формируем удобную структуру для вывода
        parsed_forecast = []
        for item in forecast_list:
            parsed_forecast.append({
                "date_time": item["dt_txt"],
                "temperature": f"{item['main']['temp']} °C",
                "feels_like": f"{item['main']['feels_like']} °C",
                "description": item["weather"][0]["description"],
                "wind_speed": f"{item['wind']['speed']} м/с",
                "humidity": f"{item['main']['humidity']} %"
            })
        return parsed_forecast

    except requests.exceptions.HTTPError as e:
        print(f"❌ Ошибка HTTP: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ Нет подключения к интернету или неверный URL.")
    except requests.exceptions.Timeout:
        print("⏳ Превышено время ожидания ответа от сервера.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса: {e}")
    except KeyError as e:
        print(f"❌ Ошибка структуры данных: отсутствует ключ {e}")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
    
    return []

# 8. Запуск скрипта
if __name__ == "__main__":
    API_KEY = "ab103bd334ed4082f14421c114929a3d"  # Вставьте реальный ключ
    CITY = "Москва"           # Или любой другой город
    
    forecast = get_weather_forecast(CITY, API_KEY)
    
    if forecast:
        print(f"🌤 Прогноз для города {CITY}:\n")
        for entry in forecast:
            print(f"📅 {entry['date_time']}")
            print(f"   🌡 Температура: {entry['temperature']} (ощущается как {entry['feels_like']})")
            print(f"   🌧 Описание: {entry['description']}")
            print(f"   💨 Ветер: {entry['wind_speed']}")
            print(f"   💧 Влажность: {entry['humidity']}")
            print("-" * 40)