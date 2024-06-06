import { useEffect, useState } from 'react';
import { GrPrevious } from 'react-icons/gr';
import { GrNext } from 'react-icons/gr';

export default function Pagination({ skip, setSkip, limit, total }) {
    const [customPage, setCustomPage] = useState(0);

    useEffect(() => {
        setCustomPage(skip / limit + 1);
    }, [skip]);

    return (
        <div className="mt-4 join">
            <button
                className="bg-white border-none join-item btn"
                onClick={() => {
                    if (skip - limit >= 0) setSkip((prevSkip) => prevSkip - limit);
                }}
            >
                <GrPrevious />
            </button>
            <p className="z-20 grid content-center translate-x-2 join-item">Trang</p>
            <input
                value={customPage}
                type="number"
                onChange={(e) => {
                    setCustomPage(e.target.value);
                }}
                onKeyDown={(e) => {
                    if (e.key === 'Enter')
                        if (e.target.value <= 0) {
                            setCustomPage(1);
                            setSkip(0);
                        } else if (e.target.value > Math.ceil(total / limit)) {
                            setCustomPage(Math.ceil(total / limit));
                            setSkip((Math.ceil(total / limit) - 1) * limit);
                        } else setSkip((e.target.value - 1) * limit);
                }}
                className="grid content-center w-12 font-semibold -translate-y-px bg-white border-none input join-item focus:outline-none"
                style={{
                    MozAppearance: 'textfield',
                }}
            />
            <p className="grid content-center -translate-x-4 join-item">/ {Math.ceil(total / limit)}</p>
            <button
                className="bg-white border-none join-item btn"
                onClick={() => {
                    if (skip + limit < total) setSkip((prevSkip) => prevSkip + limit);
                }}
            >
                <GrNext />
            </button>
        </div>
    );
}
