import React from "react";
import { Link } from "react-router-dom";
import '../../styles/global.css';


export const NavbarPrivado = () => {
    return (
        <div>
            <nav className="navbar rounded-top bg-dark">
                <div className="container">
                    <Link to="/dashboard" className="text-decoration-none">
                        <h4 className="mb-0 text-naranja"><i class="fa-solid fa-spider"></i> Halloween</h4>
                    </Link>
                    <div className="ml-auto">
                        <Link to="/demo">
                            <button className="btn btn-naranja me-3">Mi cuenta</button>
                        </Link>
                    </div>
                </div>

            </nav>
            <div className="navbar-segunda bg-naranja text-center">
                <p className="mb-0 text-white">DASHBOARD</p>
            </div>
        </div>

    );
};
