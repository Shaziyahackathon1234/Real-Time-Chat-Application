import React, { useState } from 'react'
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import toast from "react-hot-toast";
import { setAuthUser } from '../redux/userSlice';
import { BASE_URL } from '..';
import { avatarSrc, avatarOnError } from '../utils/avatar';
import { formatJoined, isUserOnline } from '../utils/helpers';
import { FiX, FiEdit2, FiCamera, FiAtSign, FiUser, FiCalendar, FiEye } from "react-icons/fi";

const ProfileModal = ({ user, isOwn, onClose, startEditing = false }) => {
    const dispatch = useDispatch();
    const { onlineUsers } = useSelector(store => store.user);
    // Own profile: show real connection. Others: respect their privacy setting.
    const isOnline = isOwn ? onlineUsers?.includes(user?._id) : isUserOnline(user, onlineUsers);

    const [editing, setEditing] = useState(startEditing && isOwn);
    const [fullName, setFullName] = useState(user?.fullName || "");
    const [photo, setPhoto] = useState(user?.profilePhoto || "");
    const [gender, setGender] = useState(user?.gender || "");
    const [showStatus, setShowStatus] = useState(user?.showStatus !== false);
    const [saving, setSaving] = useState(false);

    const handleFile = (e) => {
        const file = e.target.files?.[0];
        if (!file) return;
        if (file.size > 3 * 1024 * 1024) {
            toast.error("Please choose an image under 3MB");
            return;
        }
        const reader = new FileReader();
        reader.onloadend = () => setPhoto(reader.result); // base64 data URL
        reader.readAsDataURL(file);
    };

    const handleSave = async () => {
        if (!fullName.trim()) {
            toast.error("Name cannot be empty");
            return;
        }
        setSaving(true);
        try {
            const res = await axios.post(`${BASE_URL}/api/v1/user/profile/update`,
                { fullName, profilePhoto: photo, gender, showStatus },
                { headers: { 'Content-Type': 'application/json' }, withCredentials: true }
            );
            dispatch(setAuthUser(res.data.user));
            toast.success("Profile updated");
            setEditing(false);
        } catch (error) {
            toast.error(error?.response?.data?.message || "Update failed");
        } finally {
            setSaving(false);
        }
    };

    const cancelEdit = () => {
        setEditing(false);
        setFullName(user?.fullName || "");
        setPhoto(user?.profilePhoto || "");
        setGender(user?.gender || "");
        setShowStatus(user?.showStatus !== false);
    };

    const Toggle = ({ on, onClick }) => (
        <button type="button" onClick={onClick}
            className={`w-11 h-6 rounded-full transition relative ${on ? 'bg-blue-600' : 'bg-slate-300'}`}>
            <span className={`absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition ${on ? 'left-[22px]' : 'left-0.5'}`}></span>
        </button>
    );

    const GenderBtn = ({ value, label }) => (
        <button type="button" onClick={() => setGender(value)}
            className={`flex-1 py-2 rounded-lg text-sm font-medium border transition ${gender === value
                ? "bg-blue-600 border-blue-600 text-white"
                : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"}`}>
            {label}
        </button>
    );

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4" onClick={onClose}>
            <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl overflow-hidden max-h-[92vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
                {/* Header banner */}
                <div className="relative h-28 bg-gradient-to-br from-blue-600 to-blue-800">
                    <p className="absolute top-4 left-5 text-white font-semibold text-sm">
                        {isOwn ? (editing ? "Edit Profile" : "My Profile") : "Profile"}
                    </p>
                    <button onClick={onClose} className="absolute top-3 right-3 text-white/80 hover:text-white">
                        <FiX size={20} />
                    </button>
                </div>

                {/* Avatar */}
                <div className="flex flex-col items-center -mt-12 px-6 pb-6">
                    <div className="relative">
                        <img
                            src={editing ? avatarSrc({ ...user, profilePhoto: photo }) : avatarSrc(user)}
                            onError={avatarOnError(user)}
                            alt="profile"
                            className="w-24 h-24 rounded-full object-cover border-4 border-white bg-slate-100 shadow" />
                        {isOnline && (
                            <span className="absolute bottom-1 right-1 w-4 h-4 bg-green-500 border-2 border-white rounded-full"></span>
                        )}
                        {isOwn && editing && (
                            <label className="absolute bottom-0 right-0 w-8 h-8 flex items-center justify-center bg-blue-600 text-white rounded-full cursor-pointer hover:bg-blue-700 border-2 border-white">
                                <FiCamera size={14} />
                                <input type="file" accept="image/*" className="hidden" onChange={handleFile} />
                            </label>
                        )}
                    </div>

                    {isOwn && editing ? (
                        /* ---------- EDIT MODE ---------- */
                        <div className="w-full mt-4 space-y-4">
                            <div>
                                <label className="block text-xs font-medium text-slate-500 mb-1">Full Name</label>
                                <input
                                    value={fullName}
                                    onChange={(e) => setFullName(e.target.value)}
                                    className="w-full px-3 py-2 rounded-lg bg-slate-50 border border-slate-200 text-slate-900 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
                                    placeholder="Your name" />
                            </div>

                            <div>
                                <label className="block text-xs font-medium text-slate-500 mb-1">Gender</label>
                                <div className="flex gap-2">
                                    <GenderBtn value="male" label="Male" />
                                    <GenderBtn value="female" label="Female" />
                                </div>
                            </div>

                            {/* Status privacy toggle */}
                            <div className="flex items-center justify-between px-3 py-2.5 rounded-lg bg-slate-50">
                                <div className="flex items-center gap-2">
                                    <FiEye className="text-slate-400" />
                                    <div>
                                        <p className="text-sm text-slate-800 font-medium">Show online status</p>
                                        <p className="text-[11px] text-slate-400">{showStatus ? "Friends can see when you're online" : "Hidden — no one can see your status"}</p>
                                    </div>
                                </div>
                                <Toggle on={showStatus} onClick={() => setShowStatus(!showStatus)} />
                            </div>

                            <p className="text-xs text-slate-400 text-center">Tap the camera icon to change your photo</p>
                            <div className="flex gap-2">
                                <button onClick={cancelEdit}
                                    className="flex-1 py-2 rounded-lg text-sm font-medium text-slate-600 bg-slate-100 hover:bg-slate-200">
                                    Cancel
                                </button>
                                <button onClick={handleSave} disabled={saving}
                                    className="flex-1 py-2 rounded-lg text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-60">
                                    {saving ? "Saving..." : "Save"}
                                </button>
                            </div>
                        </div>
                    ) : (
                        /* ---------- VIEW MODE ---------- */
                        <>
                            <h2 className="mt-3 text-xl font-bold text-slate-900">{user?.fullName}</h2>
                            <span className={`text-xs mt-0.5 ${isOnline ? 'text-green-600' : 'text-slate-400'}`}>
                                {isOnline ? '● Online' : '● Offline'}
                                {isOwn && user?.showStatus === false && <span className="text-slate-400"> (hidden from others)</span>}
                            </span>

                            <div className="w-full mt-5 space-y-2.5">
                                <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-slate-50">
                                    <FiAtSign className="text-slate-400" />
                                    <div>
                                        <p className="text-[11px] text-slate-400">Username</p>
                                        <p className="text-sm text-slate-800 font-medium">{user?.username}</p>
                                    </div>
                                </div>
                                {user?.gender && (
                                    <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-slate-50">
                                        <FiUser className="text-slate-400" />
                                        <div>
                                            <p className="text-[11px] text-slate-400">Gender</p>
                                            <p className="text-sm text-slate-800 font-medium capitalize">{user?.gender}</p>
                                        </div>
                                    </div>
                                )}
                                {user?.createdAt && (
                                    <div className="flex items-center gap-3 px-3 py-2.5 rounded-lg bg-slate-50">
                                        <FiCalendar className="text-slate-400" />
                                        <div>
                                            <p className="text-[11px] text-slate-400">Joined</p>
                                            <p className="text-sm text-slate-800 font-medium">{formatJoined(user?.createdAt)}</p>
                                        </div>
                                    </div>
                                )}
                            </div>

                            {isOwn && (
                                <button onClick={() => setEditing(true)}
                                    className="w-full mt-5 flex items-center justify-center gap-2 py-2.5 rounded-lg text-sm font-semibold text-white bg-blue-600 hover:bg-blue-700">
                                    <FiEdit2 size={15} /> Edit Profile
                                </button>
                            )}
                        </>
                    )}
                </div>
            </div>
        </div>
    )
}

export default ProfileModal
