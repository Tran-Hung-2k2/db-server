import { useState } from 'react';

import ButtonBack from './ButtonBack';

function FormAdd({ fields, title, onSubmit, children }) {
    const fieldsState = fields.reduce(
        (acc, field) => ({ ...acc, [field.id]: field.type == 'checkbox' ? true : '' }),
        {},
    );
    const [state, setState] = useState(fieldsState);

    const handleChange = (e) => {
        if (e.target.type === 'file') {
            setState({ ...state, [e.target.id]: e.target.files[0] });
        } else if (e.target.type === 'checkbox') {
            setState({ ...state, [e.target.id]: e.target.checked });
        } else {
            setState({ ...state, [e.target.id]: e.target.value });
        }
    };

    return (
        <form className="m-6 space-y-6 h-fit" onSubmit={(e) => onSubmit(e, state)}>
            <ButtonBack />
            <h3 className="text-2xl font-bold text-primary">{title}</h3>
            <div className="flex flex-col space-y-4 h-fit">
                {children}
                {fields.map((field) => (
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
                                            onChange={handleChange}
                                            className="w-full h-24 textarea textarea-primary"
                                        ></textarea>
                                    );
                                case 'checkbox':
                                    return (
                                        <input
                                            {...field}
                                            type="checkbox"
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
                                            className="w-full max-w-xs file-input file-input-bordered file-input-primary"
                                        />
                                    );
                                case 'select':
                                    return (
                                        <select
                                            name="select"
                                            className="w-full max-w-xs select select-primary"
                                            onChange={handleChange}
                                            {...field}
                                            defaultValue={field.placeholder}
                                        >
                                            <option value=''>{field.placeholder}</option>
                                            {field.options.map((option) => (
                                                <option key={Object.keys(option)[0]} value={Object.keys(option)[0]}>
                                                    {Object.values(option)[0]}
                                                </option>
                                            ))}
                                        </select>
                                    );
                                default:
                                    return (
                                        <input
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
    );
}

export default FormAdd;
