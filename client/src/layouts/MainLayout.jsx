import Header from '@components/Header';
import Sidebar from '@components/Sidebar';

const MainLayout = ({ children }) => {
    return (
        <main className="flex">
            <div className="sticky top-0 left-0 h-full drawer drawer-open max-w-fit">
                <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
                <Sidebar className="min-w-[300px]" />
            </div>
            <div className="w-screen mb-20">
                <Header />
                {children}
            </div>
        </main>
    );
};

export default MainLayout;
