import { confirmAlert } from 'react-confirm-alert';
import 'react-confirm-alert/src/react-confirm-alert.css';

const confirm = (options) => {
    // {
    //     title: ...,
    //     message: ...,
    //     onConfirm: ...,
    // }
    confirmAlert({
        customUI: ({ onClose }) => {
            return (
                <div className="">
                    <div className="modal modal-open" role="dialog">
                        <div className="modal-box">
                            <h3 className="text-lg font-bold">{options.title || 'Xác nhận'}</h3>
                            <p className="py-4">{options.message || 'Bạn có chắc muốn thực hiện không?'}</p>
                            <div className="flex justify-end gap-2">
                                <button
                                    onClick={() => {
                                        if (options.onConfirm) options.onConfirm();
                                        onClose();
                                    }}
                                    className="btn btn-error"
                                >
                                    {options.confirmLabel || 'Xác nhận'}
                                </button>
                                <button className="z-30 btn btn-active" onClick={onClose}>
                                    {options.cancelLabel || 'Hủy'}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            );
        },
    });
};

export default confirm;
