import React, { useState } from 'react'
import { BiSearchAlt2 } from "react-icons/bi";
import { FiLogOut } from "react-icons/fi";
import OtherUsers from './OtherUsers';
import ProfileModal from './ProfileModal';
import axios from "axios";
import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { setAuthUser, setOtherUsers, setSelectedUser } from '../redux/userSlice';
import { setMessages } from '../redux/messageSlice';
import { BASE_URL } from '..';
import { avatarSrc, avatarOnError } from '../utils/avatar';

const Sidebar = () => {
    const [search, setSearch] = useState("");
    const [showProfile, setShowProfile] = useState(false);
    const { otherUsers, authUser } = useSelector(store => store.user);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const logoutHandler = async () => {
        try {
            const res = await axios.get(`${BASE_URL}/api/v1/user/logout`);
            navigate("/login");
            toast.success(res.data.message);
            dispatch(setAuthUser(null));
            dispatch(setMessages(null));
            dispatch(setOtherUsers(null));
            dispatch(setSelectedUser(null));
        } catch (error) {
            console.log(error);
        }
    }
    const searchSubmitHandler = (e) => {
        e.preventDefault();
        const conversationUser = otherUsers?.find((user) => user.fullName.toLowerCase().includes(search.toLowerCase()));
        if (conversationUser) {
            dispatch(setOtherUsers([conversationUser]));
        } else {
            toast.error("User not found!");
        }
    }

    return (
        <div className='w-full md:w-2/5 md:max-w-md shrink-0 border-r border-slate-200 flex flex-col bg-white'>
            {/* Header — current user (click to view profile) */}
            <button
                onClick={() => setShowProfile(true)}
                className="flex items-center gap-3 px-4 py-4 border-b border-slate-200 hover:bg-slate-50 transition text-left">
                <div className="relative">
                    <img
                        src={avatarSrc(authUser)}
                        onError={avatarOnError(authUser)}
                        alt="me"
                        className="w-11 h-11 rounded-full object-cover bg-slate-100 border border-slate-200" />
                    <span className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-white rounded-full"></span>
                </div>
                <div className="min-w-0">
                    <p className="text-slate-900 font-semibold truncate">{authUser?.fullName || "Me"}</p>
                    <p className="text-xs text-slate-400">View profile</p>
                </div>
            </button>

            {/* Search */}
            <form onSubmit={searchSubmitHandler} className='flex items-center gap-2 px-4 py-3'>
                <div className="relative flex-1">
                    <BiSearchAlt2 className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                    <input
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className='w-full pl-9 pr-3 py-2 text-sm rounded-xl bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition'
                        type="text"
                        placeholder='Search people...'
                    />
                </div>
                <button type='submit' className='p-2.5 rounded-xl bg-blue-600 text-white hover:bg-blue-700 transition'>
                    <BiSearchAlt2 className='w-4 h-4' />
                </button>
            </form>

            {/* User list */}
            <div className="flex-1 overflow-hidden px-2">
                <OtherUsers />
            </div>

            {/* Logout */}
            <div className='p-3 border-t border-slate-200'>
                <button
                    onClick={logoutHandler}
                    className='w-full flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-semibold text-red-600 bg-red-50 hover:bg-red-100 border border-red-200 transition'>
                    <FiLogOut /> Logout
                </button>
            </div>

            {showProfile && (
                <ProfileModal user={authUser} isOwn={true} onClose={() => setShowProfile(false)} />
            )}
        </div>
    )
}

export default Sidebar
