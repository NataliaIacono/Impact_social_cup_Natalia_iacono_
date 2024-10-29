import React from "react";
import '../../styles/global.css';

export const CardEquipo = ({ rol, nombre, email }) => {
    return (
        <div>
            <div className="card text-bg-dark mb-3 p-3" style={{ maxWidth: "18rem" }}>
                <div className="card-header">
                    <i className="fa-solid fa-circle text-naranja"></i>
                    <span className="text-naranja ms-2">{rol}</span>
                </div>
                <div className="card-body">
                    <h5 className="card-title text-naranja">{nombre}</h5>
                    <p className="card-text">{email}</p>
                </div>
            </div>
        </div>
    );
};
