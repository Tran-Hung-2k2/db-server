export default function Page() {
    return (
        <main className="grid min-h-full px-6 py-6 bg-white">
            <div className="text-center mt-36">
                <p className="text-6xl font-semibold text-primary">404</p>
                <h1 className="mt-4 text-3xl font-bold tracking-tight text-gray-900 sm:text-5xl">
                    Không tìm thấy trang
                </h1>
                <p className="mt-6 text-base leading-7 text-gray-600">
                    Xin lỗi, chúng tôi không thể tìm thấy trang bạn muốn truy cập.
                </p>
                <div className="flex items-center justify-center mt-10 gap-x-6">
                    <a
                        href="/"
                        className="rounded-md bg-primary px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-secondary focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
                    >
                        Trở lại trang chủ
                    </a>
                </div>
            </div>
        </main>
    );
}
