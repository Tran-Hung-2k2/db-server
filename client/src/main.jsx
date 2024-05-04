import React from 'react';
import { Provider } from 'react-redux';
import ReactDOM from 'react-dom/client';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { BrowserRouter as Router } from 'react-router-dom';

import './index.css';
import App from './App';
import store from '@redux/store';

ReactDOM.createRoot(document.getElementById('root')).render(
    <Router>
        <Provider store={store}>
            <App />
            <ToastContainer style={{ zIndex: 10000000 }} position="top-right" />
        </Provider>
    </Router>,
);
