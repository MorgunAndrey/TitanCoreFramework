import React, { Component } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./Login";
import Register from "./Register";
import ForgotPassword from "./ForgotPassword";
import ResetPassword from "./ResetPassword";


export default class RoutesReact extends Component {
    constructor(props) {
        super(props);
        const csrfMetaTag = document.querySelector('meta[name="csrf-token"]');
        this.state = {
            csrfToken: csrfMetaTag ? csrfMetaTag.getAttribute('content') : ''
        };
    }

    // Функция для обновления CSRF токена в состоянии и в DOM
    updateCsrfToken = (newToken) => {
        this.setState({ csrfToken: newToken });
        
        // Обновляем meta-тег в DOM
        const csrfMetaTag = document.querySelector('meta[name="csrf-token"]');
        if (csrfMetaTag) {
            csrfMetaTag.setAttribute('content', newToken);
        }
    };

    render() {
        return (
            <Router>
                <Routes>
                    <Route 
                        path="/register" 
                        element={
                            <Register 
                                csrfToken={this.state.csrfToken} 
                                setCsrfToken={this.updateCsrfToken} 
                            />
                        } 
                    />
                    <Route 
                        path="/login" 
                        element={
                            <Login 
                                csrfToken={this.state.csrfToken} 
                                setCsrfToken={this.updateCsrfToken} 
                            />
                        } 
                    />
                    <Route 
                        path="/forgot/password" 
                        element={
                            <ForgotPassword 
                              csrfToken={this.state.csrfToken} 
                                setCsrfToken={this.updateCsrfToken} 
                            />
                        }    
                    />
                    <Route 
                        path="/password/reset/:token" 
                        element={
                            <ResetPassword 
                              csrfToken={this.state.csrfToken} 
                                setCsrfToken={this.updateCsrfToken} 
                            />
                        }    
                    />
                </Routes>
            </Router>
        )
    }
}

const container = document.getElementById('main');
const root = createRoot(container);
root.render(<RoutesReact />);