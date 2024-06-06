import { useState } from 'react';

import Header from '@components/Header';
import Sidebar from '@components/Sidebar';

const MainLayout = ({ children }) => {
    const [open, setOpen] = useState(false);
    return (
        <main className="relative flex min-h-screen">
            <div className={`${!open ? 'absolute' : ''} top-0 left-0 h-full drawer drawer-open max-w-fit`}>
                <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
                <Sidebar className="min-w-[300px] h-full pb-20" open={open} setOpen={setOpen} />
            </div>
            <div className={`${!open ? 'ml-20' : ''} w-screen mb-20 `}>
                <Header />
                {children}
            </div>
        </main>
    );
};

export default MainLayout;
