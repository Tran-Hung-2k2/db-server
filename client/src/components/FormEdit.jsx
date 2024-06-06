import { useEffect, useState } from 'react';
import Loader from './Loader';
import InputPassword from './InputPasswod';

export default function Component({ fields, title, onSubmit, getData, children, reload }) {
    // Khởi tạo trạng thái ban đầu cho các trường
    const fieldsState = fields.reduce(
        (acc, field) => ({ ...acc, [field.name]: field.type == 'checkbox' ? true : '' }),
        {},
    );

    const [loading, setLoading] = useState(true);
    // Sử dụng hook useState để quản lý trạng thái của các trường
    const [state, setState] = useState(fieldsState);

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            const data = await getData();
            setState(() => ({ ...fieldsState, ...data }));
            setLoading(false);
        };

        fetchData();
    }, [reload]);

    // Hàm xử lý sự thay đổi của các trường
    const handleChange = (e) => {
        if (e.target.type === 'file') {
            setState({ ...state, [e.target.name]: e.target.files[0] });
        } else if (e.target.type === 'checkbox') {
            setState({ ...state, [e.target.name]: e.target.checked });
        } else {
            setState({ ...state, [e.target.name]: e.target.value });
        }
    };

    // Render component
    return (
        <>
            {loading ? (
                <Loader />
            ) : (
                <form className="m-2 space-y-6" onSubmit={(e) => onSubmit(e, state)}>
                    <h3 className="text-xl font-bold text-primary">{title}</h3>
                    <div className="grid grid-cols-2 gap-4">
                        {children}
                        {fields.map((field) => (
                            <div key={field.name} className={field.col == 1 ? '' : 'col-span-2'}>
                                {!field.inline_label && (
                                    <label htmlFor={field.name} className="block mb-2 font-medium">
                                        {field.label}
                                    </label>
                                )}
                                {(() => {
                                    // Dựa vào loại trường để render input tương ứng
                                    switch (field.type) {
                                        case 'textarea':
                                            return (
                                                <textarea
                                                    {...field}
                                                    onChange={handleChange}
                                                    value={state[field.name]}
                                                    className={`w-full h-12 leading-6 textarea textarea-primary ${field.className}`}
                                                ></textarea>
                                            );
                                        case 'checkbox':
                                            return (
                                                <input
                                                    {...field}
                                                    type="checkbox"
                                                    checked={state[field.name]}
                                                    defaultChecked
                                                    onChange={handleChange}
                                                    className="checkbox"
                                                />
                                            );
                                        case 'file':
                                            return (
                                                <input
                                                    type="file"
                                                    {...field}
                                                    onChange={handleChange}
                                                    className="w-full file-input file-input-bordered file-input-primary"
                                                />
                                            );
                                        case 'select':
                                            return (
                                                <select
                                                    name="select"
                                                    className="w-full select select-primary"
                                                    onChange={handleChange}
                                                    value={state[field.name]}
                                                    disabled={field?.disable}
                                                    {...field}
                                                >
                                                    <option value="">{field.placeholder}</option>
                                                    {field.options.map((option) => (
                                                        <option
                                                            key={Object.keys(option)[0]}
                                                            value={Object.keys(option)[0]}
                                                        >
                                                            {Object.values(option)[0]}
                                                        </option>
                                                    ))}
                                                </select>
                                            );
                                        case 'password':
                                            return field.inline_label ? (
                                                <label className="flex items-center gap-2 input input-primary input-bordered">
                                                    {field.label}
                                                    <InputPassword
                                                        value={state[field.name]}
                                                        onChange={handleChange}
                                                        {...field}
                                                        className="grow"
                                                    />
                                                </label>
                                            ) : (
                                                <InputPassword
                                                    value={state[field.name]}
                                                    onChange={handleChange}
                                                    {...field}
                                                    className="w-full input input-bordered input-primary"
                                                />
                                            );
                                        default:
                                            return field.inline_label ? (
                                                <label className="flex items-center gap-2 input input-primary input-bordered">
                                                    {field.label}
                                                    <input
                                                        value={state[field.name]}
                                                        onChange={handleChange}
                                                        {...field}
                                                        className="grow"
                                                    />
                                                </label>
                                            ) : (
                                                <input
                                                    value={state[field.name]}
                                                    onChange={handleChange}
                                                    {...field}
                                                    className="w-full input input-bordered input-primary"
                                                />
                                            );
                                    }
                                })()}
                            </div>
                        ))}
                    </div>

                    <button type="submit" className="text-white btn btn-active btn-primary">
                        {title}
                    </button>
                </form>
            )}
        </>
    );
}
