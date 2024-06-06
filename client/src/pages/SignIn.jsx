import { useEffect, useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';

import fields from '@constants/form/signin';
import action from '@redux/auth/auth.action';
import InputPassword from '@/components/InputPasswod';

const fieldsState = fields.reduce((acc, field) => ({ ...acc, [field.id]: '' }), {});

export default function Page() {
    const [state, setState] = useState(fieldsState);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    useEffect(() => {
        document.title = 'Sign In | DEP';
    }, []);

    const handleChange = (e) => {
        setState({ ...state, [e.target.id]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        dispatch(
            action.signin(state, () => {
                navigate('/');
            }),
        );
    };

    return (
        <form className="m-auto -translate-x-36 w-200" onSubmit={handleSubmit}>
            <h3 className="mb-2 text-2xl font-bold text-primary">Đăng nhập</h3>
            <div>
                Bạn chưa có tài khoản?
                <NavLink to="/signup" className="ml-2 text-primary">
                    Đăng ký ngay
                </NavLink>
            </div>
            <div className="flex flex-col mt-6 space-y-4 w-80">
                {fields.map((field) => {
                    switch (field.type) {
                        case 'password':
                            return (
                                <label key={field.id} className="flex items-center gap-2 input input-primary">
                                    {field.icon}
                                    <InputPassword onChange={handleChange} {...field} className="grow" />
                                </label>
                            );
                        default:
                            return (
                                <label key={field.id} className="flex items-center gap-2 input input-primary">
                                    {field.icon}
                                    <input onChange={handleChange} {...field} className="grow" />
                                </label>
                            );
                    }
                })}
            </div>
            <div className="mt-2 mb-4 text-primary">
                <NavLink to="/forget_passord">Quên mật khẩu?</NavLink>
            </div>
            <button type="submit" className="btn btn-active btn-primary">
                Đăng nhập
            </button>
        </form>
    );
}
