# Weather Dashboard Application

A modern Python weather dashboard built with CustomTkinter, featuring live weather data, historical tracking, and analytics.

## Features

- 🌤️ Live weather data from OpenWeatherMap API
- 📊 Temperature graphs and analytics
- 📝 Weather journal with data persistence
- 🔮 Tomorrow's temperature prediction
- 🎨 Modern dark/light theme switching
- 💾 Export data to CSV/JSON formats
- 🏙️ City comparison functionality

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd weatherdashboard_DunashaPayne
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**
   - Get an API key from [OpenWeatherMap](https://openweathermap.org/api)
   - Create a `.env` file in the project root:
     ```
     API_KEY=your_api_key_here
     ```

4. **Run the application**
   ```bash
   python main.py
   ```

## Project Structure

```
weatherdashboard_DunashaPayne/
├── main.py                 # Application entry point
├── gui.py                  # Main GUI controller
├── requirements.txt        # Dependencies
├── .env                   # API keys (not in git)
├── config/
│   ├── constants.py       # App configuration
│   └── api_key_loader.py  # Environment loader
└── src/
    ├── features/
    │   ├── weather_journal.py
    │   └── tomorrows_guess.py
    └── ui/
        ├── ui_components.py
        └── ui_journal.py
```

## Usage

1. Launch the application
2. Enter a city name to get current weather
3. Use the journal to track weather observations
4. Switch themes using the theme switcher
5. Export your data for analysis

## Requirements

- Python 3.8+
- CustomTkinter
- Pandas
- NumPy
- Matplotlib
- PIL (Pillow)
- python-dotenv
- requests

## License

This project is for educational purposes as part of a capstone project.
