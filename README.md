# Movie Revenue Tracker 🎬

A Streamlit-based web application that helps analyze and visualize movie revenue data using the OMDB API. Track box office collections, compare movies across regions, and get detailed analytics about movie performance.

## Features 🌟

- **Movie Search**: Search for any movie using OMDB API
- **Revenue Analytics**: 
  - Box office performance metrics
  - Revenue breakdown analysis
  - Market distribution visualization
- **Multi-Movie Tracking**: 
  - Track multiple movies simultaneously
  - Compare performance across different titles
  - Genre-wise analysis
- **Interactive Dashboard**:
  - Filter by genre, region, and language
  - Dynamic visualizations
  - Export data to CSV

## Live Demo 🚀

Access the live application: [Movie Revenue Tracker](https://github.com/vikash517/movie-revenue-tracker)

## Installation 🛠️

1. Clone the repository:
   ```bash
   git clone https://github.com/vikash517/movie-revenue-tracker.git
   cd movie-revenue-tracker
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage 📖

1. **Search Movies**:
   - Enter movie title in the search box
   - View detailed analytics and revenue data
   - Add movies to tracking list

2. **Analytics Dashboard**:
   - Compare multiple movies
   - Filter by genre, region, or language
   - Export data for further analysis

3. **Data Visualization**:
   - Revenue breakdown charts
   - Genre distribution
   - Market share analysis
   - Performance metrics

## Technology Stack 💻

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **OMDB API**: Movie data source

## Project Structure 📁

```
movie-revenue-tracker/
├── app.py                 # Main Streamlit application
├── movie_revenue.csv      # Sample movie revenue data
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## API Configuration 🔑

The application uses the OMDB API. Current configuration:
- API Key: Included in the code
- Base URL: http://www.omdbapi.com/

## Features in Detail 🔍

### 1. Movie Search
- Real-time movie data fetching
- Comprehensive movie information
- Revenue and box office data

### 2. Analytics
- Revenue breakdown analysis
- Genre-wise performance
- Market distribution insights
- Historical performance tracking

### 3. Dashboard
- Interactive data filtering
- Multiple visualization options
- Export functionality
- Real-time updates

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Future Enhancements 🚀

- [ ] Add user authentication
- [ ] Implement movie recommendations
- [ ] Add more visualization options
- [ ] Include historical data tracking
- [ ] Enable custom data import

## Author ✍️

Vikash - [@vikash517](https://github.com/vikash517)

## License 📝

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- OMDB API for providing movie data
- Streamlit for the excellent web framework
- Python community for various packages used
