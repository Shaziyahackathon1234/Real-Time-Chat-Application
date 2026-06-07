import React from 'react'
import OtherUser from './OtherUser';
import useGetOtherUsers from '../hooks/useGetOtherUsers';
import { useSelector } from "react-redux";

const OtherUsers = () => {
    // my custom hook
    useGetOtherUsers();
    const { otherUsers } = useSelector(store => store.user);
    console.log("otherUsers",otherUsers)
    if (!otherUsers) return null; // early return in react

    return (
        <div className='h-full overflow-auto py-2 space-y-1'>
            {
                otherUsers?.map((user) => {
                    return (
                        <OtherUser key={user._id} user={user} />
                    )
                })
            }
        </div>
    )
}

export default OtherUsers
