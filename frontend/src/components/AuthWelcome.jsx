import React from 'react'
import { HiOutlineChatBubbleLeftRight } from "react-icons/hi2";
import { FiZap, FiImage, FiUser } from "react-icons/fi";
import { BsCircleFill } from "react-icons/bs";

const features = [
    { icon: <FiZap />, title: "Real-time messaging", desc: "Instant delivery, powered by sockets." },
    { icon: <FiImage />, title: "Share images & media", desc: "Send photos and moments easily." },
    { icon: <FiUser />, title: "Create your profile", desc: "Personalize your name and avatar." },
    { icon: <BsCircleFill className="text-green-300 text-xs" />, title: "See who's online", desc: "Live presence for every friend." },
];

const AuthWelcome = () => {
    return (
        <div className="hidden md:flex flex-col justify-between w-1/2 p-10 lg:p-14 bg-gradient-to-br from-blue-600 to-blue-800 text-white relative overflow-hidden">
            {/* decorative glow */}
            <div className="absolute -top-16 -right-16 w-72 h-72 rounded-full bg-white/10"></div>
            <div className="absolute -bottom-24 -left-10 w-80 h-80 rounded-full bg-white/5"></div>

            {/* Brand */}
            <div className="relative flex items-center gap-3">
                <div className="w-11 h-11 rounded-xl bg-white text-blue-600 flex items-center justify-center">
                    <HiOutlineChatBubbleLeftRight className="text-2xl" />
                </div>
                <span className="text-xl font-bold tracking-tight">ChatWave</span>
            </div>

            {/* Headline */}
            <div className="relative max-w-md">
                <h2 className="text-4xl font-bold leading-snug">
                    Real-time communication,<br />reimagined.
                </h2>
                <p className="text-blue-100 mt-4 text-base leading-relaxed">
                    Connect instantly, share images and moments, and stay close with friends — all in one clean, fast place.
                </p>

                {/* Feature list */}
                <div className="mt-9 space-y-5">
                    {features.map((f, i) => (
                        <div key={i} className="flex items-start gap-3">
                            <div className="w-10 h-10 rounded-lg bg-white/15 flex items-center justify-center text-white shrink-0">
                                {f.icon}
                            </div>
                            <div>
                                <p className="text-sm font-semibold">{f.title}</p>
                                <p className="text-xs text-blue-200">{f.desc}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <p className="relative text-xs text-blue-200">© {new Date().getFullYear()} ChatWave · Stay connected.</p>
        </div>
    )
}

export default AuthWelcome
