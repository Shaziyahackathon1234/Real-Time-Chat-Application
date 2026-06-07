import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import toast from "react-hot-toast"
import axios from "axios";
import { useDispatch } from "react-redux";
import { setAuthUser } from '../redux/userSlice';
import { BASE_URL } from '..';
import { FiUser, FiLock, FiEye, FiEyeOff } from "react-icons/fi";
import { HiOutlineChatBubbleLeftRight } from "react-icons/hi2";
import AuthWelcome from './AuthWelcome';

const Login = () => {
    const [user, setUser] = useState({
        username: "",
        password: "",
    });
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const onSubmitHandler = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await axios.post(`${BASE_URL}/api/v1/user/login`, user, {
                headers: { 'Content-Type': 'application/json' },
                withCredentials: true
            });
            navigate("/");
            dispatch(setAuthUser(res.data));
        } catch (error) {
            toast.error(error?.response?.data?.message || "Incorrect username or password");
            console.log(error);
        } finally {
            setLoading(false);
        }
        setUser({ username: "", password: "" });
    }

    return (
        <div className="h-screen w-screen flex bg-white">
            {/* Left welcome panel */}
            <AuthWelcome />

            {/* Right form */}
            <div className="w-full md:w-1/2 flex items-center justify-center p-6 sm:p-10">
                <div className="w-full max-w-md">
                    <div className="md:hidden flex items-center gap-2 mb-6">
                        <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center">
                            <HiOutlineChatBubbleLeftRight className="text-white text-xl" />
                        </div>
                        <span className="font-bold text-slate-900">ChatWave</span>
                    </div>

                    <h1 className='text-3xl font-bold text-slate-900'>Welcome back</h1>
                    <p className="text-sm text-slate-500 mt-1 mb-8">Sign in to continue chatting</p>

                    <form onSubmit={onSubmitHandler} className="space-y-5">
                        {/* Username */}
                        <div>
                            <label className='block text-sm font-medium text-slate-700 mb-1.5'>Username</label>
                            <div className="relative">
                                <FiUser className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                                <input
                                    value={user.username}
                                    onChange={(e) => setUser({ ...user, username: e.target.value })}
                                    className='w-full pl-11 pr-4 py-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition'
                                    type="text"
                                    placeholder='Enter your username' />
                            </div>
                        </div>

                        {/* Password */}
                        <div>
                            <label className='block text-sm font-medium text-slate-700 mb-1.5'>Password</label>
                            <div className="relative">
                                <FiLock className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
                                <input
                                    value={user.password}
                                    onChange={(e) => setUser({ ...user, password: e.target.value })}
                                    className='w-full pl-11 pr-11 py-3 rounded-xl bg-slate-50 border border-slate-200 text-slate-900 placeholder-slate-400 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100 transition'
                                    type={showPassword ? "text" : "password"}
                                    placeholder='Enter your password' />
                                <button
                                    type="button"
                                    onClick={() => setShowPassword(!showPassword)}
                                    className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                                    {showPassword ? <FiEye /> : <FiEyeOff />}
                                </button>
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className='w-full py-3 rounded-xl font-semibold text-white bg-blue-600 hover:bg-blue-700 active:scale-[0.99] transition disabled:opacity-60'>
                            {loading ? "Signing in..." : "Login"}
                        </button>

                        <p className='text-center text-sm text-slate-500'>
                            Don't have an account?{" "}
                            <Link to="/signup" className="text-blue-600 font-semibold hover:underline">Sign up</Link>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default Login
