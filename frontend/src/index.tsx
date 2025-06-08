import {Elements} from '@stripe/react-stripe-js';
import React from 'react';
import ReactDOM from 'react-dom';
import './styles/index.scss';
import {configureStripe} from 'src/app/external-apis/configure-stripe';
import App from './app/App';
import reportWebVitals from './reportWebVitals';
import {Router} from 'react-router-dom';
import history from './app/shared/util/history';
import {Provider} from 'react-redux';
import {store} from './app/store';
import {configureBaseApi} from './app/api/common/clients/base-api';
import AuthAutoLogin from 'src/app/shared/context-providers/auth-auto-login';

configureBaseApi();
const stripePromise = configureStripe();

ReactDOM.render(
    <React.StrictMode>
        <Router history={history}>
            <Provider store={store}>
                <AuthAutoLogin>
                    <Elements stripe={stripePromise}>
                        <App/>
                    </Elements>
                </AuthAutoLogin>
            </Provider>
        </Router>
    </React.StrictMode>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
