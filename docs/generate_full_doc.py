#!/usr/bin/env python3
"""Generate a complete, beginner-friendly documentation PDF (40-50 pages)
covering frontend, backend, redux, database, real-time, media, and a glossary."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    HRFlowable, ListFlowable, ListItem, Image
)
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = os.path.join(os.path.dirname(__file__), "ChatWave-Full-Documentation.pdf")

_AR = "/System/Library/Fonts/Supplemental/Arial.ttf"
_ARB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_ARI = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
pdfmetrics.registerFont(TTFont("Sans", _AR))
pdfmetrics.registerFont(TTFont("Sans-Bold", _ARB))
pdfmetrics.registerFont(TTFont("Sans-Italic", _ARI))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Italic", boldItalic="Sans-Bold")
REG, BOLD, ITAL = "Sans", "Sans-Bold", "Sans-Italic"

BLUE = colors.HexColor("#2563eb")
DARK = colors.HexColor("#0f172a")
GRAY = colors.HexColor("#64748b")
LIGHT = colors.HexColor("#eff6ff")
BORDER = colors.HexColor("#cbd5e1")
CODEBG = colors.HexColor("#f1f5f9")
GREEN = colors.HexColor("#16a34a")

styles = getSampleStyleSheet()
def S(name, **kw): styles.add(ParagraphStyle(name, parent=styles['Normal'], **kw))
S('CTitle', fontName=BOLD, fontSize=32, textColor=DARK, alignment=TA_CENTER, leading=38)
S('CSub', fontName=REG, fontSize=15, textColor=BLUE, alignment=TA_CENTER, leading=22)
S('CSmall', fontName=REG, fontSize=10.5, textColor=GRAY, alignment=TA_CENTER, leading=16)
S('Ch', fontName=BOLD, fontSize=20, textColor=BLUE, spaceBefore=4, spaceAfter=10, leading=24)
S('H1', fontName=BOLD, fontSize=15, textColor=DARK, spaceBefore=14, spaceAfter=6, leading=19)
S('H2', fontName=BOLD, fontSize=12, textColor=BLUE, spaceBefore=8, spaceAfter=3, leading=15)
S('Body', fontName=REG, fontSize=10.3, textColor=DARK, leading=15.5, spaceAfter=6)
S('Bul', fontName=REG, fontSize=10.3, textColor=DARK, leading=14.5)
S('CodeB', fontName="Courier", fontSize=8.6, textColor=DARK, leading=12.2, backColor=CODEBG,
  borderPadding=(7,7,7,7), spaceBefore=3, spaceAfter=7)
S('Cell', fontName=REG, fontSize=8.8, textColor=DARK, leading=12)
S('CellB', fontName=BOLD, fontSize=8.8, textColor=colors.white, leading=12)
S('TOC', fontName=REG, fontSize=11, textColor=DARK, leading=20)
S('Note', fontName=ITAL, fontSize=9.5, textColor=GRAY, leading=14, spaceAfter=6)

story = []
def ch(t): story.append(Paragraph(t, styles['Ch']))
def h1(t): story.append(Paragraph(t, styles['H1']))
def h2(t): story.append(Paragraph(t, styles['H2']))
def p(t): story.append(Paragraph(t, styles['Body']))
def note(t): story.append(Paragraph(t, styles['Note']))
def sp(h=8): story.append(Spacer(1, h))
def pb(): story.append(PageBreak())
def hr(): story.append(HRFlowable(width="100%", thickness=0.8, color=BORDER)); sp(6)
def code(t): story.append(Paragraph(t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>").replace(" ","&nbsp;"), styles['CodeB']))
def bullets(items):
    story.append(ListFlowable([ListItem(Paragraph(i, styles['Bul']), leftIndent=10) for i in items],
        bulletColor=BLUE, bulletFontSize=7, leftIndent=12, bulletType='bullet')); sp(6)
def table(data, widths):
    rows=[[Paragraph(str(c), styles['CellB' if r==0 else 'Cell']) for c in row] for r,row in enumerate(data)]
    t=Table(rows, colWidths=widths, repeatRows=1)
    ts=[('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('BACKGROUND',(0,0),(-1,0),BLUE),('BOX',(0,0),(-1,-1),0.5,BORDER),('LINEBELOW',(0,0),(-1,-1),0.5,BORDER)]
    for r in range(1,len(data)):
        if r%2==0: ts.append(('BACKGROUND',(0,r),(-1,r),LIGHT))
    t.setStyle(TableStyle(ts)); story.append(t); sp(8)
def flow(steps, color=BLUE):
    cells=[Paragraph(s, ParagraphStyle('f', parent=styles['Normal'], fontName=BOLD, fontSize=7.6,
            textColor=colors.white, alignment=TA_CENTER, leading=9.5)) for s in steps]
    t=Table([cells], colWidths=[(17.0/len(steps))*cm]*len(steps))
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),color),('TOPPADDING',(0,0),(-1,-1),7),
        ('BOTTOMPADDING',(0,0),(-1,-1),7),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),
        ('LINEAFTER',(0,0),(-2,-1),1,colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(t); sp(8)
def deflist(pairs):
    # term -> definition list
    for term, d in pairs:
        story.append(Paragraph(f"<b>{term}</b> — {d}", styles['Bul'])); sp(3)
    sp(4)
SHOTS = os.path.join(os.path.dirname(__file__), "_shots")
def shot(filename, caption):
    path = os.path.join(SHOTS, filename)
    if not os.path.exists(path): return
    iw, ih = PILImage.open(path).size
    w = 16.5*cm
    h = w * ih / iw
    story.append(Image(path, width=w, height=h))
    story.append(Paragraph(caption, ParagraphStyle('cap', parent=styles['Normal'], fontName=ITAL,
        fontSize=9, textColor=GRAY, alignment=TA_CENTER, spaceBefore=4, spaceAfter=14)))

# ============ COVER ============
sp(150)
story.append(Paragraph("ChatWave", styles['CTitle']))
sp(6)
story.append(Paragraph("Complete Project Documentation", styles['CSub']))
sp(24)
story.append(Paragraph("A full, beginner-friendly guide to the Real-Time Chat Application —<br/>"
    "frontend, backend, Redux, database, real-time messaging, media uploads,<br/>"
    "with the definition of every concept used.", styles['CSmall']))
sp(40)
story.append(Paragraph("MERN Stack · React · Redux Toolkit · Node/Express · MongoDB · Socket.IO · Cloudinary", styles['CSmall']))
pb()

# ============ TABLE OF CONTENTS ============
ch("Table of Contents")
toc = [
    "1.  Introduction",
    "2.  Technology Stack (with definitions)",
    "3.  High-Level Architecture",
    "4.  Project Folder Structure",
    "5.  Frontend — Entry & Routing",
    "6.  Frontend — Pages",
    "7.  Frontend — Components",
    "8.  Frontend — Utilities & Hooks",
    "9.  Redux State Management (full flow)",
    "10. Backend — Server & Middleware",
    "11. Backend — Routes & Controllers",
    "12. Database Design (models & relationships)",
    "13. Authentication & Security",
    "14. Real-Time Messaging (Socket.IO)",
    "15. Media Uploads (images & files / Cloudinary)",
    "16. Complete API Reference",
    "17. End-to-End Data Flows",
    "18. Feature Walkthroughs",
    "19. Environment Variables",
    "20. Deployment Guide",
    "21. Annotated Source Code (frontend & backend)",
    "22. Glossary (every term defined)",
    "23. UI Gallery (screenshots)",
    "24. FAQ — common questions",
    "25. Getting Started — Setup & Run",
    "26. Testing the Application",
    "27. Troubleshooting & Common Errors",
    "28. Best Practices & Future Improvements",
    "29. Appendix — Component Reference",
    "30. Visual Sequence Diagrams",
]
for t in toc:
    story.append(Paragraph(t, styles['TOC']))
pb()

# ============ 1. INTRODUCTION ============
ch("1. Introduction")
p("<b>ChatWave</b> is a real-time one-to-one chat application built on the <b>MERN</b> stack "
  "(MongoDB, Express, React, Node.js) with <b>Socket.IO</b> for live messaging. Users can register, "
  "log in, see other users, chat in real time, send images and files, manage their profile, and control "
  "whether others can see their online status.")
h1("What you can do in the app")
bullets([
    "<b>Register & log in</b> securely (passwords hashed, sessions via cookies).",
    "<b>See all other users</b> with live online/offline presence.",
    "<b>Chat in real time</b> — messages appear instantly without refreshing.",
    "<b>Send images and documents</b> as attachments.",
    "<b>Manage your profile</b> — change name, gender, photo, and status visibility.",
    "<b>Stay logged in</b> across refreshes (state is persisted).",
])
h1("Who this document is for")
p("This guide is written for beginners. Every technical term is explained in plain English the first time "
  "it appears, and again in the <b>Glossary</b> (Section 21). Read it top to bottom, or jump to a section "
  "using the Table of Contents.")
h1("The two halves of the app")
table([
    ["Half", "Folder", "Job"],
    ["Frontend (client)", "frontend/", "What the user sees and clicks (React)."],
    ["Backend (server)", "backend/", "Logic, database, and real-time engine (Node/Express)."],
], [4*cm, 3.2*cm, 8.3*cm])
p("They talk to each other over <b>HTTP</b> (normal requests) and a <b>WebSocket</b> (live connection).")
pb()

# ============ 2. TECH STACK ============
ch("2. Technology Stack (with definitions)")
p("Here is every major technology used, what it <i>is</i>, and why this project uses it.")
h1("Frontend technologies")
table([
    ["Technology", "What it is", "Why we use it"],
    ["React", "A JavaScript library for building user interfaces from reusable components.", "Builds the whole UI."],
    ["Create React App", "A ready-made React project setup and build tool.", "Runs & bundles the app."],
    ["Redux Toolkit", "The official, simple way to use Redux — a central state container.", "Shares data app-wide."],
    ["redux-persist", "Saves the Redux state to browser storage and restores it.", "Keeps you logged in."],
    ["React Router", "Handles navigation between pages without reloading.", "Login / Signup / Home routes."],
    ["Tailwind CSS", "A utility-class CSS framework for styling.", "All the styling."],
    ["daisyUI", "Prebuilt UI components on top of Tailwind.", "Some base UI pieces."],
    ["Axios", "A library to make HTTP requests.", "Calls the backend APIs."],
    ["socket.io-client", "The browser side of Socket.IO.", "Receives live messages."],
    ["react-hot-toast", "Small popup notifications (toasts).", "Success / error messages."],
    ["react-icons", "A big icon set as React components.", "All the icons."],
], [3.3*cm, 8.2*cm, 4*cm])
h1("Backend technologies")
table([
    ["Technology", "What it is", "Why we use it"],
    ["Node.js", "A runtime that lets JavaScript run on a server.", "Runs the backend."],
    ["Express", "A minimal web framework for Node.", "Routes & HTTP server."],
    ["MongoDB", "A NoSQL document database (stores JSON-like data).", "Stores users & messages."],
    ["Mongoose", "An ODM that models MongoDB data with schemas.", "Defines & queries data."],
    ["JWT", "JSON Web Token — a signed token proving identity.", "Login sessions."],
    ["bcryptjs", "A library to hash (scramble) passwords.", "Secure passwords."],
    ["cookie-parser", "Reads cookies from incoming requests.", "Reads the auth cookie."],
    ["cors", "Controls which websites may call the API.", "Allows the frontend."],
    ["Socket.IO", "Real-time, two-way communication over WebSockets.", "Live messaging & presence."],
    ["Cloudinary", "Cloud media hosting & delivery.", "Stores uploaded images/files."],
    ["dotenv", "Loads secrets from a .env file into the app.", "Keys & config."],
], [3.3*cm, 8.2*cm, 4*cm])
pb()

# ============ 3. ARCHITECTURE ============
ch("3. High-Level Architecture")
p("At the highest level, data flows like this:")
flow(["Browser (React)", "HTTP (Axios)", "Express API", "Mongoose", "MongoDB"])
sp(2)
flow(["Browser (Socket.IO)", "WebSocket", "Socket.IO Server", "Other Browsers"], color=GREEN)
h1("How the pieces cooperate")
bullets([
    "The <b>React</b> app renders the UI and holds shared data in the <b>Redux</b> store.",
    "For normal actions (login, fetch users, send a message), it calls the <b>Express</b> API with <b>Axios</b>.",
    "Express runs <b>middleware</b> (security checks), then a <b>controller</b> (logic), which uses <b>Mongoose</b> to read/write <b>MongoDB</b>.",
    "For live updates, a <b>Socket.IO</b> connection stays open; the server pushes new messages and the online-user list instantly.",
    "Uploaded media is sent to <b>Cloudinary</b> and only its URL is stored in the database.",
])
note("Think of HTTP as sending letters (request → reply), and the WebSocket as a phone call that stays connected so either side can talk at any time.")
pb()

# ============ 4. FOLDER STRUCTURE ============
ch("4. Project Folder Structure")
h1("Frontend (frontend/src)")
code("src/\n"
     "  index.js          # app entry; BASE_URL; Redux Provider + PersistGate\n"
     "  App.js            # routes (/, /login, /signup); socket setup\n"
     "  index.css         # global styles (Tailwind)\n"
     "  components/       # all UI pieces (see Section 7)\n"
     "  redux/            # store + slices (user, message, socket)\n"
     "  hooks/            # data-fetching hooks\n"
     "  utils/            # avatar + helpers")
h1("Backend (backend/)")
code("backend/\n"
     "  index.js          # server start, middleware, mount routes\n"
     "  config/           # database.js (Mongo), cloudinary.js (uploads)\n"
     "  routes/           # userRoute.js, messageRoute.js\n"
     "  controllers/      # userController.js, messageController.js\n"
     "  middleware/       # isAuthenticated.js (JWT check)\n"
     "  models/           # userModel, messageModel, conversationModel\n"
     "  socket/           # socket.js (Socket.IO server)")
p("Each folder has one clear job. This separation (routes vs controllers vs models) is called a "
  "<b>layered architecture</b> and keeps code easy to find and change.")
pb()

# ============ 5. FRONTEND ENTRY & ROUTING ============
ch("5. Frontend — Entry & Routing")
h1("index.js — the starting point")
p("This file mounts React into the page and wraps the app with three providers:")
bullets([
    "<b>Provider</b> (react-redux) — gives every component access to the Redux store.",
    "<b>PersistGate</b> — waits for the saved state to load before showing the app.",
    "<b>Toaster</b> — enables the popup notifications.",
])
p("It also exports <b>BASE_URL</b>, the address of the backend, used by every API call.")
code('export const BASE_URL = "http://localhost:8080"')
h1("App.js — routing & socket")
p("App.js defines the pages with <b>React Router</b>:")
table([
    ["Path", "Component", "Purpose"],
    ["/", "HomePage", "The chat screen (must be logged in)."],
    ["/login", "Login", "Sign in."],
    ["/signup", "Signup", "Create an account."],
], [3*cm, 4.5*cm, 8*cm])
p("It also opens the <b>Socket.IO</b> connection when you are logged in, and listens for the "
  "<b>getOnlineUsers</b> event to know who is online. When you log out, it closes the socket.")
pb()

# ============ 6. PAGES ============
ch("6. Frontend — Pages")
h1("Login")
bullets([
    "Collects username & password; toggles password visibility with an eye icon.",
    "Calls POST /api/v1/user/login.",
    "On success: saves you with <b>dispatch(setAuthUser(...))</b> and navigates to /.",
    "On failure: shows a red toast 'Incorrect username or password'.",
])
h1("Signup")
bullets([
    "Collects full name, username, password, confirm password, and gender (single-select).",
    "Calls POST /api/v1/user/register; on success navigates to /login.",
    "Left side shows the welcome panel (AuthWelcome) describing the app's features.",
])
h1("HomePage")
bullets([
    "Guards the route: if not logged in (no authUser), it redirects to /login.",
    "Lays out the <b>Sidebar</b> (40% width) and the <b>MessageContainer</b> (60%).",
])
pb()

# ============ 7. COMPONENTS ============
ch("7. Frontend — Components")
comp = [
    ("AuthWelcome", "The blue feature panel on the Login/Signup pages (brand + highlights)."),
    ("Sidebar", "Your profile header, search, the user list, and the red Logout button."),
    ("OtherUsers", "Fetches and lists all other users (uses the useGetOtherUsers hook)."),
    ("OtherUser", "A single user row: avatar, name, and online/offline status; click to open that chat."),
    ("MessageContainer", "The right side: chat header (with the friend's profile), messages, and the input."),
    ("Messages", "Scrolls and renders all messages; wires up live updates."),
    ("Message", "One message bubble — supports text, an image, or a file attachment."),
    ("SendInput", "The composer: text box, attach (paperclip) button, and send button."),
    ("ProfileModal", "Popup showing a user's details (username, gender, joined date, status). Your own profile is editable."),
]
deflist(comp)
h1("How a click becomes a chat")
flow(["Click OtherUser", "setSelectedUser", "MessageContainer reads it", "useGetMessages loads history"])
pb()

# ============ 8. UTILS & HOOKS ============
ch("8. Frontend — Utilities & Hooks")
h1("utils/avatar.js")
bullets([
    "<b>defaultAvatar(user)</b> — builds a colored circle with the user's initials (an SVG), so an avatar always shows.",
    "<b>avatarSrc(user)</b> — uses an uploaded photo if present, otherwise the initials avatar.",
    "<b>avatarOnError(user)</b> — if a photo fails to load, falls back to the initials avatar.",
])
h1("utils/helpers.js")
bullets([
    "<b>formatJoined(iso)</b> — turns a stored date into a friendly '25 May 2026'.",
    "<b>isUserOnline(user, onlineUsers)</b> — true only if the user is connected AND hasn't hidden their status.",
])
h1("Hooks (reusable data logic)")
table([
    ["Hook", "What it does"],
    ["useGetOtherUsers", "On load, GET /user and store the list with setOtherUsers."],
    ["useGetMessages", "When you open a chat, GET /message/:id and store with setMessages."],
    ["useGetRealTimeMessage", "Listens to the socket 'newMessage' event and appends it with setMessages."],
], [4.6*cm, 10.9*cm])
note("A 'hook' is a reusable function (name starts with 'use') that adds behavior to a component.")
pb()

# ============ 9. REDUX ============
ch("9. Redux State Management (full flow)")
p("<b>Redux</b> is a central box (the <b>store</b>) that holds shared data. Components <b>read</b> it with "
  "<b>useSelector</b> and <b>change</b> it by <b>dispatching</b> actions. When the data changes, the components "
  "using it re-render automatically.")
h1("The golden loop")
flow(["Component", "dispatch(action)", "Reducer updates store", "useSelector re-renders"])
h1("Your store")
code("store = {\n  user:    { authUser, otherUsers, selectedUser, onlineUsers },\n  message: { messages },\n  socket:  { socket }\n}")
h1("The three slices")
table([
    ["Slice", "State", "Actions"],
    ["userSlice", "authUser, otherUsers, selectedUser, onlineUsers", "setAuthUser, setOtherUsers, setSelectedUser, setOnlineUsers"],
    ["messageSlice", "messages", "setMessages"],
    ["socketSlice", "socket", "setSocket"],
], [3*cm, 6.5*cm, 6*cm])
h1("Key terms defined")
deflist([
    ("Store", "The single object holding all shared state."),
    ("Slice", "A named part of the store plus the functions that change it."),
    ("Action", "A plain instruction describing a change (e.g. setMessages)."),
    ("Reducer", "The function that applies an action to the state."),
    ("dispatch", "How a component sends an action to the store."),
    ("useSelector", "How a component reads a value from the store."),
    ("redux-persist", "Saves the store to localStorage so a refresh keeps your data."),
])
pb()

# ============ 10. BACKEND SERVER ============
ch("10. Backend — Server & Middleware")
h1("index.js")
bullets([
    "Loads env vars with dotenv and connects to MongoDB.",
    "Registers global <b>middleware</b>: express.json (parse bodies), cookieParser (read cookies), cors (allow the frontend).",
    "Mounts the routers under /api/v1/user and /api/v1/message.",
    "Starts the combined HTTP + Socket.IO server with server.listen.",
])
h1("What is middleware?")
p("<b>Middleware</b> is a function that runs <i>between</i> the request arriving and the controller answering. "
  "It can inspect or modify the request, then call <b>next()</b> to continue. Examples here: JSON parsing, "
  "cookie reading, CORS, and the authentication check.")
h1("isAuthenticated middleware")
code('const token = req.cookies.token;\nif(!token) return res.status(401).json({message:"User not authenticated."});\nconst decode = jwt.verify(token, SECRET);\nreq.id = decode.userId;   // controllers now know who you are\nnext();')
pb()

# ============ 11. ROUTES & CONTROLLERS ============
ch("11. Backend — Routes & Controllers")
h1("Routes map URLs to controllers")
code('// userRoute.js\nrouter.post("/register", register)\nrouter.post("/login", login)\nrouter.get("/logout", logout)\nrouter.post("/profile/update", isAuthenticated, updateProfile)\nrouter.get("/", isAuthenticated, getOtherUsers)\n\n// messageRoute.js\nrouter.post("/send/:id", isAuthenticated, sendMessage)\nrouter.get("/:id", isAuthenticated, getMessage)')
h1("User controller functions")
deflist([
    ("register", "Validates input, hashes the password (bcrypt), creates the user, returns success."),
    ("login", "Checks the password, signs a JWT, sets it as an httpOnly cookie, returns your profile."),
    ("logout", "Clears the cookie."),
    ("updateProfile", "Updates your name, photo, gender, or status visibility."),
    ("getOtherUsers", "Returns every user except you (without passwords)."),
])
h1("Message controller functions")
deflist([
    ("sendMessage", "Finds or creates the conversation, uploads any attachment, creates the Message, saves it, and pushes it live via Socket.IO."),
    ("getMessage", "Finds the conversation between the two users and returns all its messages (populated)."),
])
pb()

# ============ 12. DATABASE ============
ch("12. Database Design (models & relationships)")
p("Data is stored in <b>MongoDB</b> as documents. <b>Mongoose schemas</b> define the shape of each document.")
h1("User")
table([
    ["Field", "Type", "Notes"],
    ["fullName", "String", "Required."],
    ["username", "String", "Required, unique."],
    ["password", "String", "Required, stored hashed."],
    ["profilePhoto", "String", "Photo URL or uploaded image."],
    ["gender", "String", "'male' or 'female'."],
    ["showStatus", "Boolean", "If false, others can't see your status."],
    ["createdAt / updatedAt", "Date", "Added automatically (timestamps)."],
], [4*cm, 3*cm, 8.5*cm])
h1("Message")
table([
    ["Field", "Type", "Notes"],
    ["senderId", "ObjectId → User", "Who sent it."],
    ["receiverId", "ObjectId → User", "Who receives it."],
    ["message", "String", "The text (may be empty if media only)."],
    ["image", "String", "Image URL, if any."],
    ["fileUrl / fileName", "String", "File link & name, if any."],
], [4*cm, 3.5*cm, 8*cm])
h1("Conversation")
table([
    ["Field", "Type", "Notes"],
    ["participants", "[ObjectId → User]", "The two users."],
    ["messages", "[ObjectId → Message]", "All messages in this chat."],
], [4*cm, 4*cm, 7.5*cm])
h1("Relationships")
flow(["User A", "Conversation (A,B)", "[ Messages ]", "User B"])
p("A <b>Conversation</b> connects two users and references a list of <b>Message</b> documents. The <b>ObjectId</b> "
  "fields are <b>references</b> — like a pointer to another document — which Mongoose can <b>populate</b> "
  "(replace the id with the full document) when loading a chat.")
pb()

# ============ 13. AUTH ============
ch("13. Authentication & Security")
h1("Registration")
flow(["Validate", "bcrypt hash password", "Create user", "Success"])
h1("Login")
flow(["Find user", "bcrypt.compare", "Sign JWT", "Set httpOnly cookie"])
h1("Why these choices are secure")
deflist([
    ("Hashing (bcrypt)", "Passwords are scrambled one-way. Even if the DB leaks, real passwords aren't exposed."),
    ("JWT", "A signed token the server can verify without storing sessions."),
    ("httpOnly cookie", "JavaScript can't read it, which protects the token from many attacks (XSS)."),
    ("isAuthenticated", "Every protected route verifies the cookie before running."),
])
h1("Frontend vs backend 'logged in'")
table([
    ["Question", "Where", "How"],
    ["Show chat or login page?", "Frontend", "Is Redux authUser not null?"],
    ["Is this API call allowed?", "Backend", "Is the JWT cookie valid?"],
], [6*cm, 3*cm, 6.5*cm])
pb()

# ============ 14. SOCKET ============
ch("14. Real-Time Messaging (Socket.IO)")
p("<b>Socket.IO</b> keeps an always-open connection so the server can push data to the browser the instant "
  "it happens — no refresh, no polling.")
h1("On the server (socket/socket.js)")
bullets([
    "When a user connects, save <b>userId → socketId</b> in a map (userSocketMap).",
    "Broadcast <b>getOnlineUsers</b> (all online ids) to everyone.",
    "<b>getReceiverSocketId(id)</b> finds a specific user's socket so a message goes only to them.",
    "On disconnect, remove the user and broadcast the updated online list.",
])
h1("On the client")
bullets([
    "App.js opens the socket when you log in and stores it in Redux (setSocket).",
    "It listens for <b>getOnlineUsers</b> → setOnlineUsers (green dots).",
    "useGetRealTimeMessage listens for <b>newMessage</b> → setMessages (live bubble).",
])
flow(["Sender sends", "Server saves", "emit newMessage", "Receiver sees instantly"], color=GREEN)
pb()

# ============ 15. MEDIA ============
ch("15. Media Uploads (images & files)")
p("Attachments (images, PDFs, docs) are handled like this:")
flow(["Pick file", "Read as base64", "POST to API", "Upload to Cloudinary", "Store URL"])
h1("Step by step")
bullets([
    "In <b>SendInput</b>, the paperclip opens a file picker; the file is read into a base64 <b>data URI</b>.",
    "It's sent to <b>sendMessage</b> as 'media' (plus 'fileName').",
    "The server's <b>uploadMedia</b> helper sends it to <b>Cloudinary</b> and stores the returned URL in the message (image or fileUrl).",
    "The <b>Message</b> component shows images inline and files as a downloadable chip.",
])
h1("Smart fallback")
p("If Cloudinary keys are not set, <b>uploadMedia</b> simply stores the data URI directly, so sending still "
  "works in development. Add the keys (Section 19) to switch to real hosting — no code change needed.")
deflist([
    ("base64 / data URI", "A way to embed a file's bytes as a text string the browser can read directly."),
    ("Cloudinary", "A cloud service that stores media and returns a fast public URL."),
])
pb()

# ============ 16. API REFERENCE ============
ch("16. Complete API Reference")
table([
    ["Method", "Endpoint", "Auth", "Body / Params", "Returns"],
    ["POST", "/api/v1/user/register", "No", "fullName, username, password, confirmPassword, gender", "success message"],
    ["POST", "/api/v1/user/login", "No", "username, password", "your profile + sets cookie"],
    ["GET", "/api/v1/user/logout", "No", "—", "clears cookie"],
    ["POST", "/api/v1/user/profile/update", "Yes", "fullName, profilePhoto, gender, showStatus", "updated user"],
    ["GET", "/api/v1/user/", "Yes", "—", "list of other users"],
    ["POST", "/api/v1/message/send/:id", "Yes", "message, media, fileName", "the new message"],
    ["GET", "/api/v1/message/:id", "Yes", "id = other user", "all messages"],
], [1.6*cm, 5.3*cm, 1.1*cm, 4.2*cm, 3.3*cm])
note("Auth = requires a valid login cookie (the isAuthenticated middleware).")
pb()

# ============ 17. END TO END FLOWS ============
ch("17. End-to-End Data Flows")
h1("A) Registration")
flow(["Fill form", "POST register", "Hash + save", "Go to login"])
h1("B) Login")
flow(["POST login", "Verify + JWT cookie", "setAuthUser", "Show chat"])
h1("C) Loading the app")
bullets([
    "useGetOtherUsers → GET /user → setOtherUsers (sidebar fills).",
    "Socket connects → setSocket; server sends online list → setOnlineUsers.",
])
h1("D) Opening a chat & messaging")
flow(["setSelectedUser", "GET messages", "Type/attach", "POST send", "socket newMessage"])
h1("E) Editing profile / hiding status")
flow(["Open profile", "Edit + Save", "POST profile/update", "setAuthUser"])
h1("F) Logout")
flow(["Click Logout", "GET logout", "Clear cookie", "setAuthUser(null)"])
pb()

# ============ 18. FEATURES ============
ch("18. Feature Walkthroughs")
h1("Online status privacy")
p("Each user has <b>showStatus</b>. If you turn it off in your profile, <b>isUserOnline</b> returns false for "
  "you on everyone else's screen — so no one sees your green dot, even though you're connected. You still see "
  "your own real status.")
h1("Default avatars")
p("If a user hasn't uploaded a photo, the app generates a colored circle with their initials, so the UI never "
  "shows a blank avatar.")
h1("Profile (view & edit)")
bullets([
    "Click your own profile → view details → Edit → change name, gender, photo (from device), status.",
    "Click a friend's header or the info icon → view their photo, username, gender, and joined date.",
])
h1("Persisted login")
p("redux-persist saves the store to localStorage, so refreshing the page keeps you logged in and remembers "
  "the open chat.")
pb()

# ============ 19. ENV ============
ch("19. Environment Variables")
h1("Backend (backend/.env)")
table([
    ["Variable", "Purpose"],
    ["PORT", "Port the server runs on (e.g. 8080)."],
    ["MONGO_URI", "MongoDB connection string."],
    ["JWT_SECRET_KEY", "Secret used to sign/verify JWT tokens."],
    ["CLOUDINARY_CLOUD_NAME", "Cloudinary account name (optional)."],
    ["CLOUDINARY_API_KEY", "Cloudinary API key (optional)."],
    ["CLOUDINARY_API_SECRET", "Cloudinary API secret (optional)."],
], [6.5*cm, 9*cm])
h1("Frontend")
p("<b>BASE_URL</b> in src/index.js points to the backend (http://localhost:8080 in development).")
note("Cloudinary variables are optional — without them, media is stored inline as a fallback.")
pb()

# ============ 20. DEPLOYMENT ============
ch("20. Deployment Guide")
h1("Recommended setup")
table([
    ["Layer", "Platform", "Notes"],
    ["Frontend", "Vercel / Netlify", "Build with 'npm run build'."],
    ["Backend", "Render / Railway", "Start with 'npm start'."],
    ["Database", "MongoDB Atlas", "Allow access from anywhere (0.0.0.0/0)."],
    ["Media", "Cloudinary", "Add the 3 Cloudinary env vars."],
], [3.5*cm, 5*cm, 7*cm])
h1("Things to change for production")
bullets([
    "Point <b>BASE_URL</b> (frontend) to the deployed backend URL (https).",
    "Update <b>CORS origin</b> (backend) to the deployed frontend URL.",
    "Update the Socket.IO cors origin to the deployed frontend URL.",
    "Cookies: use secure + sameSite 'none' so they work across domains (HTTPS).",
])
pb()

# ============ 21. ANNOTATED SOURCE CODE ============
ch("21. Annotated Source Code")
p("This chapter walks through the most important files with the real code and a short explanation of what "
  "each part does. Read the explanation first, then the code.")

h1("Frontend · src/index.js")
p("Boots the React app and wires Redux + persistence + toasts. Exports the backend address.")
code('export const BASE_URL = "http://localhost:8080";\n\n'
     'let persistor = persistStore(store);\n'
     'root.render(\n'
     '  <Provider store={store}>\n'
     '    <PersistGate loading={null} persistor={persistor}>\n'
     '      <App />\n'
     '      <Toaster />\n'
     '    </PersistGate>\n'
     '  </Provider>\n'
     ');')
note("Provider shares the store; PersistGate restores saved state; Toaster enables notifications.")

h1("Frontend · src/App.js (routing + socket)")
p("Defines the three routes and opens the Socket.IO connection when logged in.")
code('const router = createBrowserRouter([\n'
     '  { path:"/", element:<HomePage/> },\n'
     '  { path:"/signup", element:<Signup/> },\n'
     '  { path:"/login", element:<Login/> },\n'
     ']);\n\n'
     'useEffect(() => {\n'
     '  if (authUser) {\n'
     '    const s = io(BASE_URL, { query:{ userId: authUser._id } });\n'
     '    dispatch(setSocket(s));\n'
     '    s.on("getOnlineUsers", (u)=> dispatch(setOnlineUsers(u)));\n'
     '    return () => s.close();\n'
     '  } else if (socket) { socket.close(); dispatch(setSocket(null)); }\n'
     '}, [authUser]);')
pb()

h1("Frontend · redux/store.js")
p("Combines the three slices and wraps them with redux-persist.")
code('const rootReducer = combineReducers({\n'
     '  user: userReducer,\n'
     '  message: messageReducer,\n'
     '  socket: socketReducer,\n'
     '});\n'
     'const persistedReducer = persistReducer({key:"root", version:1, storage}, rootReducer);\n'
     'const store = configureStore({ reducer: persistedReducer, /* ignore socket in serialize check */ });')

h1("Frontend · redux/userSlice.js")
p("Holds the core user state and the setters that change it.")
code('initialState: { authUser:null, otherUsers:null, selectedUser:null, onlineUsers:null }\n\n'
     'reducers: {\n'
     '  setAuthUser:     (s,a)=> { s.authUser = a.payload; },\n'
     '  setOtherUsers:   (s,a)=> { s.otherUsers = a.payload; },\n'
     '  setSelectedUser: (s,a)=> { s.selectedUser = a.payload; },\n'
     '  setOnlineUsers:  (s,a)=> { s.onlineUsers = a.payload; },\n'
     '}')

h1("Frontend · redux/messageSlice.js & socketSlice.js")
code('// messageSlice\ninitialState: { messages:null }\nsetMessages: (s,a)=> { s.messages = a.payload; }\n\n'
     '// socketSlice\ninitialState: { socket:null }\nsetSocket: (s,a)=> { s.socket = a.payload; }')
pb()

h1("Frontend · hooks")
p("Three small hooks fetch data and push it into Redux.")
code('// useGetOtherUsers — on mount\nconst res = await axios.get(`${BASE_URL}/api/v1/user`);\ndispatch(setOtherUsers(res.data));\n\n'
     '// useGetMessages — when selectedUser changes\nconst res = await axios.get(`${BASE_URL}/api/v1/message/${selectedUser._id}`);\ndispatch(setMessages(res.data));\n\n'
     '// useGetRealTimeMessage — live\nsocket?.on("newMessage", (m)=> dispatch(setMessages([...messages, m])));')

h1("Frontend · components/SendInput.jsx (sending text + media)")
code('const reader = new FileReader();\nreader.onloadend = () => { setMedia(reader.result); setFileName(file.name); };\nreader.readAsDataURL(file);\n\n'
     'await axios.post(`${BASE_URL}/api/v1/message/send/${selectedUser._id}`,\n'
     '  { message, media, fileName }, { withCredentials:true });')

h1("Frontend · components/Message.jsx (rendering a bubble)")
code('{message.image && <img src={message.image} .../>}\n'
     '{message.fileUrl && <a href={message.fileUrl} download>{message.fileName}</a>}\n'
     '{message.message && <div className="bubble">{message.message}</div>}')
pb()

h1("Backend · middleware/isAuthenticated.js")
p("Guards protected routes by verifying the JWT cookie.")
code('const token = req.cookies.token;\n'
     'if(!token) return res.status(401).json({message:"User not authenticated."});\n'
     'const decode = jwt.verify(token, process.env.JWT_SECRET_KEY);\n'
     'req.id = decode.userId;\n'
     'next();')

h1("Backend · controllers/userController.js — register & login")
code('// register\nconst hashed = await bcrypt.hash(password, 10);\nawait User.create({ fullName, username, password:hashed, gender, profilePhoto });\n\n'
     '// login\nconst ok = await bcrypt.compare(password, user.password);\nif(!ok) return res.status(400).json({message:"Incorrect username or password"});\n'
     'const token = jwt.sign({userId:user._id}, SECRET, {expiresIn:"1d"});\n'
     'res.cookie("token", token, { httpOnly:true, sameSite:"strict" }).json(user);')
pb()

h1("Backend · controllers/messageController.js — sendMessage")
code('const { message, media, fileName } = req.body;\n'
     'let image="", fileUrl="", fName="";\n'
     'if (media) {\n'
     '  const url = await uploadMedia(media);  // Cloudinary or inline fallback\n'
     '  if (media.startsWith("data:image")) image = url;\n'
     '  else { fileUrl = url; fName = fileName; }\n'
     '}\n'
     'const newMessage = await Message.create({ senderId, receiverId, message, image, fileUrl, fileName:fName });\n'
     'conversation.messages.push(newMessage._id); await conversation.save();\n\n'
     'const sid = getReceiverSocketId(receiverId);\n'
     'if (sid) io.to(sid).emit("newMessage", newMessage);   // live delivery')

h1("Backend · socket/socket.js")
code('const userSocketMap = {};   // userId -> socketId\n'
     'io.on("connection", (socket) => {\n'
     '  const userId = socket.handshake.query.userId;\n'
     '  if (userId) userSocketMap[userId] = socket.id;\n'
     '  io.emit("getOnlineUsers", Object.keys(userSocketMap));\n'
     '  socket.on("disconnect", () => {\n'
     '    delete userSocketMap[userId];\n'
     '    io.emit("getOnlineUsers", Object.keys(userSocketMap));\n'
     '  });\n'
     '});\n'
     'export const getReceiverSocketId = (id) => userSocketMap[id];')

h1("Backend · config/cloudinary.js (upload with fallback)")
code('export const uploadMedia = async (dataUri) => {\n'
     '  const c = await getCloudinary();         // null if not configured\n'
     '  if (!c) return dataUri;                  // fallback: store inline\n'
     '  const res = await c.uploader.upload(dataUri, { resource_type:"auto" });\n'
     '  return res.secure_url;                   // hosted URL\n'
     '};')
pb()

# ============ 22. GLOSSARY ============
ch("22. Glossary — every term defined")
glossary = [
    ("API", "A set of URLs the frontend calls to get or change data."),
    ("Axios", "A library for making HTTP requests from the browser."),
    ("Backend", "The server side: logic, database, and APIs."),
    ("base64 / data URI", "A file encoded as a text string the browser can use directly."),
    ("bcrypt", "A library that hashes passwords securely."),
    ("Component", "A reusable, self-contained piece of UI in React."),
    ("Controller", "A backend function with the logic for a specific request."),
    ("Cookie", "A small piece of data the browser stores and sends back to the server."),
    ("CORS", "A rule controlling which websites may call your API."),
    ("Dispatch", "Sending an action to the Redux store to change state."),
    ("Frontend", "The client side the user sees and interacts with."),
    ("Hashing", "One-way scrambling of data (used for passwords)."),
    ("Hook", "A reusable function (use…) that adds behavior to a component."),
    ("HTTP", "The request/response protocol used for normal web calls."),
    ("httpOnly cookie", "A cookie JavaScript cannot read — safer for tokens."),
    ("JWT", "A signed token that proves who you are."),
    ("Middleware", "Code that runs between a request and its controller."),
    ("MongoDB", "A NoSQL database storing JSON-like documents."),
    ("Mongoose", "A tool to define schemas and query MongoDB."),
    ("ObjectId", "MongoDB's unique id; used to reference other documents."),
    ("ODM", "Object Data Modelling — maps code objects to DB documents."),
    ("populate", "Replacing a referenced id with the full document."),
    ("Props", "Inputs passed into a React component."),
    ("Reducer", "A function that updates state in response to an action."),
    ("Redux", "A central store for app-wide shared state."),
    ("redux-persist", "Saves/restores the Redux store from browser storage."),
    ("Route", "A mapping from a URL to code (page on frontend, controller on backend)."),
    ("Schema", "The defined shape/fields of a database document."),
    ("Selector (useSelector)", "Reads a value from the Redux store."),
    ("Slice", "A named section of the Redux store + its reducers."),
    ("Socket.IO", "Real-time two-way communication over WebSockets."),
    ("State", "Data that can change over time and drives the UI."),
    ("Token", "A string proving identity (here, a JWT)."),
    ("WebSocket", "A persistent connection allowing instant two-way data."),
]
deflist(glossary)
sp(6); hr()
p("<b>The end.</b> You now have a complete picture of ChatWave — from a button click in the browser, through "
  "Redux and the API, into MongoDB, and back out live over Socket.IO.")

# ============ 23. UI GALLERY ============
pb()
ch("23. UI Gallery")
p("Real screenshots of the finished application.")
shot("login.png", "Login — full-width two-column layout with welcome panel and password show/hide.")
shot("signup.png", "Signup — name, username, password, gender select, with the same welcome panel.")
pb()
shot("chat.png", "Chat — wider sidebar (40/60), initials avatars, online dots, image + file messages, red logout.")
note("Avatars are generated from initials when no photo is uploaded, so they always render.")

# ============ 24. FAQ ============
pb()
ch("24. FAQ — common questions")
faq = [
    ("How does the app know I'm logged in?",
     "The frontend checks the Redux value authUser (not null = logged in). The backend checks the JWT cookie via the isAuthenticated middleware. The frontend decides what to show; the backend decides what to allow."),
    ("Why do I stay logged in after refresh?",
     "redux-persist saves the Redux store to the browser's localStorage and restores it on startup, so authUser is still there."),
    ("Why did a friend appear Offline while online?",
     "That user turned OFF 'Show online status' in their profile (showStatus=false). isUserOnline hides their dot from others. They can turn it back on in Edit Profile."),
    ("Where are uploaded images stored?",
     "If Cloudinary keys are set, on Cloudinary (only the URL is saved in MongoDB). If not, the file is stored inline as a data URI so it still works in development."),
    ("How do messages arrive instantly?",
     "Socket.IO keeps a live connection. When you send, the server emits a 'newMessage' event to the receiver's socket, and their UI appends it immediately."),
    ("How are passwords kept safe?",
     "They are hashed with bcrypt before saving. The original password is never stored, and the token lives in an httpOnly cookie JavaScript can't read."),
    ("How do I add a new API endpoint?",
     "Add a route in routes/, write a controller function in controllers/, and (if it needs login) put isAuthenticated in front of it."),
    ("How do I change the theme color?",
     "The UI uses Tailwind 'blue-600' as the accent. Search the components for 'blue-600' / 'blue-700' and replace with your color."),
]
for q, a in faq:
    h2("Q: " + q)
    p(a)

# ============ 25. GETTING STARTED ============
pb()
ch("25. Getting Started — Setup & Run")
h1("Prerequisites")
bullets([
    "<b>Node.js</b> (v16+) and npm installed.",
    "A <b>MongoDB</b> database — local, or a free MongoDB Atlas cluster.",
    "(Optional) a <b>Cloudinary</b> account for media hosting.",
])
h1("1) Backend setup")
code('cd backend\nnpm install\n# create backend/.env :\nPORT=8080\nMONGO_URI=your_mongodb_connection_string\nJWT_SECRET_KEY=any_long_random_string\n# optional:\nCLOUDINARY_CLOUD_NAME=...\nCLOUDINARY_API_KEY=...\nCLOUDINARY_API_SECRET=...\n\nnpm run dev   # starts the server on PORT')
h1("2) Frontend setup")
code('cd frontend\nnpm install\nnpm start     # opens http://localhost:3000')
h1("3) First run")
bullets([
    "Open http://localhost:3000 — you'll land on the Login page.",
    "Click <b>Sign up</b>, create an account, then log in.",
    "Open a second browser (or incognito) and sign up as another user to test real-time chat.",
])
note("The frontend talks to the backend via BASE_URL in src/index.js (http://localhost:8080 by default).")

# ============ 26. TESTING ============
pb()
ch("26. Testing the Application")
h1("Manual test checklist")
table([
    ["Area", "What to check"],
    ["Signup", "All fields required; gender must be picked; redirects to login."],
    ["Login", "Wrong password shows a red toast; correct login opens chat."],
    ["Presence", "A second logged-in user appears 'Active now' with a green dot."],
    ["Messaging", "Text sends instantly on both sides (real-time)."],
    ["Attachments", "An image shows inline; a file shows a download chip."],
    ["Profile", "Edit name/gender/photo/status saves and updates the UI."],
    ["Status privacy", "Turning status off hides your dot from others."],
    ["Persistence", "Refresh keeps you logged in and on the same chat."],
    ["Logout", "Returns to login; protected pages redirect away."],
], [3.5*cm, 12*cm])
h1("Two-user test (real-time)")
bullets([
    "Browser A: log in as User 1. Browser B (incognito): log in as User 2.",
    "Open each other's chat; send messages both ways — they should appear without refreshing.",
    "Watch the green online dots appear/disappear as you log in/out.",
])

# ============ 27. TROUBLESHOOTING ============
pb()
ch("27. Troubleshooting & Common Errors")
trouble = [
    ("CORS error in the browser console",
     "The backend only allows a specific origin. Make sure the CORS origin in index.js and socket.js matches the frontend URL (http://localhost:3000 in dev)."),
    ("Login works but you're logged out on refresh / 401s",
     "Cookie issue. In development, axios must send credentials (withCredentials:true) and the cookie sameSite must allow it. In production over HTTPS use secure:true + sameSite:'none'."),
    ("Cannot connect to MongoDB",
     "Check MONGO_URI. On Atlas, allow your IP (or 0.0.0.0/0) under Network Access."),
    ("Messages don't appear in real time",
     "Check the socket connects to the correct BASE_URL and that the userId query is passed. Confirm the server logs a connection."),
    ("Image upload seems large / slow",
     "Without Cloudinary, images are stored inline (base64) which is heavy. Add Cloudinary keys to host them and keep the database light."),
    ("Avatar shows blank",
     "Handled: the app falls back to a generated initials avatar. If you still see blank, hard-refresh to clear the old cached bundle."),
    ("Port already in use",
     "Another process uses the port. Stop it, or change PORT (backend) / use a different port for the frontend."),
]
for t, d in trouble:
    h2(t); p(d)

# ============ 28. BEST PRACTICES ============
pb()
ch("28. Best Practices & Future Improvements")
h1("Good practices already used")
bullets([
    "Layered backend (routes → controllers → models) keeps code organized.",
    "Passwords hashed; tokens in httpOnly cookies.",
    "Central state in Redux with a single source of truth.",
    "Reusable hooks and utilities (avatars, helpers).",
])
h1("Ideas to take it further")
bullets([
    "<b>Typing indicators</b> and <b>read receipts</b> via extra socket events.",
    "<b>Group chats</b> by allowing more than two participants in a Conversation.",
    "<b>Message search</b> and <b>pagination</b> for long histories.",
    "<b>Push notifications</b> for new messages when the tab is closed.",
    "<b>Delete / edit messages</b> and <b>emoji reactions</b>.",
    "Server-side filtering of online status for stronger privacy.",
    "Unit/integration tests (Jest, React Testing Library, Supertest).",
])
sp(6); hr()
p("With these foundations and ideas, ChatWave can grow from a clean one-to-one chat into a full messaging platform.")

# ============ 29. APPENDIX — COMPONENT REFERENCE ============
pb()
ch("29. Appendix — Component Reference")
p("Key responsibilities and the core logic of each component, for quick reference.")

h1("Login.jsx")
p("Signs the user in and stores them in Redux.")
code('const res = await axios.post(`${BASE_URL}/api/v1/user/login`, user, {withCredentials:true});\n'
     'dispatch(setAuthUser(res.data));\nnavigate("/");\n'
     '// on error: toast.error("Incorrect username or password")')

h1("Signup.jsx")
p("Creates an account; gender is a required single-select.")
code('if(!user.gender) return toast.error("Please select your gender");\n'
     'const res = await axios.post(`${BASE_URL}/api/v1/user/register`, user, {withCredentials:true});\n'
     'if(res.data.success){ navigate("/login"); toast.success(res.data.message); }')

h1("Sidebar.jsx")
p("Shows your profile (click to open ProfileModal), search, the user list, and logout.")
code('const res = await axios.get(`${BASE_URL}/api/v1/user/logout`);\n'
     'dispatch(setAuthUser(null)); dispatch(setMessages(null));\n'
     'dispatch(setOtherUsers(null)); dispatch(setSelectedUser(null));\n'
     'navigate("/login");')
pb()

h1("OtherUser.jsx")
p("One contact row; selecting it opens that conversation.")
code('const isOnline = isUserOnline(user, onlineUsers);   // respects status privacy\n'
     'onClick={() => dispatch(setSelectedUser(user))}')

h1("MessageContainer.jsx")
p("Right pane: header (opens the friend’s profile), messages, and the composer.")
code('const isOnline = isUserOnline(selectedUser, onlineUsers);\n'
     '{selectedUser ? (<><Header/><Messages/><SendInput/></>) : (<EmptyState/>)}\n'
     '{showProfile && <ProfileModal user={selectedUser} isOwn={false} .../>}')

h1("ProfileModal.jsx")
p("Views any user; your own profile can be edited (name, gender, photo, status).")
code('// upload photo from device -> base64\nreader.onloadend = () => setPhoto(reader.result);\n\n'
     '// save\nawait axios.post(`${BASE_URL}/api/v1/user/profile/update`,\n'
     '  { fullName, profilePhoto:photo, gender, showStatus }, {withCredentials:true});\n'
     'dispatch(setAuthUser(res.data.user));')

h1("AuthWelcome.jsx")
p("The static blue feature panel shown beside the Login/Signup forms (brand + highlights). Pure presentational component — no state or API calls.")
sp(6); hr()
p("That completes the full reference. Use the Table of Contents to jump back to any topic.")

# ============ 30. SEQUENCE DIAGRAMS ============
pb()
ch("30. Visual Sequence Diagrams")
p("Each diagram shows the exact order of steps for one operation, end to end.")

h1("Register")
flow(["Browser form", "POST /register", "bcrypt hash", "User.create", "201 success"])
h1("Login")
flow(["POST /login", "bcrypt.compare", "jwt.sign", "Set-Cookie", "setAuthUser"])
h1("Load other users")
flow(["useGetOtherUsers", "GET /user", "isAuthenticated", "User.find", "setOtherUsers"])
h1("Open a conversation")
flow(["Click user", "setSelectedUser", "useGetMessages", "GET /message/:id", "setMessages"])
h1("Send a text message")
flow(["SendInput", "POST /send/:id", "Message.create", "save Conversation", "201 + setMessages"])
h1("Send an image / file")
flow(["Pick file", "base64", "POST /send/:id", "uploadMedia", "store URL"])
h1("Receive a message in real time")
flow(["Server emit", "newMessage", "socket.on", "setMessages", "bubble appears"], color=GREEN)
h1("Presence (online users)")
flow(["Socket connect", "userSocketMap", "emit getOnlineUsers", "setOnlineUsers", "green dots"], color=GREEN)
h1("Edit profile")
flow(["Open modal", "Edit + Save", "POST /profile/update", "findByIdAndUpdate", "setAuthUser"])
h1("Logout")
flow(["Click Logout", "GET /logout", "clear cookie", "setAuthUser(null)", "go /login"])
sp(6); hr()
p("These ten flows cover every major action in ChatWave. Together with the chapters above, you now have a "
  "complete, end-to-end understanding of the project — frontend, backend, state, database, and real-time.")

# ============ BUILD ============
def footer(canvas, doc):
    canvas.saveState(); canvas.setFont(REG, 8); canvas.setFillColor(GRAY)
    canvas.drawString(2*cm, 1.1*cm, "ChatWave — Complete Documentation")
    canvas.drawRightString(A4[0]-2*cm, 1.1*cm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=1.8*cm,
                        title="ChatWave Full Documentation", author="ChatWave")
doc.build(story, onLaterPages=footer)
print("PDF created:", OUT)
