// Uploads media to Cloudinary if configured; otherwise returns the data URI
// directly (so image/file sending works even before you set up Cloudinary).
let _cloudinary = null;

const getCloudinary = async () => {
    if (_cloudinary) return _cloudinary;
    const { CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET } = process.env;
    if (!CLOUDINARY_CLOUD_NAME || !CLOUDINARY_API_KEY || !CLOUDINARY_API_SECRET) {
        return null; // not configured -> caller will fall back to inline data
    }
    try {
        const mod = await import("cloudinary");
        const c = mod.v2 || mod.default?.v2 || mod.default;
        c.config({
            cloud_name: CLOUDINARY_CLOUD_NAME,
            api_key: CLOUDINARY_API_KEY,
            api_secret: CLOUDINARY_API_SECRET,
        });
        _cloudinary = c;
        return c;
    } catch (e) {
        console.log("Cloudinary not installed; using inline fallback.");
        return null;
    }
};

// Accepts a base64 data URI. Returns a hosted URL (Cloudinary) or the data URI itself.
export const uploadMedia = async (dataUri) => {
    if (!dataUri) return "";
    const c = await getCloudinary();
    if (!c) return dataUri; // fallback: store the data URI directly
    try {
        const res = await c.uploader.upload(dataUri, { resource_type: "auto", folder: "chatwave" });
        return res.secure_url;
    } catch (e) {
        console.log("Cloudinary upload failed, using inline fallback:", e.message);
        return dataUri;
    }
};
