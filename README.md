# QuickTT - Timetable Management System

A modern web-based timetable management system that automatically generates conflict-free schedules for multiple classes, built with FastAPI and React.

## 🌐 Live Demo

**[https://quick-tt-1.onrender.com](https://quick-tt-1.onrender.com)**

## ✨ Features

- **Automated Scheduling**: Generate conflict-free timetables using constraint-based scheduling algorithms
- **Multi-Class Support**: Create schedules for multiple classes simultaneously (e.g., 12A, 12B, 11A, 11B)
- **Subject Management**: Flexible subject assignment for different streams (Science, Arts, etc.)
- **Persistent Storage**: Save and retrieve timetables using SQLite database
- **Interactive UI**: Clean, modern interface built with React and Tailwind CSS
- **RESTful API**: Full-featured API for programmatic access
- **Real-time Preview**: View generated schedules before saving

## 🚀 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server
- **Python 3.11+**

### Frontend
- **React 19** - UI library
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library
- **Framer Motion** - Animation library

## 📁 Project Structure

```
QUICKTT/
├── api/                    # FastAPI application
│   ├── main.py            # API routes and server configuration
│   └── models.py          # Pydantic models for API
├── timetable_system/      # Core business logic
│   ├── models/            # Database models
│   ├── repositories/      # Data access layer
│   ├── services/          # Business logic (scheduler, input)
│   └── utils/             # Utilities (logger, etc.)
├── web/                   # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Generator.jsx
│   │   │   └── TimetableView.jsx
│   │   ├── services/      # API client
│   │   └── App.jsx        # Root component
│   └── dist/              # Build output
├── build.sh               # Deployment build script
├── Dockerfile             # Multi-stage Docker configuration
├── requirements.txt       # Python dependencies
└── firebase.json          # Firebase hosting configuration
```

## 🛠️ Installation

### Prerequisites
- **Python 3.11+**
- **Node.js 18+**
- **npm**

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd QUICKTT
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and build frontend**
   ```bash
   cd web
   npm install
   npm run build
   cd ..
   ```

4. **Run the development server**
   ```bash
   uvicorn api.main:app --reload --port 8080
   ```

5. **Access the application**
   - Open your browser to `http://localhost:8080`

### Frontend Development Mode

For active frontend development with hot reload:

```bash
# Terminal 1 - Backend
uvicorn api.main:app --reload --port 8080

# Terminal 2 - Frontend (in /web directory)
cd web
npm run dev
```

Frontend dev server will run on `http://localhost:5173` with API proxying.

## 🐳 Docker Deployment

Build and run using Docker:

```bash
docker build -t quicktt .
docker run -p 8080:8080 quicktt
```

## 📡 API Endpoints

### Timetable Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/generate` | Generate a new timetable schedule |
| `GET` | `/timetables` | List all saved timetables |
| `GET` | `/timetables/{name}` | Get specific timetable details |
| `POST` | `/timetables` | Save a generated timetable |
| `DELETE` | `/timetables/{name}` | Delete a timetable |

### Example Request

**Generate Timetable**
```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "periods": 8,
    "classes": {
      "12A": ["MATH", "PHY", "CHEM", "BIO", "ENG", "CS", "PT", "LIB"],
      "12B": ["MATH", "PHY", "CHEM", "CS", "ENG", "PT", "LIB", "BIO"]
    }
  }'
```

## 🎯 Usage

1. **Create New Timetable**
   - Navigate to "New Timetable"
   - Set the number of periods per day
   - Configure classes and their subjects
   - Click "Generate Schedule"
   - Review the preview
   - Save with a unique name

2. **View Saved Timetables**
   - Access the Dashboard
   - Browse all saved timetables
   - Click on any timetable to view details
   - Delete outdated schedules as needed

## 🔧 Configuration

### Environment Variables

- `PORT` - Server port (default: 8080)
- `TT_DB_PASSWORD` - Database password (optional)

### Supported Subject Codes

**Science Stream**: MATH, PHY, CHEM, BIO, CS, ENG, PT, LIB  
**Arts Stream**: MATH, ACC, BST, ECO, IP, ENG, PT, LIB

## 📦 Build for Production

Run the build script:

```bash
./build.sh
```

This will:
1. Install Python dependencies
2. Build the React frontend
3. Generate optimized production assets

## 🚢 Deployment

The project is configured for deployment on:
- **Render** (primary)
- **Firebase Hosting** (frontend option)
- **Docker** containers

### Render Deployment

1. Connect your GitHub repository
2. Set build command: `./build.sh`
3. Set start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
4. Deploy!

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Known Issues

- Ensure both URLs point to the same deployment; only `quick-tt-1.onrender.com` is currently operational

## 📧 Contact

For questions or support, please open an issue in the GitHub repository.

---

**Made with ❤️ using FastAPI and React**