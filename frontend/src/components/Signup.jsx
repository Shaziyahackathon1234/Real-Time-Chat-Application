import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom';
import axios from "axios";
import toast from "react-hot-toast";
import { BASE_URL } from '..';
import { FiUser, FiLock, FiAtSign, FiEye, FiEyeOff, FiCheck } from "react-icons/fi";
import { HiOutlineChatBubbleLeftRight } from "react-icons/hi2";
import AuthWelcome from './AuthWelcome';

const Signup = () => {
    const [user, setUser] = useState({
        fullName: "",
        username: "",
        password: "",
        confirmPassword: "",
        gender: "",
    });
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirm, setShowConfirm] = useState(false);
    const navigate = useNavigate();

    const handleGender = (gender) => {
        setUser((prev) => ({ ...prev, gender }));
    }

    const onSubmitHandler = async (e) => {
        e.preventDefault();
        if (!user.gender) {
            toast.error("Please select your gender");
            return;
        }
        setLoading(true);
        try {
            const res = await axios.post(`${BASE_URL}/api/v1/user/register`, user, {
                headers: { 'Content-Type': 'application/json' },
                withCredentials: true
            });
            if (res.data.success) {
                navigate("/login");
                toast.success(res.data.message);
            }
        } catch (error) {
            toast.error(error?.response?.data?.message || "Signup failed");
            console.log(error);
        } finally {
            setLoading(false);
        }
        setUser({ fullName: "", username: "", password: "", confirmPassword: "", gender: "" });
    }

    const inputClass = 'w-full pl-11 pr-4 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition';
    const pwdClass = 'w-full pl-11 pr-11 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition';

    const GenderBtn = ({ value, label }) => {
        const active = user.gender === value;
        return (
            <button
                type="button"
                onClick={() => handleGender(value)}
                className={`flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-medium border transition ${active
                    ? "bg-blue-600 border-blue-600 text-white"
                    : "bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100"}`}>
                {active && <FiCheck size={15} />} {label}
            </button>
        );
    };

    return (
        <div className="h-screen w-screen flex bg-white">
            {/* Left welcome panel */}
            <AuthWelcome />

            {/* Right form */}
            <div className="w-full md:w-1/2 flex items-center justify-center p-6 sm:p-10 overflow-auto">
                <div className="w-full max-w-md py-6">
                    <div className="md:hidden flex items-center gap-2 mb-5">
                        <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center">
                            <HiOutlineChatBubbleLeftRight className="text-white text-xl" />
                        </div>
                        <span className="font-bold text-slate-900">ChatWave</span>
                    </div>

                    <h1 className='text-3xl font-bold text-slate-900'>Create account</h1>
                    <p className="text-sm text-slate-500 mt-1 mb-6">Join and start chatting in real time</p>

                    <form onSubmit={onSubmitHandler} className="space-y-4">
                        {/* Full Name */}
                        <div className="relative">
                            <FiUser className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                            <input
                                value={user.fullName}
                                onChange={(e) => setUser({ ...user, fullName: e.target.value })}
                                className={inputClass}
                                type="text"
                                placeholder='Full Name' />
                        </div>
                        {/* Username */}
                        <div className="relative">
                            <FiAtSign className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                            <input
                                value={user.username}
                                onChange={(e) => setUser({ ...user, username: e.target.value })}
                                className={inputClass}
                                type="text"
                                placeholder='Username' />
                        </div>
                        {/* Password */}
                        <div className="relative">
                            <FiLock className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                            <input
                                value={user.password}
                                onChange={(e) => setUser({ ...user, password: e.target.value })}
                                className={pwdClass}
                                type={showPassword ? "text" : "password"}
                                placeholder='Password' />
                            <button type="button" onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                                {showPassword ? <FiEye /> : <FiEyeOff />}
                            </button>
                        </div>
                        {/* Confirm Password */}
                        <div className="relative">
                            <FiLock className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                            <input
                                value={user.confirmPassword}
                                onChange={(e) => setUser({ ...user, confirmPassword: e.target.value })}
                                className={pwdClass}
                                type={showConfirm ? "text" : "password"}
                                placeholder='Confirm Password' />
                            <button type="button" onClick={() => setShowConfirm(!showConfirm)}
                                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                                {showConfirm ? <FiEye /> : <FiEyeOff />}
                            </button>
                        </div>

                        {/* Gender — single select */}
                        <div>
                            <label className="block text-xs font-medium text-slate-500 mb-1.5">Gender</label>
                            <div className='flex items-center gap-3'>
                                <GenderBtn value="male" label="Male" />
                                <GenderBtn value="female" label="Female" />
                            </div>
                        </div>

                        <button
                            type='submit'
                            disabled={loading}
                            className='w-full py-3 rounded-xl font-semibold text-white bg-blue-600 hover:bg-blue-700 active:scale-[0.99] transition disabled:opacity-60 mt-2'>
                            {loading ? "Creating account..." : "Sign up"}
                        </button>

                        <p className='text-center text-sm text-slate-500'>
                            Already have an account?{" "}
                            <Link to="/login" className="text-blue-600 font-semibold hover:underline">Login</Link>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default Signup
