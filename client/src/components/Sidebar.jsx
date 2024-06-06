import { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { IoMenu } from 'react-icons/io5';
import { HiArrowNarrowLeft } from 'react-icons/hi';

import sidebarAvatar from '@assets/images/sidebar.svg';
import favicon from '@assets/images/favicon.svg';
import viettelText from '@assets/images/viettel.png';
import menuItem from '@constants/sidebar';

export default function Component({ className, open, setOpen }) {
    const { user } = useSelector((state) => state.auth);

    const [hover, setHover] = useState(false);

    return (
        <div
            className={`overflow-x-hidden z-50 bg-white border shadow-md drawer-side ${open ? className : ''}`}
            onMouseEnter={(e) => {
                setHover(true);
            }}
            onMouseLeave={(e) => {
                setHover(false);
            }}
        >
            <label htmlFor="my-drawer-2" aria-label="close sidebar" className="drawer-overlay"></label>
            <ul className="!p-0 bg-white menu">
                {/* Sidebar content here */}
                {/* <!-- SIDEBAR HEADER --> */}
                <div className="items-center justify-between gap-2 px-6 pt-2 lex ">
                    {open && (
                        <NavLink to="/" className="flex items-center justify-center w-full">
                            <img className="w-40 mt-4 mr-4" src={sidebarAvatar} alt="Viettel High Tech" />
                        </NavLink>
                    )}
                    <label className={`absolute left-60 top-5 swap swap-rotate ${open ? '' : '!left-6'}`}>
                        {/* this hidden checkbox controls the state */}
                        <input
                            onClick={(e) => {
                                setOpen(!open);
                            }}
                            type="checkbox"
                        />

                        {/* hamburger icon */}
                        <div className="flex items-center gap-5 fill-current swap-off">
                            <img className="inline-block h-10" src={favicon} alt="Viettel High Tech" />

                                {hover && <img className="inline-block object-cover w-32 h-10 -translate-x-3" src={viettelText} alt="" />}
                        </div>

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
                            <ul className="w-full menu rounded-box !p-0">
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
                        <ul className="w-full mt-16 menu rounded-box !p-0">
                            {menuItem.map(
                                (item, index) =>
                                    !item.label &&
                                    item.child &&
                                    item.role.includes(user.role) &&
                                    item?.child[0].role.includes(user.role) && (
                                        <li key={index}>
                                            {hover ? (
                                                <NavLink
                                                    to={item?.child[0].path}
                                                    className={({ isActive }) =>
                                                        'relative pl-4 py-2 focus:text-white rounded-none text-base font-semibold hover:bg-stone-100 ' +
                                                        (isActive && '!bg-red-600 !text-white')
                                                    }
                                                >
                                                    {({ isActive }) => (
                                                        <>
                                                            <span
                                                                className={`p-2 rounded-md ${
                                                                    isActive ? 'bg-red-700' : 'bg-stone-200'
                                                                }`}
                                                            >
                                                                {item.bigIcon || item.icon}
                                                            </span>
                                                            <div className="pr-24">{item.title}</div>
                                                        </>
                                                    )}
                                                </NavLink>
                                            ) : (
                                                <div className="py-2 pl-4 text-base font-semibold rounded-none focus:text-white">
                                                    <NavLink
                                                        to={item?.child[0].path}
                                                        className={({ isActive }) =>
                                                            `p-2 rounded-md ${
                                                                isActive ? 'bg-red-600 !text-white' : 'bg-stone-200'
                                                            }`
                                                        }
                                                    >
                                                        {item.bigIcon || item.icon}
                                                    </NavLink>
                                                </div>
                                            )}
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
