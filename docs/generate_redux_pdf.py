#!/usr/bin/env python3
"""Generate a beginner-friendly Redux Flow PDF for the chat application."""
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

OUT = os.path.join(os.path.dirname(__file__), "Redux-Flow-Explained.pdf")

# Embed Arial so text always renders
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

styles = getSampleStyleSheet()
def S(name, **kw): styles.add(ParagraphStyle(name, parent=styles['Normal'], **kw))

S('CoverTitle', fontName=BOLD, fontSize=30, textColor=DARK, alignment=TA_CENTER, leading=36)
S('CoverSub', fontName=REG, fontSize=14, textColor=BLUE, alignment=TA_CENTER, leading=20)
S('CoverSmall', fontName=REG, fontSize=10, textColor=GRAY, alignment=TA_CENTER, leading=16)
S('H1', fontName=BOLD, fontSize=17, textColor=BLUE, spaceBefore=16, spaceAfter=7, leading=21)
S('H2', fontName=BOLD, fontSize=12.5, textColor=DARK, spaceBefore=9, spaceAfter=3, leading=16)
S('Body', fontName=REG, fontSize=10.5, textColor=DARK, leading=16, spaceAfter=6)
S('MyBullet', fontName=REG, fontSize=10.5, textColor=DARK, leading=15)
S('CodeBox', fontName="Courier", fontSize=9, textColor=DARK, leading=13, backColor=CODEBG,
  borderPadding=(8,8,8,8), spaceBefore=4, spaceAfter=8, leftIndent=2)
S('Cell', fontName=REG, fontSize=9.5, textColor=DARK, leading=13)
S('CellB', fontName=BOLD, fontSize=9.5, textColor=colors.white, leading=13)
S('Step', fontName=REG, fontSize=10.5, textColor=DARK, leading=15)

story = []
def h1(t): story.append(Paragraph(t, styles['H1']))
def h2(t): story.append(Paragraph(t, styles['H2']))
def p(t): story.append(Paragraph(t, styles['Body']))
def sp(h=8): story.append(Spacer(1, h))
def code(t): story.append(Paragraph(t.replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>").replace(" ","&nbsp;"), styles['CodeBox']))
def bullets(items):
    story.append(ListFlowable([ListItem(Paragraph(i, styles['MyBullet']), leftIndent=10) for i in items],
        bulletColor=BLUE, bulletFontSize=8, leftIndent=12, bulletType='bullet'))
    sp(6)
def table(data, widths):
    rows=[]
    for r,row in enumerate(data):
        rows.append([Paragraph(str(c), styles['CellB' if r==0 else 'Cell']) for c in row])
    t=Table(rows, colWidths=widths, repeatRows=1)
    ts=[('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('BACKGROUND',(0,0),(-1,0),BLUE),('BOX',(0,0),(-1,-1),0.5,BORDER),('LINEBELOW',(0,0),(-1,-1),0.5,BORDER)]
    for r in range(1,len(data)):
        if r%2==0: ts.append(('BACKGROUND',(0,r),(-1,r),LIGHT))
    t.setStyle(TableStyle(ts)); story.append(t); sp(8)
def flow(steps):
    # render an arrow flow as a single-row table
    cells=[]
    for i,s in enumerate(steps):
        cells.append(Paragraph(s, ParagraphStyle('f', parent=styles['Normal'], fontName=BOLD, fontSize=8.5,
            textColor=colors.white, alignment=TA_CENTER, leading=11)))
    t=Table([cells], colWidths=[(17.0/len(steps))*cm]*len(steps))
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BLUE),('TOPPADDING',(0,0),(-1,-1),8),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
        ('LINEAFTER',(0,0),(-2,-1),1,colors.white),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    story.append(t); sp(8)

# -------- COVER --------
sp(140)
story.append(Paragraph("Redux Flow — Explained Simply", styles['CoverTitle']))
sp(8)
story.append(Paragraph("ChatWave · Real-Time Chat Application", styles['CoverSub']))
sp(26)
story.append(Paragraph("How data moves through Redux Toolkit in your MERN chat app —<br/>store, slices, actions, dispatch, selectors, and redux-persist.", styles['CoverSmall']))
sp(36)
story.append(Paragraph("Frontend: React + Redux Toolkit + redux-persist", styles['CoverSmall']))
story.append(PageBreak())

# -------- 1. WHAT IS REDUX --------
h1("1. What is Redux? (the simple idea)")
p("Redux is a <b>central box</b> that holds data your whole app needs to share — like the logged-in user, "
  "the list of friends, the selected chat, and the messages. Instead of passing this data through many "
  "components (prop-drilling), every component reads it directly from this one box.")
p("That central box is called the <b>store</b>. The big benefit: when the data in the store changes, "
  "every component using it <b>updates automatically</b>.")
h2("The 4 words you must know")
table([
    ["Term", "Meaning (in plain English)"],
    ["Store", "The single box that holds all shared data (state)."],
    ["Slice", "A labelled section of the store + the functions that change it."],
    ["Action / Reducer", "An instruction to change the store (e.g. 'set the messages')."],
    ["dispatch", "How a component SENDS an instruction to change the store."],
], [4.2*cm, 11.3*cm])
p("And one more for reading: <b>useSelector</b> — how a component READS data from the store.")

# -------- 2. THE GOLDEN FLOW --------
h1("2. The golden flow (read this twice)")
flow(["Component", "dispatch(action)", "Reducer updates Store", "useSelector re-renders UI"])
bullets([
    "A component calls <b>dispatch(someAction(data))</b> — \"please change the store\".",
    "The matching <b>reducer</b> updates that slice of the store.",
    "Every component using <b>useSelector</b> on that data <b>re-renders</b> with the new value.",
])
p("That's the entire cycle. Everything below is just this same loop with your real data.")

# -------- 3. YOUR STORE --------
h1("3. Your store setup")
p("Your store combines <b>three slices</b> and is wrapped with <b>redux-persist</b> (explained in section 6):")
code("combineReducers({\n  user: userReducer,      // who am I, friends, selected chat, online users\n  message: messageReducer, // the messages in the open chat\n  socket: socketReducer    // the live socket connection\n})")
p("So your store looks like this in memory:")
code("store = {\n  user:    { authUser, otherUsers, selectedUser, onlineUsers },\n  message: { messages },\n  socket:  { socket }\n}")

# -------- 4. THE SLICES --------
story.append(PageBreak())
h1("4. Your three slices in detail")

h2("userSlice  →  store.user")
table([
    ["State", "What it holds", "Action to change it"],
    ["authUser", "The logged-in user (you)", "setAuthUser"],
    ["otherUsers", "List of all other users (friends)", "setOtherUsers"],
    ["selectedUser", "The friend whose chat is open", "setSelectedUser"],
    ["onlineUsers", "IDs of users currently online", "setOnlineUsers"],
], [3.6*cm, 7.4*cm, 4.5*cm])

h2("messageSlice  →  store.message")
table([
    ["State", "What it holds", "Action to change it"],
    ["messages", "All messages in the open conversation", "setMessages"],
], [3.6*cm, 7.4*cm, 4.5*cm])

h2("socketSlice  →  store.socket")
table([
    ["State", "What it holds", "Action to change it"],
    ["socket", "The live Socket.IO connection object", "setSocket"],
], [3.6*cm, 7.4*cm, 4.5*cm])

# -------- 5. REAL EXAMPLES --------
h1("5. Real examples from YOUR app")

h2("A) Logging in")
p("When login succeeds, the component saves you into the store:")
code('dispatch(setAuthUser(res.data));  // store.user.authUser = you')
p("Now the whole app knows who you are — the sidebar shows your name, and HomePage stops redirecting to /login.")

h2("B) Opening a chat")
p("Clicking a friend in the sidebar:")
code('dispatch(setSelectedUser(user));  // store.user.selectedUser = that friend')
p("<b>MessageContainer</b> reads selectedUser with useSelector, so it instantly switches to that conversation.")

h2("C) Sending a message")
code('dispatch(setMessages([...messages, newMessage]));')
p("The new message is added to store.message.messages, and the chat re-renders to show it.")

h2("D) Real-time incoming messages (Socket.IO)")
p("Your <b>socket</b> lives in the store. When the server pushes a 'newMessage', the hook adds it:")
code('socket.on("newMessage", (m) => dispatch(setMessages([...messages, m])));')

h2("E) Who is online")
p("The socket emits 'getOnlineUsers'; you store the list so green dots appear:")
code('dispatch(setOnlineUsers(onlineUsers));  // store.user.onlineUsers')

# -------- 6. REDUX PERSIST --------
story.append(PageBreak())
h1("6. redux-persist — staying logged in on refresh")
p("Normally, the Redux store is wiped when you refresh the page. <b>redux-persist</b> automatically saves your "
  "store into the browser's <b>localStorage</b> and reloads it on startup — so you stay logged in and your "
  "selected chat is remembered.")
bullets([
    "<b>persistReducer</b> wraps your reducers and saves state to storage under the key 'root'.",
    "<b>persistStore</b> + <b>PersistGate</b> (in index.js) restore the saved state before the app renders.",
    "The <b>socket</b> is excluded from saving (it's a live connection, not data) via ignoredPaths.",
])
p("This is why, even after pressing refresh, you don't get logged out.")

# -------- 7. END TO END --------
h1("7. End-to-end: from login to chatting")
flow(["Login", "setAuthUser", "Load friends", "Pick a friend", "Send / receive"])
steps = [
    "<b>1.</b> You log in → <b>dispatch(setAuthUser)</b> → store knows you.",
    "<b>2.</b> The useGetOtherUsers hook fetches friends → <b>dispatch(setOtherUsers)</b> → sidebar fills up.",
    "<b>3.</b> Socket connects → <b>dispatch(setSocket)</b> and online list → <b>dispatch(setOnlineUsers)</b>.",
    "<b>4.</b> You click a friend → <b>dispatch(setSelectedUser)</b> → chat opens.",
    "<b>5.</b> useGetMessages fetches history → <b>dispatch(setMessages)</b> → bubbles appear.",
    "<b>6.</b> You type & send → <b>dispatch(setMessages)</b>; friend's message arrives via socket → <b>dispatch(setMessages)</b>.",
    "<b>7.</b> redux-persist quietly saves everything so a refresh keeps you in.",
]
story.append(ListFlowable([ListItem(Paragraph(s, styles['Step']), leftIndent=10) for s in steps],
    bulletColor=BLUE, bulletFontSize=1, leftIndent=6, bulletType='bullet'))
sp(10)
story.append(HRFlowable(width="100%", thickness=1, color=BORDER)); sp(8)
p("<b>Remember the one loop:</b> a component <b>dispatches</b> an action → the <b>reducer</b> updates the "
  "<b>store</b> → components reading that data with <b>useSelector</b> re-render. Everything in this app is "
  "just that loop, repeated.")

# -------- BUILD --------
def footer(canvas, doc):
    canvas.saveState(); canvas.setFont(REG, 8); canvas.setFillColor(GRAY)
    canvas.drawString(2*cm, 1.2*cm, "ChatWave — Redux Flow Explained")
    canvas.drawRightString(A4[0]-2*cm, 1.2*cm, f"Page {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm,
                        title="Redux Flow Explained", author="ChatWave")
doc.build(story, onLaterPages=footer)
print("PDF created:", OUT)
