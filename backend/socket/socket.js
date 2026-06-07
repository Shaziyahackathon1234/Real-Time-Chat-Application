import {Server} from "socket.io";
import http from "http";
import express from "express";

const app = express();

const server = http.createServer(app);
const normalize = (u) => (u || "").replace(/\/+$/, "");
const staticAllowed = ['http://localhost:3000', normalize(process.env.CLIENT_URL)].filter(Boolean);
const isAllowedOrigin = (origin) => {
    if (!origin) return true;
    const o = normalize(origin);
    if (staticAllowed.includes(o)) return true;
    if (o.endsWith('.vercel.app')) return true;
    return false;
};
const io = new Server(server, {
    cors:{
        origin: (origin, callback) => callback(null, isAllowedOrigin(origin)),
        methods:['GET', 'POST'],
        credentials: true,
    },
});

export const getReceiverSocketId = (receiverId) => {
    return userSocketMap[receiverId];
}

const userSocketMap = {}; // {userId->socketId}


io.on('connection', (socket)=>{
    const userId = socket.handshake.query.userId
    if(userId !== undefined){
        userSocketMap[userId] = socket.id;
    } 

    io.emit('getOnlineUsers',Object.keys(userSocketMap));

    socket.on('disconnect', ()=>{
        delete userSocketMap[userId];
        io.emit('getOnlineUsers',Object.keys(userSocketMap));
    })

})

export {app, io, server};

