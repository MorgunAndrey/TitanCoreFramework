import React, { Component } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Test from "./Test";

export default class RoutesReact extends Component {
    render() {
        return (
            <Router>
                <Routes>
                    <Route path="/test" element={ <Test /> } /> 
                </Routes>
            </Router>
        )
    }
}

const container = document.getElementById('main');
const root = createRoot(container);
root.render(<RoutesReact />);