import React from "react";
import { Link } from "react-router-dom";
import '../../styles/global.css';

export const NavbarPrivado = () => {
    return (
        <div>
            <nav className="navbar bg-dark">
                <div className="container d-flex justify-content-between">
                    {/* Contenedor de Enlaces de la Izquierda */}
                    <div className="d-flex align-items-center gap-3">
                        <Link to="/dashboard" className="text-decoration-none">
                            <h4 className="mb-0 text-naranja"><i className="fa-solid fa-spider"></i> Halloween</h4>
                        </Link>
                        <Link to="/dashboard" className="text-decoration-none">
                            <p className="mb-0 text-white">DASHBOARD</p>
                        </Link>
                        <Link to="/colaboradores" className="text-decoration-none">
                            <p className="mb-0 text-white">EQUIPO</p>
                        </Link>
                    </div>

                    {/* Botón de la Derecha */}
                    <div>
                        <Link to="/demo">
                            <button className="btn btn-naranja me-3">Mi cuenta</button>
                        </Link>
                    </div>
                </div>
            </nav>
        </div>
    );
};
