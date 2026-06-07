import React from 'react'
import { useDispatch, useSelector } from "react-redux";
import { setSelectedUser } from '../redux/userSlice';
import { avatarSrc, avatarOnError } from '../utils/avatar';
import { isUserOnline } from '../utils/helpers';

const OtherUser = ({ user }) => {
    const dispatch = useDispatch();
    const { selectedUser, onlineUsers } = useSelector(store => store.user);
    const isOnline = isUserOnline(user, onlineUsers);
    const isSelected = selectedUser?._id === user?._id;
    const selectedUserHandler = (user) => {
        dispatch(setSelectedUser(user));
    }
    return (
        <div
            onClick={() => selectedUserHandler(user)}
            className={`flex gap-3 items-center rounded-xl px-3 py-2.5 cursor-pointer transition border ${isSelected
                ? 'bg-blue-50 border-blue-200'
                : 'hover:bg-slate-50 border-transparent'}`}>
            <div className="relative">
                <img
                    src={avatarSrc(user)}
                    onError={avatarOnError(user)}
                    alt="user-profile"
                    className="w-11 h-11 rounded-full object-cover bg-slate-100 border border-slate-200" />
                {isOnline && (
                    <span className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-white rounded-full"></span>
                )}
            </div>
            <div className='flex flex-col flex-1 min-w-0'>
                <p className="text-slate-900 font-medium truncate">{user?.fullName}</p>
                <p className={`text-xs truncate ${isOnline ? 'text-green-600' : 'text-slate-400'}`}>
                    {isOnline ? 'Active now' : 'Offline'}
                </p>
            </div>
        </div>
    )
}

export default OtherUser
