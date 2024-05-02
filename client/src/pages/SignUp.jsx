import { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';

import fields from '@constants/form/signup';
import api from '@api/auth';

const fieldsState = fields.reduce((acc, field) => ({ ...acc, [field.id]: '' }), {});

export default function Page() {
    const [loading, setLoading] = useState(false);
    const [state, setState] = useState(fieldsState);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setState({ ...state, [e.target.id]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            setLoading(true);
            await api.signup(state);
        } finally {
            setLoading(false);
        }

        navigate('/signin');
    };

    return (
        <form className="m-auto -translate-x-36 w-200" onSubmit={handleSubmit}>
            <h3 className="mb-2 text-2xl font-bold text-primary">Đăng ký</h3>
            <div>
                Bạn đã có tài khoản?
                <NavLink to="/signin" className="ml-2 text-primary">
                    Đăng nhập ngay
                </NavLink>
            </div>
            <div className="flex flex-col my-6 space-y-4 w-80">
                {fields.map((field) => (
                    <input
                        key={field.id}
                        onChange={handleChange}
                        {...field}
                        className="w-full max-w-xl input input-bordered input-primary"
                    />
                ))}
            </div>

            <button type="submit" className={`btn btn-active btn-primary ${loading && 'btn-disabled'}`}>
                Đăng ký
            </button>
        </form>
    );
}
