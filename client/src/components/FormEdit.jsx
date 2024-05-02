import { useState, useEffect } from 'react';

import ButtonBack from './ButtonBack';
import Loader from './Loader';

function FormEdit({ fields, title, onSubmit, getData, children }) {
    const [loading, setLoading] = useState(true);
    const fieldsState = fields.reduce(
        (acc, field) => ({ ...acc, [field.id]: field.type == 'checkbox' ? true : '' }),
        {},
    );
    const [state, setState] = useState(fieldsState);

    const handleChange = (e) => {
        if (e.target.type === 'file') {
            setState((prevState) => ({ ...prevState, [e.target.id]: e.target.files[0] }));
        } else if (e.target.type === 'checkbox') {
            setState((prevState) => ({ ...prevState, [e.target.id]: e.target.checked }));
        } else {
            setState({ ...state, [e.target.id]: e.target.value });
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            const data = await getData();
            setState((prevState) => ({ ...prevState, ...data }));
            setLoading(false);
        };

        fetchData();
    }, []);

    return (
        <>
            {loading ? (
                <Loader />
            ) : (
                <>
                    <ButtonBack className="ml-6" />
                    <form className="m-6 space-y-6 h-fit" onSubmit={(e) => onSubmit(e, state)}>
                        <h3 className="text-2xl font-bold text-primary">{title}</h3>
                        <div className="flex flex-col space-y-4 h-fit">
                            {children}
                            {fields.map((field, index) => (
                                <div key={field.id}>
                                    <label htmlFor={field.id} className="block mb-2 font-medium">
                                        {field.label}
                                    </label>
                                    {(() => {
                                        switch (field.type) {
                                            case 'textarea':
                                                return (
                                                    <textarea
                                                        {...field}
                                                        value={state[field.id]}
                                                        onChange={handleChange}
                                                        className="w-full h-24 textarea textarea-primary"
                                                    ></textarea>
                                                );
                                            case 'checkbox':
                                                return (
                                                    <input
                                                        {...field}
                                                        type="checkbox"
                                                        checked={state[field.id]}
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
                                                        className="w-full max-w-xs file-input file-input-bordered file-input-primary"
                                                        required={false}
                                                    />
                                                );
                                            case 'select':
                                                return (
                                                    <select
                                                        name="select"
                                                        className="w-full max-w-xs select select-primary"
                                                        onChange={handleChange}
                                                        value={state[field.id]}
                                                        {...field}
                                                    >
                                                        <option disabled>{field.placeholder}</option>
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
                                            default:
                                                return (
                                                    <input
                                                        value={state[field.id]}
                                                        onChange={handleChange}
                                                        {...field}
                                                        className="w-full max-w-xl input input-bordered input-primary"
                                                    />
                                                );
                                        }
                                    })()}
                                </div>
                            ))}
                        </div>

                        <button type="submit" className="btn btn-active btn-primary">
                            {title}
                        </button>
                    </form>
                </>
            )}
        </>
    );
}

export default FormEdit;
