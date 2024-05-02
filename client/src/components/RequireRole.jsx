import React, { useEffect } from 'react';
import { useSelector } from 'react-redux';
import { Navigate, Outlet, useLocation } from 'react-router-dom';

function RequireRole({ roles, children }) {
    const { user } = useSelector((state) => state.auth);
    const location = useLocation();

    // useEffect(() => {
    //     console.log(user);
    // }, []);

    return user && roles.includes(user?.role) ? children : <Navigate to="/signin" state={{ from: location }} replace />;
}

export default RequireRole;
