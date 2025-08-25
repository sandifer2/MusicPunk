# MusicPunk: A music review app inspired by Letterboxd



A music review application project with the intent of turning a barely working school project into a dynamic full-stack app with React, FastAPI, PostgreSQL(hosted on AWS RDS) and Capacitor(future)
This README is wildly innaccurate and will be updated in due time.
## Project Structure
- this is currently being reworked and may be innaccurate
```
MusicBoxV2/
├── .vscode/                  # VSCode configuration
│   └── settings.json
├── backend/                  # Flask server
│   └── app.py                # Flask API endpoints
├── my-react-app/             # React frontend
│   ├── public/               # Static assets
│   │   └── vite.svg
│   ├── src/                  # Source code
│   │   ├── assets/           # Images and other assets
│   │   │   └── react.svg
│   │   ├── Components/       # Reusable React components
│   │   │   └── Navbar.jsx    
│   │   ├── CSS/              # Stylesheets
│   │   │   ├── App.css
│   │   │   ├── Home.css
│   │   │   ├── Login.css
│   │   │   ├── NavBar.css
│   │   │   ├── Page.css
│   │   │   └── ProfilePage.css
│   │   ├── Pages/            # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Login.jsx
│   │   │   ├── Page2.jsx
│   │   │   ├── Profile.jsx
│   │   │   ├── SongReview.jsx
│   │   │   └── Table.jsx
│   │   ├── App.jsx           # Main application component
│   │   ├── index.css         # Global styles
│   │   ├── Layout.jsx        # Layout component with Navbar
│   │   └── main.jsx          # Application entry point
│   ├── .gitignore            # Git ignore file
│   ├── eslint.config.js      # ESLint configuration
│   ├── index.html            # HTML entry point
│   ├── package-lock.json     # npm dependencies lock file
│   ├── package.json          # npm dependencies and scripts
│   ├── README.md             # React app readme
│   └── vite.config.js        # Vite configuration
├── README.md                 # Project readme
└── testingConnection.py      # Database connection test script
```

## Technologies Used

- **Frontend**: React 19, React Router 7, Vite 6
- **Backend**: Flask (Python), Flask-CORS
- **Database**: MySQL
- **Development Tools**: ESLint, npm

## Setup Instructions

### Prerequisites

- Node.js (v18.0.0 or higher)
- Python 3.8+ 
- MySQL Server

### Backend Setup

1. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Flask and required packages:
   ```bash
   pip install Flask flask-cors mysql-connector-python
   ```

3. Configure your MySQL database connection in `backend/app.py`:
   ```python
   conn = mysql.connector.connect(
       host="your_database_host",  
       user="your_username",  
       password="your_password",  
       database="your_database_name"  
   )
   ```

4. Start the Flask server:
   ```bash
   cd backend
   python app.py
   ```
   The server will run on http://127.0.0.1:5000/

### Frontend Setup

1. Navigate to the React app directory:
   ```bash
   cd my-react-app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The application will be available at http://localhost:5173/

## Database Schema

The application uses the following database tables:
- `Songs`: Contains information about songs
- `Artists`: Contains information about artists
- `Albums`: Contains information about albums
- `users`: Contains user login information

## Features

- User authentication (login)
- Search songs, artists, and albums
- View music dataset tables
- Navigation between different pages
- Responsive design

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/songs` | GET | Search for songs by name, artist, or album |
| `/api/artists` | GET | Search for artists by name |
| `/api/albums` | GET | Search for albums by name |
| `/Songs` | GET | Get all songs (limited to 200) |
| `/Artists` | GET | Get all artists (limited to 200) |
| `/Albums` | GET | Get all albums (limited to 200) |
| `/login` | POST | User authentication |

## License

This project is intended for educational purposes.
