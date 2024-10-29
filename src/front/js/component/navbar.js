import React, { useState, useContext } from "react";
import { Link } from "react-router-dom";
import '../../styles/global.css';
import { ModalRegistro } from "./modalRegistro";
import { Context } from '../store/appContext';
import { ModalSesion } from "./modalSesion";

export const Navbar = () => {
    const { store, actions } = useContext(Context);
    
    // Estados para los modales
    const [showRegistroModal, setShowRegistroModal] = useState(false);
    const [showSesionModal, setShowSesionModal] = useState(false);
    
    const openRegistroModal = () => {
        setShowRegistroModal(true);
    };

    const closeRegistroModal = () => {
        setShowRegistroModal(false);
    };

    const openSesionModal = () => {
        setShowSesionModal(true);
    };

    const closeSesionModal = () => {
        setShowSesionModal(false);
    };

    return (
        <nav className="navbar bg-dark">
            <div className="container">
                <Link to="/" className="text-decoration-none">
                    <h4 className="mb-0 text-naranja"><i className="fa-solid fa-spider"></i> Halloween</h4>
                </Link>
                <div className="ml-auto d-flex">
                    <div>
                        <button className="btn btn-naranja me-3" onClick={openRegistroModal}>Registrarse</button>
                        <ModalRegistro show={showRegistroModal} onClose={closeRegistroModal} />
                    </div>

                    <div>
                        <button className="btn btn-naranja me-3" onClick={openSesionModal}><i className="fas fa-user"></i>&nbsp; &nbsp;Iniciar sesión</button>
                        <ModalSesion show={showSesionModal} onClose={closeSesionModal} />
                    </div>
                </div>
            </div>
        </nav>
    );
};
