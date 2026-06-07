import React, { useState } from 'react'
import SendInput from './SendInput'
import Messages from './Messages';
import ProfileModal from './ProfileModal';
import { useSelector } from "react-redux";
import { HiOutlineChatBubbleLeftRight } from "react-icons/hi2";
import { FiInfo } from "react-icons/fi";
import { avatarSrc, avatarOnError } from '../utils/avatar';
import { isUserOnline } from '../utils/helpers';

const MessageContainer = () => {
    const { selectedUser, authUser, onlineUsers } = useSelector(store => store.user);
    const isOnline = isUserOnline(selectedUser, onlineUsers);
    const [showProfile, setShowProfile] = useState(false);

    return (
        <div className="flex-1 flex flex-col min-w-0 bg-slate-50">
            {selectedUser !== null ? (
                <>
                    {/* Chat header — click to view friend's profile */}
                    <div className='flex gap-3 items-center px-5 py-3.5 border-b border-slate-200 bg-white'>
                        <button onClick={() => setShowProfile(true)} className="relative">
                            <img
                                src={avatarSrc(selectedUser)}
                                onError={avatarOnError(selectedUser)}
                                alt="user-profile"
                                className="w-10 h-10 rounded-full object-cover bg-slate-100 border border-slate-200" />
                            {isOnline && (
                                <span className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-green-500 border-2 border-white rounded-full"></span>
                            )}
                        </button>
                        <button onClick={() => setShowProfile(true)} className='flex flex-col text-left'>
                            <p className="text-slate-900 font-semibold leading-tight">{selectedUser?.fullName}</p>
                            <span className={`text-xs ${isOnline ? 'text-green-600' : 'text-slate-400'}`}>
                                {isOnline ? 'Online' : 'Offline'}
                            </span>
                        </button>
                        <button
                            onClick={() => setShowProfile(true)}
                            className="ml-auto p-2 rounded-full text-slate-500 hover:bg-slate-100 transition"
                            title="View profile">
                            <FiInfo size={18} />
                        </button>
                    </div>

                    <Messages />
                    <SendInput />

                    {showProfile && (
                        <ProfileModal user={selectedUser} isOwn={false} onClose={() => setShowProfile(false)} />
                    )}
                </>
            ) : (
                <div className='flex-1 flex flex-col justify-center items-center text-center px-6'>
                    <div className="w-20 h-20 rounded-3xl bg-white border border-slate-200 shadow-sm flex items-center justify-center mb-5">
                        <HiOutlineChatBubbleLeftRight className="text-4xl text-slate-700" />
                    </div>
                    <h1 className='text-2xl text-slate-900 font-bold'>Hi, {authUser?.fullName} 👋</h1>
                    <p className='text-slate-500 mt-2'>Select a chat to start a conversation</p>
                </div>
            )}
        </div>
    )
}

export default MessageContainer
