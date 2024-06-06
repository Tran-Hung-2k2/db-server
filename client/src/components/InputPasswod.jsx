import { useState } from 'react';
import { BiShow } from 'react-icons/bi';
import { BiHide } from 'react-icons/bi';

export default function InputPassword({ ...fields }) {
    const [showPassword, setShowPassword] = useState(false);

    return (
        <>
            <input {...fields} type={showPassword ? 'text' : 'password'} />
            <button type="button" className="-ml-8 focus:outline-none" onClick={() => setShowPassword(!showPassword)}>
                {showPassword ? <BiShow size={20} /> : <BiHide size={20} />}
            </button>
        </>
    );
}
