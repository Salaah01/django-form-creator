import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, compose, combineReducers } from "redux"
import './index.css';
import reportWebVitals from './reportWebVitals';
import App from './App';
import formSetupReducer from './store/reducers/formSetup';



declare global {
  interface Window {
    __REDUX_DEVTOOLS_EXTENSION_COMPOSE__?: typeof compose;
    __REDUX_DEVTOOLS_EXTENSION__?: typeof compose;
  }
}

const composeEnhancer =
  process.env.NODE_ENV === "development"
    ? window.__REDUX_DEVTOOLS_EXTENSION__ &&
    window.__REDUX_DEVTOOLS_EXTENSION__()
    : null || compose;


const rootReducer = combineReducers({
  formSetup: formSetupReducer
});

const store = createStore(rootReducer, composeEnhancer);

const app = <Provider store={store}><App /></Provider>;


ReactDOM.render(app, document.getElementById('root'));


// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
