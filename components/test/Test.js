import React, { useState } from 'react';

function Test() {
    let title = "Test component React!";

    return (
        <div className="container-fluid">
            <div className="text-center">
                <br/><br/><br/><br/><br/><br/>
                <h3>{title}</h3>
            </div>
        </div>
    ); 
}

export default Test;