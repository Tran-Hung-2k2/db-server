import { NavLink } from 'react-router-dom';
import image from '@assets/images/signin.svg';

export default function AuthLayout({ children }) {
    return (
        <div className="flex items-center justify-center w-screen h-screen">
            <NavLink to="/" className="w-3/5">
                <div className="w-full p-32">
                    <img className="border rounded-lg border-primary" src={image} alt="DEP Viettel" />
                </div>
            </NavLink>
            {children}
        </div>
    );
}
