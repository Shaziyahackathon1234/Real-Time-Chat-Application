# 💬 ChatWave — Real-Time Chat Application

A full-stack **MERN** real-time chat app where users can register, log in, see who's online, chat instantly, **send images & documents**, manage their profile, and control their online-status privacy.

Built with **React + Redux Toolkit** on the frontend and **Node/Express + MongoDB + Socket.IO** on the backend.

---

## ✨ Features

- 🔐 **Authentication** — register & login with JWT stored in httpOnly cookies (passwords hashed with bcrypt)
- 💬 **Real-time messaging** — instant 1-to-1 chat powered by Socket.IO
- 🟢 **Live presence** — see who's online, with a privacy toggle to hide your own status
- 🖼️ **Image & document sharing** — send photos and files (Cloudinary, with inline fallback)
- 👤 **Profile management** — view & edit your name, gender, avatar (upload from device), and status
- 🧑‍🤝‍🧑 **View other users' profiles** — photo, username, gender, and joined date
- 🎨 **Modern UI** — clean white + blue theme, full-width responsive layout, default initials avatars
- 💾 **Persistent login** — stay logged in across refreshes (redux-persist)

---

## 🛠️ Technology Stack

### Frontend (`frontend/`)
| Technology | Purpose |
|---|---|
| React 18 (Create React App) | UI library |
| Redux Toolkit + React-Redux | Global state management |
| redux-persist | Persist state to localStorage |
| React Router DOM v6 | Client-side routing |
| Tailwind CSS + daisyUI | Styling |
| Axios | HTTP requests |
| socket.io-client | Real-time client |
| react-hot-toast | Toast notifications |
| react-icons | Icons |

### Backend (`backend/`)
| Technology | Purpose |
|---|---|
| Node.js + Express 4 | REST API server |
| MongoDB + Mongoose | Database & ODM |
| Socket.IO | Real-time messaging & presence |
| JWT (jsonwebtoken) | Auth tokens |
| bcryptjs | Password hashing |
| cookie-parser | Read auth cookies |
| cors | Cross-origin security |
| Cloudinary | Image/file hosting |
| dotenv | Environment variables |

---

## 📁 Project Structure

```
chat-application/
├── frontend/                 # React app
│   └── src/
│       ├── components/       # Login, Signup, HomePage, Sidebar, MessageContainer, etc.
│       ├── redux/            # store + slices (user, message, socket)
│       ├── hooks/            # useGetOtherUsers, useGetMessages, useGetRealTimeMessage
│       ├── utils/            # avatar + helpers
│       ├── App.js            # routes + socket setup
│       └── index.js          # entry + BASE_URL + providers
│
└── backend/                  # Express API
    ├── controllers/          # userController, messageController
    ├── routes/               # userRoute, messageRoute
    ├── models/               # userModel, messageModel, conversationModel
    ├── middleware/           # isAuthenticated (JWT check)
    ├── config/               # database.js, cloudinary.js
    ├── socket/               # socket.js (Socket.IO server)
    └── index.js              # server entry
```

---

## 🚀 Getting Started (Local Setup)

### Prerequisites
- Node.js (v16+)
- MongoDB (local or MongoDB Atlas)
- (Optional) a Cloudinary account for media hosting

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/chat-application.git
cd chat-application
```

### 2. Backend setup
```bash
cd backend
npm install
```
Create `backend/.env` (see `backend/.env.example`):
```
PORT=8080
MONGO_URI=your_mongodb_connection_string
JWT_SECRET_KEY=any_long_random_string

# Optional — for image/file hosting (leave empty to store inline)
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```
Run the backend:
```bash
npm run dev      # starts on http://localhost:8080
```

### 3. Frontend setup
```bash
cd frontend
npm install
npm start        # opens http://localhost:3000
```

> The frontend connects to the backend via `BASE_URL` in `frontend/src/index.js`.

### 4. Try it
Open `http://localhost:3000`, sign up, then open a second browser (or incognito) and sign up as another user to test real-time chat.

---

## 📡 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/user/register` | No | Create an account |
| POST | `/api/v1/user/login` | No | Log in (sets cookie) |
| GET  | `/api/v1/user/logout` | No | Log out |
| POST | `/api/v1/user/profile/update` | Yes | Update name, photo, gender, status |
| GET  | `/api/v1/user/` | Yes | Get all other users |
| POST | `/api/v1/message/send/:id` | Yes | Send a message (text/image/file) |
| GET  | `/api/v1/message/:id` | Yes | Get conversation messages |

**Socket.IO events:** `getOnlineUsers` (presence), `newMessage` (live delivery).

---

## ☁️ Deployment

- **Frontend → Vercel** (Root Directory: `frontend`)
- **Backend → Render** (Root Directory: `backend`, Start Command: `npm start`)
- **Database → MongoDB Atlas** (Network Access: allow `0.0.0.0/0`)
- **Media → Cloudinary** (add the 3 Cloudinary env vars)

### Production checklist
- Set `BASE_URL` (frontend `src/index.js`) to your deployed backend URL (https).
- Update the **CORS origin** in `backend/index.js` and `backend/socket/socket.js` to your Vercel URL.
- For cross-domain cookies (HTTPS), set the auth cookie to `secure: true` and `sameSite: "none"`.
- Add all backend env vars on Render; add frontend env/config on Vercel.

---

## 👤 Author

**Shaziya** — [GitHub](https://github.com/Shaziyahackathon1234)

---

## 📄 Documentation

Detailed PDFs are available in the [`docs/`](docs/) folder:
- `ChatWave-Full-Documentation.pdf` — complete 40-page guide
- `Redux-Flow-Explained.pdf` — frontend state flow
- `Backend-Flow-Explained.pdf` — server & API flow

---

## 📝 License

This project is licensed under the ISC License.
