import React, { useState, useRef } from 'react'
import { IoSend } from "react-icons/io5";
import { FiPaperclip, FiX, FiFile } from "react-icons/fi";
import axios from "axios";
import toast from "react-hot-toast";
import { useDispatch, useSelector } from "react-redux";
import { setMessages } from '../redux/messageSlice';
import { BASE_URL } from '..';

const SendInput = () => {
    const [message, setMessage] = useState("");
    const [media, setMedia] = useState("");      // base64 data URI
    const [fileName, setFileName] = useState(""); // name (for non-image files)
    const [sending, setSending] = useState(false);
    const fileRef = useRef();
    const dispatch = useDispatch();
    const { selectedUser } = useSelector(store => store.user);
    const { messages } = useSelector(store => store.message);

    const isImage = media.startsWith("data:image");

    const handleFile = (e) => {
        const file = e.target.files?.[0];
        if (!file) return;
        if (file.size > 4 * 1024 * 1024) {
            toast.error("Please choose a file under 4MB");
            return;
        }
        const reader = new FileReader();
        reader.onloadend = () => {
            setMedia(reader.result);
            setFileName(file.name);
        };
        reader.readAsDataURL(file);
    };

    const clearMedia = () => {
        setMedia(""); setFileName("");
        if (fileRef.current) fileRef.current.value = "";
    };

    const onSubmitHandler = async (e) => {
        e.preventDefault();
        if (!message.trim() && !media) return;
        setSending(true);
        try {
            const res = await axios.post(`${BASE_URL}/api/v1/message/send/${selectedUser?._id}`,
                { message, media, fileName },
                { headers: { 'Content-Type': 'application/json' }, withCredentials: true });
            dispatch(setMessages([...(messages || []), res?.data?.newMessage]));
            setMessage(""); clearMedia();
        } catch (error) {
            toast.error(error?.response?.data?.message || "Failed to send");
            console.log(error);
        } finally {
            setSending(false);
        }
    }

    return (
        <form onSubmit={onSubmitHandler} className='px-4 py-4 border-t border-slate-200 bg-white'>
            {/* Attachment preview */}
            {media && (
                <div className="mb-3 flex items-center gap-3">
                    {isImage ? (
                        <img src={media} alt="preview" className="w-16 h-16 rounded-lg object-cover border border-slate-200" />
                    ) : (
                        <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-slate-100 text-slate-700 text-sm">
                            <FiFile /> <span className="max-w-[160px] truncate">{fileName}</span>
                        </div>
                    )}
                    <button type="button" onClick={clearMedia}
                        className="w-7 h-7 flex items-center justify-center rounded-full bg-slate-200 text-slate-600 hover:bg-slate-300">
                        <FiX size={14} />
                    </button>
                </div>
            )}

            <div className='w-full flex items-center gap-2'>
                {/* Attach button */}
                <button type="button" onClick={() => fileRef.current?.click()}
                    className="w-11 h-11 shrink-0 flex items-center justify-center rounded-xl bg-slate-100 text-slate-600 hover:bg-slate-200 transition"
                    title="Attach image or file">
                    <FiPaperclip size={18} />
                </button>
                <input ref={fileRef} type="file" accept="image/*,.pdf,.doc,.docx,.txt,.zip" className="hidden" onChange={handleFile} />

                <input
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    type="text"
                    placeholder='Type a message...'
                    className='flex-1 text-sm rounded-xl px-4 py-3 bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition'
                />
                <button type="submit" disabled={sending}
                    className='w-12 h-12 shrink-0 flex items-center justify-center rounded-xl bg-blue-600 text-white hover:bg-blue-700 active:scale-95 transition disabled:opacity-60'>
                    <IoSend className="text-lg" />
                </button>
            </div>
        </form>
    )
}

export default SendInput
