// Initials from a user's name (e.g. "Aisha Khan" -> "AK")
export const initials = (user) => {
    const name = (user?.fullName || user?.username || "User").trim();
    const parts = name.split(/\s+/);
    const a = parts[0]?.[0] || "U";
    const b = parts[1]?.[0] || "";
    return (a + b).toUpperCase();
};

// Pick a stable color from a small blue/teal palette based on the name.
const palette = ["#2563eb", "#3b82f6", "#0ea5e9", "#0891b2", "#0d9488", "#06b6d4"];
const colorFor = (user) => {
    const key = user?.username || user?.fullName || "U";
    let h = 0;
    for (let i = 0; i < key.length; i++) h = key.charCodeAt(i) + ((h << 5) - h);
    return palette[Math.abs(h) % palette.length];
};

// A locally-generated initials avatar (SVG data URI) — always renders, no network needed.
export const defaultAvatar = (user) => {
    const text = initials(user);
    const bg = colorFor(user);
    const svg = `<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'><rect width='100' height='100' fill='${bg}'/><text x='50' y='50' dy='.35em' font-size='42' fill='#ffffff' text-anchor='middle' font-family='Arial, sans-serif' font-weight='600'>${text}</text></svg>`;
    return `data:image/svg+xml,${encodeURIComponent(svg)}`;
};

// Use the photo ONLY if the user actually uploaded one (stored as a base64 data URI).
// The old auto-generated external avatar URLs often fail to load, so we always
// fall back to a clean local initials avatar for those.
export const avatarSrc = (user) => {
    const p = user?.profilePhoto;
    if (p && p.startsWith("data:")) return p; // user-uploaded image
    return defaultAvatar(user);
};

// onError handler — if the photo URL fails, fall back to the local initials avatar.
export const avatarOnError = (user) => (e) => {
    e.currentTarget.onerror = null;
    e.currentTarget.src = defaultAvatar(user);
};
