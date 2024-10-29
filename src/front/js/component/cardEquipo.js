import React from "react";
import '../../styles/global.css';

export const CardEquipo = ({ rol, nombre, email }) => {
    return (
        <div>
            <div className="card text-bg-dark mb-3 p-3 me-3" style={{ maxWidth: "15rem" }}>
                <div className="card-header">
                    <i className="fa-solid fa-circle text-naranja"></i>
                    <span className="text-naranja ms-2">{rol}</span>
                </div>
                <div className="card-body">
                    <h5 className="card-title text-naranja">{nombre}</h5>
                    <h6 className="card-text">{email}</h6>
                </div>
            </div>
        </div>
    );
};
