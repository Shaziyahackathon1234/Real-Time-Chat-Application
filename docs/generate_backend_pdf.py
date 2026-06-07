#!/usr/bin/env python3
"""Generate a beginner-friendly Backend Flow PDF for the chat application."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
    HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = os.path.join(os.path.dirname(__file__), "Backend-Flow-Explained.pdf")

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

S('CoverTitle', fontName=BOLD, fontSize=30, textColor=DARK, alignment=TA_CENTER, leading=36)
S('CoverSub', fontName=REG, fontSize=14, textColor=BLUE, alignment=TA_CENTER, leading=20)
S('CoverSmall', fontName=REG, fontSize=10, textColor=GRAY, alignment=TA_CENTER, leading=16)
S('BH1', fontName=BOLD, fontSize=17, textColor=BLUE, spaceBefore=16, spaceAfter=7, leading=21)
S('BH2', fontName=BOLD, fontSize=12.5, textColor=DARK, spaceBefore=9, spaceAfter=3, leading=16)
S('BBody', fontName=REG, fontSize=10.5, textColor=DARK, leading=16, spaceAfter=6)
S('BBullet', fontName=REG, fontSize=10.5, textColor=DARK, leading=15)
S('BCode', fontName="Courier", fontSize=8.7, textColor=DARK, leading=12.5, backColor=CODEBG,
  borderPadding=(8,8,8,8), spaceBefore=4, spaceAfter=8)
S('BCell', fontName=REG, fontSize=9, textColor=DARK, leading=12)
S('BCellB', fontName=BOLD, fontSize=9, textColor=colors.white, leading=12)
S('BStep', fontName=REG, fontSize=10.5, textColor=DARK, leading=15)

story = []
def h1(t): story.append(Paragraph(t, styles['BH1']))
def h2(t): story.append(Paragraph(t, styles['BH2']))
def p(t): story.append(Paragraph(t, styles['BBody']))
def sp(h=8): story.append(Spacer(1, h))
def code(t): story.append(Paragraph(t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>").replace(" ","&nbsp;"), styles['BCode']))
def bullets(items):
    story.append(ListFlowable([ListItem(Paragraph(i, styles['BBullet']), leftIndent=10) for i in items],
        bulletColor=BLUE, bulletFontSize=8, leftIndent=12, bulletType='bullet'))
    sp(6)
def table(data, widths):
    rows=[[Paragraph(str(c), styles['BCellB' if r==0 else 'BCell']) for c in row] for r,row in enumerate(data)]
    t=Table(rows, colWidths=widths, repeatRows=1)
    ts=[('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('BACKGROUND',(0,0),(-1,0),BLUE),('BOX',(0,0),(-1,-1),0.5,BORDER),('LINEBELOW',(0,0),(-1,-1),0.5,BORDER)]
    for r in range(1,len(data)):
        if r%2==0: ts.append(('BACKGROUND',(0,r),(-1,r),LIGHT))
    t.setStyle(TableStyle(ts)); story.append(t); sp(8)
def flow(steps, color=BLUE):
    cells=[Paragraph(s, ParagraphStyle('f', parent=styles['Normal'], fontName=BOLD, fontSize=8,
            textColor=colors.white, alignment=TA_CENTER, leading=10)) for s in steps]
    t=Table([cells], colWidths=[(17.0/len(steps))*cm]*len(steps))
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),color),('TOPPADDING',(0,0),(-1,-1),8),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),
        ('LINEAFTER',(0,0),(-2,-1),1,colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(t); sp(8)

# -------- COVER --------
sp(140)
story.append(Paragraph("Backend Flow — Explained Simply", styles['CoverTitle']))
sp(8)
story.append(Paragraph("ChatWave · Real-Time Chat Application", styles['CoverSub']))
sp(26)
story.append(Paragraph("How a request travels through your server —<br/>Express routes → middleware → controllers → Mongoose models → MongoDB,<br/>plus real-time messaging with Socket.IO.", styles['CoverSmall']))
sp(36)
story.append(Paragraph("Backend: Node.js + Express + MongoDB (Mongoose) + JWT + Socket.IO", styles['CoverSmall']))
story.append(PageBreak())

# 1. BIG PICTURE
h1("1. The big picture")
p("Your backend is an <b>Express</b> server that listens for requests from the React app, talks to a "
  "<b>MongoDB</b> database through <b>Mongoose</b>, and pushes live messages using <b>Socket.IO</b>.")
p("Every normal request follows this path:")
flow(["Client", "Middleware", "Route", "Controller", "Model", "MongoDB"])
p("And the response travels back the same way as JSON. For live chat, the server also opens a "
  "<b>websocket</b> connection (Socket.IO) that stays open to push new messages instantly.")

h2("The folders (layers)")
table([
    ["Folder / File", "Responsibility"],
    ["index.js", "Starts the server, sets middleware, mounts routes"],
    ["routes/", "Maps a URL + method to a controller function"],
    ["middleware/", "Runs before controllers (e.g. auth check)"],
    ["controllers/", "The actual logic for each request"],
    ["models/", "Mongoose schemas — the shape of your data"],
    ["config/", "Database connection"],
    ["socket/", "Socket.IO real-time setup"],
], [4.6*cm, 10.9*cm])

# 2. REQUEST LIFECYCLE
h1("2. A request's journey (step by step)")
steps = [
    "<b>1. Request arrives</b> — the React app calls e.g. POST /api/v1/message/send/:id (with the auth cookie).",
    "<b>2. Global middleware</b> runs: CORS (allow the frontend), express.json() (parse the body), cookieParser() (read cookies).",
    "<b>3. Router</b> matches the URL to a controller — here, messageRoute sends it to sendMessage.",
    "<b>4. Auth middleware</b> (isAuthenticated) reads the JWT cookie, verifies it, and sets req.id = your userId.",
    "<b>5. Controller</b> runs the logic (create the message, save the conversation).",
    "<b>6. Model (Mongoose)</b> reads/writes the data in MongoDB.",
    "<b>7. Response</b> — the controller sends JSON back; Socket.IO may also push a live event.",
]
story.append(ListFlowable([ListItem(Paragraph(s, styles['BStep']), leftIndent=10) for s in steps],
    bulletColor=BLUE, bulletFontSize=1, leftIndent=6, bulletType='bullet'))
sp(8)

# 3. AUTH
story.append(PageBreak())
h1("3. Authentication flow (JWT + cookies)")
h2("Register  →  POST /api/v1/user/register")
bullets([
    "Validates fields and that password == confirmPassword.",
    "Hashes the password with <b>bcrypt</b> (never stored in plain text).",
    "Creates the user with a generated avatar; returns success.",
])
h2("Login  →  POST /api/v1/user/login")
bullets([
    "Finds the user, compares the password with <b>bcrypt.compare</b>.",
    "On success, signs a <b>JWT</b> token and stores it in an <b>httpOnly cookie</b>.",
    "Returns your profile (id, name, username, photo, gender, status, joined).",
])
code('jwt.sign({userId}, SECRET, {expiresIn:"1d"})\n   .cookie("token", token, {httpOnly:true, sameSite:"strict"})')
h2("Protect routes  →  isAuthenticated middleware")
p("For any protected route, this middleware reads the cookie, verifies the token, and attaches your id:")
code('const token = req.cookies.token;\nconst decode = jwt.verify(token, SECRET);\nreq.id = decode.userId;  // now controllers know who you are\nnext();')
h2("Logout  →  GET /api/v1/user/logout")
p("Clears the cookie by setting it empty with maxAge 0.")

# 4. API TABLE
h1("4. All API endpoints")
table([
    ["#", "Method", "Endpoint", "Auth", "Controller"],
    ["1", "POST", "/api/v1/user/register", "No", "register"],
    ["2", "POST", "/api/v1/user/login", "No", "login"],
    ["3", "GET", "/api/v1/user/logout", "No", "logout"],
    ["4", "POST", "/api/v1/user/profile/update", "Yes", "updateProfile"],
    ["5", "GET", "/api/v1/user/", "Yes", "getOtherUsers"],
    ["6", "POST", "/api/v1/message/send/:id", "Yes", "sendMessage"],
    ["7", "GET", "/api/v1/message/:id", "Yes", "getMessage"],
], [0.9*cm, 1.9*cm, 6.6*cm, 1.4*cm, 4.7*cm])

# 5. DATA MODELS
story.append(PageBreak())
h1("5. Data models & how they relate")
h2("User")
p("<font face='Courier'>fullName, username (unique), password (hashed), profilePhoto, gender, showStatus, timestamps</font>")
h2("Message")
p("<font face='Courier'>senderId → User, receiverId → User, message, timestamps</font>")
h2("Conversation")
p("<font face='Courier'>participants: [User, User], messages: [Message], timestamps</font>")
p("<b>Relationship:</b> A <b>Conversation</b> links two users and holds a list of <b>Message</b> IDs. "
  "Each Message stores who sent it and to whom. This lets the app load a whole chat by its conversation.")
flow(["User A", "Conversation (A + B)", "Message list", "User B"])

# 6. SEND/GET MESSAGE
h1("6. Sending & loading messages")
h2("Send  →  sendMessage")
steps2 = [
    "<b>1.</b> Find the Conversation between sender & receiver; if none exists, <b>create</b> it.",
    "<b>2.</b> <b>Create</b> the Message document (senderId, receiverId, text).",
    "<b>3.</b> Push the message's id into the conversation, then <b>save</b> both.",
    "<b>4.</b> If the receiver is online, <b>Socket.IO</b> pushes 'newMessage' to them instantly.",
    "<b>5.</b> Respond to the sender with the new message.",
]
story.append(ListFlowable([ListItem(Paragraph(s, styles['BStep']), leftIndent=10) for s in steps2],
    bulletColor=BLUE, bulletFontSize=1, leftIndent=6, bulletType='bullet'))
sp(6)
h2("Load  →  getMessage")
p("Finds the conversation between the two users and <b>.populate('messages')</b> to return the full "
  "message objects (not just their ids).")

# 7. SOCKET
story.append(PageBreak())
h1("7. Real-time with Socket.IO")
p("Socket.IO keeps a live connection open so messages and presence update without refreshing.")
bullets([
    "When a user connects, the server saves <b>userId → socketId</b> in a map (userSocketMap).",
    "It broadcasts <b>getOnlineUsers</b> (the list of online user ids) to everyone.",
    "To deliver a message, <b>getReceiverSocketId(receiverId)</b> finds that user's socket, and the server emits <b>newMessage</b> only to them.",
    "On disconnect, the user is removed from the map and the online list is broadcast again.",
])
code('io.on("connection", (socket) => {\n  const userId = socket.handshake.query.userId;\n  userSocketMap[userId] = socket.id;\n  io.emit("getOnlineUsers", Object.keys(userSocketMap));\n});')

# 8. END TO END
h1("8. End-to-end: one message, start to finish")
flow(["Login (cookie)", "GET users", "GET messages", "POST send", "socket newMessage"])
steps3 = [
    "<b>1.</b> You log in → server sets the JWT cookie.",
    "<b>2.</b> App calls GET /user → getOtherUsers returns your friends.",
    "<b>3.</b> You open a chat → GET /message/:id → getMessage returns the history.",
    "<b>4.</b> You send → POST /message/send/:id → sendMessage saves it to MongoDB.",
    "<b>5.</b> The server emits 'newMessage' over Socket.IO → your friend sees it live.",
]
story.append(ListFlowable([ListItem(Paragraph(s, styles['BStep']), leftIndent=10) for s in steps3],
    bulletColor=GREEN, bulletFontSize=1, leftIndent=6, bulletType='bullet'))
sp(10)
story.append(HRFlowable(width="100%", thickness=1, color=BORDER)); sp(8)
p("<b>In one line:</b> a request passes through middleware, hits a route, runs a controller, which uses a "
  "Mongoose model to read/write MongoDB and returns JSON — while Socket.IO pushes live updates on the side.")

def footer(canvas, doc):
    canvas.saveState(); canvas.setFont(REG, 8); canvas.setFillColor(GRAY)
    canvas.drawString(2*cm, 1.2*cm, "ChatWave — Backend Flow Explained")
    canvas.drawRightString(A4[0]-2*cm, 1.2*cm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm,
                        title="Backend Flow Explained", author="ChatWave")
doc.build(story, onLaterPages=footer)
print("PDF created:", OUT)
