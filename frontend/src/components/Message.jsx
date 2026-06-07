import React, { useEffect, useRef } from 'react'
import { useSelector } from "react-redux";
import { avatarSrc, avatarOnError } from '../utils/avatar';
import { FiDownload, FiFile } from "react-icons/fi";

const Message = ({ message }) => {
    const scroll = useRef();
    const { authUser, selectedUser } = useSelector(store => store.user);
    const isMe = message?.senderId === authUser?._id;
    const sender = isMe ? authUser : selectedUser;

    useEffect(() => {
        scroll.current?.scrollIntoView({ behavior: "smooth" });
    }, [message]);

    const hasImage = !!message?.image;
    const hasFile = !!message?.fileUrl;
    const hasText = !!message?.message;

    return (
        <div ref={scroll} className={`flex items-end gap-2 animate-pop ${isMe ? 'flex-row-reverse' : 'flex-row'}`}>
            <img
                alt="avatar"
                src={avatarSrc(sender)}
                onError={avatarOnError(sender)}
                className="w-8 h-8 rounded-full object-cover bg-slate-100 border border-slate-200 shrink-0" />

            <div className={`max-w-[70%] flex flex-col gap-1 ${isMe ? 'items-end' : 'items-start'}`}>
                {/* Image attachment */}
                {hasImage && (
                    <a href={message.image} target="_blank" rel="noreferrer">
                        <img src={message.image} alt="sent"
                            className="max-w-[240px] max-h-[260px] rounded-2xl border border-slate-200 object-cover" />
                    </a>
                )}

                {/* File attachment */}
                {hasFile && (
                    <a href={message.fileUrl} target="_blank" rel="noreferrer" download={message.fileName}
                        className={`flex items-center gap-2 px-3 py-2 rounded-xl border text-sm ${isMe
                            ? 'bg-blue-600 text-white border-blue-600'
                            : 'bg-white text-slate-800 border-slate-200'}`}>
                        <FiFile />
                        <span className="max-w-[160px] truncate">{message.fileName || "file"}</span>
                        <FiDownload className="opacity-80" />
                    </a>
                )}

                {/* Text */}
                {hasText && (
                    <div className={`px-4 py-2.5 text-sm leading-relaxed shadow-sm break-words ${isMe
                        ? 'bg-blue-600 text-white rounded-2xl rounded-br-md'
                        : 'bg-white text-slate-800 border border-slate-200 rounded-2xl rounded-bl-md'}`}>
                        {message.message}
                    </div>
                )}
            </div>
        </div>
    )
}

export default Message
