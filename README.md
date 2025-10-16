# Al Nassr Scouting System

A comprehensive scouting application built with Streamlit for Al Nassr FC to manage match reports, individual player reports, and player databases across multiple categories.

## Features

### 🔐 User Authentication
- Secure login system for scouts
- Three user accounts:
  - **rafagil** (password: rafagil)
  - **alvarolopez** (password: alvaro)
  - **juangambero** (password: juan)

### 📝 Match Reports
- Create detailed match reports including:
  - Match information (teams, date, venue, score)
  - Team formations and tactics
  - Team analysis (strengths/weaknesses)
  - Key players performance
  - Match summary and scouting notes
- View and filter all match reports by team, scout, and date

### 👤 Individual Player Reports
- Comprehensive player evaluation system with:
  - Player information (name, age, position, team, nationality)
  - Match context (opponent, result, minutes played)
  - Detailed attribute ratings (1-10 scale):
    - **Physical**: Pace, Strength, Stamina, Agility
    - **Technical**: Passing, Dribbling, Shooting, First Touch, etc.
    - **Tactical**: Positioning, Vision, Decision Making, etc.
    - **Mental**: Composure, Leadership, Determination, etc.
  - Overall and potential ratings
  - Recommendation levels:
    - 🟢 Sign Immediately
    - 🟡 Monitor Closely
    - 🟠 Keep Watching
    - 🔴 Not Interested
  - Strengths, weaknesses, and detailed notes
- View and filter reports by position, recommendation, and scout

### 💾 Player Database
- View player databases for three categories:
  - PRO LEAGUE
  - SAUDI U21 LEAGUE
  - U18 PREMIER LEAGUE
- Search and filter by:
  - Player name
  - Team
  - Position
  - Nationality
  - Age range
- Database statistics and metrics

## Installation

1. Install required packages:
```bash
pip install streamlit pandas pillow openpyxl
```

2. Ensure you have the following files in the project directory:
   - `alnassr.png` - Club logo
   - `dbproleague.xlsx` - Pro League database
   - `dbsaudiu21.xlsx` - U21 League database
   - `dbsaudiu18.xlsx` - U18 Premier League database

## Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Data Storage

- **Match Reports**: Stored in `match_reports/` directory as JSON files
- **Individual Reports**: Stored in `individual_reports/` directory as JSON files
- Reports are automatically organized by category and date

## Usage Tips

1. **Login**: Use one of the three scout accounts to access the system
2. **Select Category**: Choose the league category from the sidebar
3. **Create Reports**: Use the forms in tabs 1 and 3 to create new reports
4. **View Reports**: Browse and filter existing reports in tabs 2 and 4
5. **Database**: Access the player database in tab 5 with advanced filtering

## File Structure

```
alnassrsaudi/
├── app.py                    # Main application
├── alnassr.png              # Club logo
├── dbproleague.xlsx         # Pro League database
├── dbsaudiu21.xlsx          # U21 database
├── dbsaudiu18.xlsx          # U18 database
├── match_reports/           # Match report JSON files
├── individual_reports/      # Individual report JSON files
└── README.md               # This file
```

## Features by Tab

### Tab 1: Create Match Report
- Match details form
- Team formations and tactics
- Analysis of both teams
- Key players and match summary

### Tab 2: View Match Reports
- List of all match reports
- Filter by team, scout, date
- Expandable detailed view

### Tab 3: Create Individual Report
- Player information form
- Comprehensive attribute ratings
- Performance assessment
- Recommendation system

### Tab 4: View Individual Reports
- List of all player reports
- Filter by position, recommendation, scout
- Color-coded recommendations
- Detailed attribute visualization

### Tab 5: Database
- Player database viewer
- Multi-filter system
- Search functionality
- Database statistics

## Notes

- All reports are saved locally as JSON files
- Reports are automatically timestamped
- The application supports multiple scouts working simultaneously
- Data persists between sessions

## Support

For issues or questions, contact the development team.
