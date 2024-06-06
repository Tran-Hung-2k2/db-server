import Avatar from 'react-avatar';
import { CgProfile } from 'react-icons/cg';
import { IoSettingsOutline } from 'react-icons/io5';
import { HiOutlineLogout } from 'react-icons/hi';
import { PiPassword } from 'react-icons/pi';
import { useDispatch, useSelector } from 'react-redux';

import action from '../redux/auth/auth.action';

export default function Component() {
    const { user } = useSelector((state) => state.auth);

    const dispatch = useDispatch();

    return (
        <div className="justify-end pt-4 h-fit bg-slate-50 navbar">
            
            <div className="flex items-center mr-16">
                <div className="inline-block mr-4">
                    <p className="text-base font-bold text-primary">{user.name}</p>
                    <p className="text-sm">{user.email}</p>
                </div>
                <div className="w-full dropdown dropdown-hover dropdown-bottom dropdown-end">
                    <div tabIndex={0} role="button" className="btn btn-circle">
                        <Avatar size="42" round={true} name={user?.name || 'Default Name'} />
                    </div>

                    <ul className="mt-1 z-[1] p-2 drop-shadow-2xl menu menu-md dropdown-content bg-base-100 rounded-box w-60">
                        <li>
                            <a href="/profile" className="text-lg hover:text-lime-700">
                                <CgProfile className="w-5 h-5" /> Thông tin tài khoản
                            </a>
                        </li>
                        <li>
                            <a href="/change_password" className="text-lg hover:text-lime-700">
                                <PiPassword className="w-5 h-5" /> Đổi mật khẩu
                            </a>
                        </li>
                        <li>
                            <a href="/setting" className="text-lg hover:text-lime-700">
                                <IoSettingsOutline className="w-5 h-5" /> Cài đặt
                            </a>
                        </li>
                        <li
                            onClick={(e) => {
                                e.preventDefault();
                                dispatch(action.logout());
                            }}
                        >
                            <a href="#" className="text-lg border-t-2 hover:text-lime-700">
                                <HiOutlineLogout className="w-5 h-5" /> Đăng xuất
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
