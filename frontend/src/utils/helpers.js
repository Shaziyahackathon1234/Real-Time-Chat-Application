// Format an ISO date like "2026-05-25T18:09:05.393Z" -> "25 May 2026"
export const formatJoined = (iso) => {
    if (!iso) return "—";
    try {
        const d = new Date(iso);
        if (isNaN(d.getTime())) return "—";
        return d.toLocaleDateString("en-GB", { day: "numeric", month: "short", year: "numeric" });
    } catch {
        return "—";
    }
};

// A user is shown as online only if they're connected AND haven't hidden their status.
export const isUserOnline = (user, onlineUsers) => {
    if (!user) return false;
    if (user.showStatus === false) return false; // user disabled status visibility
    return Array.isArray(onlineUsers) && onlineUsers.includes(user._id);
};
