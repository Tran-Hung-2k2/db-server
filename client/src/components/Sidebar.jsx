import { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { IoMenu } from 'react-icons/io5';
import { HiArrowNarrowLeft } from 'react-icons/hi';

import sidebarAvatar from '@assets/images/sidebar.svg';
import favicon from '@assets/images/favicon.svg';
import menuItem from '@constants/sidebar';

export default function Component({ className }) {
    const { user } = useSelector((state) => state.auth);

    const [open, setOpen] = useState(false);

    return (
        <div className={`overflow-x-hidden bg-white border shadow-md drawer-side ${open ? className : ''}`}>
            <label htmlFor="my-drawer-2" aria-label="close sidebar" className="drawer-overlay"></label>
            <ul className="p-3 bg-white menu">
                {/* Sidebar content here */}
                {/* <!-- SIDEBAR HEADER --> */}
                <div className="relative flex items-center justify-between gap-2 px-6 pt-2">
                    {open && (
                        <NavLink to="/" className="flex items-center justify-center w-full">
                            <img className="w-40 mt-4 mr-4" src={sidebarAvatar} alt="Viettel High Tech" />
                        </NavLink>
                    )}
                    <label className={`absolute right-0 top-5 swap swap-rotate ${open ? '' : 'right-2.5'}`}>
                        {/* this hidden checkbox controls the state */}
                        <input
                            onClick={(e) => {
                                setOpen(!open);
                            }}
                            type="checkbox"
                        />

                        {/* hamburger icon */}
                        <img className="fill-current swap-off" src={favicon} alt="Viettel High Tech" />

                        {/* close icon */}
                        <HiArrowNarrowLeft size={28} className="fill-current swap-on text-zinc-500" />
                    </label>
                </div>
                {/* <!-- SIDEBAR HEADER --> */}

                <div className="flex flex-col overflow-y-auto duration-300 ease-linear no-scrollbar">
                    {/* <!-- Sidebar Menu --> */}
                    {open ? (
                        <nav className="lg:px-2">
                            {/* <!-- Menu Group --> */}
                            <ul className="w-full menu rounded-box">
                                {menuItem.map((item, index) =>
                                    item.label ? (
                                        <h3
                                            key={index}
                                            className="pt-1 pb-1 mt-6 ml-4 text-lg font-bold text-bodylight2 dark:text-white"
                                        >
                                            {item.label}
                                        </h3>
                                    ) : item.role.includes(user.role) ? (
                                        <li key={index}>
                                            {item.child ? (
                                                <details open>
                                                    <summary className="relative text-lg gap-2.5 rounded-sm py-2 px-4 font-medium text-bodylight1 duration-300 ease-in-out dark:hover:bg-meta-4 dark:text-white">
                                                        <span className={`w-6 h-4.5`}>{item.icon}</span>
                                                        {item.title}
                                                    </summary>
                                                    <ul>
                                                        {item.child.map((subItem, subIndex) =>
                                                            subItem.role.includes(user.role) ? (
                                                                <li key={subIndex}>
                                                                    <NavLink
                                                                        to={subItem.path}
                                                                        className={({ isActive }) =>
                                                                            'text-base relative flex items-center gap-2.5 rounded-md font-medium duration-300 ease-in-out hover:text-bodylight dark:text-white transform hover:scale-105 ' +
                                                                            (isActive && 'link-primary')
                                                                        }
                                                                    >
                                                                        {subItem.title}
                                                                    </NavLink>
                                                                </li>
                                                            ) : (
                                                                <p key={subIndex}></p>
                                                            ),
                                                        )}
                                                    </ul>
                                                </details>
                                            ) : (
                                                <NavLink
                                                    to={item.path}
                                                    className={({ isActive }) =>
                                                        (isActive && '!bg-primary !text-white') +
                                                        ' dark:hover:bg-meta-4 text-lg rounded-md  font-medium text-bodylight1 duration-300 ease-in-out dark:text-white transform hover:scale-105'
                                                    }
                                                >
                                                    <span className={`w-6 h-4.5`}>{item.icon}</span>
                                                    {item.title}
                                                </NavLink>
                                            )}
                                        </li>
                                    ) : (
                                        <p key={index}></p>
                                    ),
                                )}
                            </ul>
                        </nav>
                    ) : (
                        <ul className="w-full p-0 mt-16 menu rounded-box">
                            {menuItem.map(
                                (item, index) =>
                                    !item.label &&
                                    item.child &&
                                    item.role.includes(user.role) &&
                                    item?.child[0].role.includes(user.role) && (
                                        <li key={index}>
                                            <NavLink
                                                to={item?.child[0].path}
                                                className={({ isActive }) =>
                                                    'bg-stone-100 px-0 my-2 flex justify-center focus:text-white ' +
                                                    (isActive && '!bg-red-600 !text-white')
                                                }
                                            >
                                                {item.bigIcon || item.icon}
                                            </NavLink>
                                        </li>
                                    ),
                            )}
                        </ul>
                    )}
                    {/* <!-- Sidebar Menu --> */}
                </div>
            </ul>
        </div>
    );
}
