import { useEffect, useState } from 'react';
import { GrNext } from 'react-icons/gr';
import { VscFilter } from 'react-icons/vsc';

export default function Component({ filter, setFilter, getValues, filterFields, getStaticValues }) {
    const [valueFilter, setValueFilter] = useState({});
    const [filterValues, setFilterValues] = useState([]);
    const [fieldOpen, setFieldOpen] = useState(filterFields[0].fieldName);

    useEffect(() => {
        const fetchData = async () => {
            let res;
            if (getStaticValues != undefined) {
                res = getStaticValues(fieldOpen);
                setFilterValues(res);
            } else {
                res = await getValues({ field: fieldOpen });
                setFilterValues(res.data);
            }
        };

        fetchData();
    }, [fieldOpen]);

    const handleClick = () => {
        const elem = document.activeElement;
        if (elem) {
            elem?.blur();
        }
    };

    return (
        <div className={`dropdown dropdown-bottom dropdown-start`}>
            <button
                tabIndex={0}
                role="button"
                className="h-10 py-2 mb-1 font-bold bg-white border btn-sm btn border-primary text-primary hover:bg-white hover:border-primary hover:opacity-75"
            >
                <VscFilter className="text-xl" />
                Lọc
            </button>
            <div
                tabIndex={0}
                className="flex dropdown-content z-[1] menu shadow bg-base-100 rounded-box w-fit border border-3  border-zinc-300 p-0"
            >
                <div className="flex">
                    <ul tabIndex={0} className="z-[1] shadow bg-base-100 w-32 h-36 rounded-l-lg overflow-auto">
                        {filterFields.map((field, index) => (
                            <li key={index}>
                                <div
                                    className={`flex justify-between ${fieldOpen === field.name ? 'bg-zinc-300' : ''} ${
                                        valueFilter[field.name] ? 'text-primary' : ''
                                    }`}
                                    onClick={() => setFieldOpen(field.name)}
                                >
                                    <div>{field.label}</div> <GrNext />
                                </div>
                            </li>
                        ))}
                    </ul>
                    <ul tabIndex={0} className="z-[1] shadow bg-base-100 h-36 rounded-r-lg overflow-auto w-60">
                        {filterValues?.map((value, index) => (
                            <li
                                key={index}
                                className={`${valueFilter[fieldOpen] == value ? 'bg-primary text-white' : ''}`}
                                onClick={() => {
                                    if (valueFilter[fieldOpen] != value)
                                        setValueFilter({ ...valueFilter, [fieldOpen]: value });
                                    else setValueFilter({ ...valueFilter, [fieldOpen]: '' });
                                }}
                            >
                                <div>{value}</div>
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="flex justify-start gap-2 m-2">
                    <button
                        className="h-8 py-2 text-white btn btn-xs btn-primary"
                        onClick={() => {
                            setFilter(valueFilter);
                            handleClick();
                        }}
                    >
                        Áp dụng
                    </button>
                    <button
                        className="h-8 py-2 btn btn-xs btn-outline hover:bg-white hover:text-black hover:opacity-75"
                        onClick={() => {
                            setFilter({});
                            setValueFilter({});
                            handleClick();
                        }}
                    >
                        Đặt lại
                    </button>
                </div>
            </div>
        </div>
    );
}
