import React, { useState, useContext } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from 'react-router-dom';
import { ModalSesion } from "./modalSesion";
import '../../styles/modal.css';

export const ModalRegistro = ({ show, onClose }) => {
    const { store, actions } = useContext(Context);
    const showHideClassName = show ? "modal display-block" : "modal display-none";

    const [email, setEmail] = useState("");
    const [contraseña, setContraseña] = useState("");
    const [nombre, setNombre] = useState("");
    const [rol, setRol] = useState("");
    const [showModalSesion, setShowModalSesion] = useState(false);

    const navigate = useNavigate();

    const signUp = async (event) => {
        event.preventDefault(); // Previene el comportamiento por defecto del formulario
        const signUpProcess = await actions.signUp(nombre, email, contraseña, rol); // Asegúrate de pasar rol
        if (signUpProcess) {
            alert('Registro exitoso');
            setShowModalSesion(true);
        }
        onClose();
    }

    return (
        <>
            <div className={showHideClassName + " modal-overlay"}>
                <section className="modal-main">
                    <button className="close-button" onClick={onClose}>
                        &times;
                    </button>
                    <p>Regístrate</p>
                    <form onSubmit={signUp}>
                        <label>Nombre</label>
                        <input
                            type="text"
                            className="login-field"
                            placeholder="Escribe tu nombre"
                            required
                            id="signUp-nombre"
                            value={nombre}
                            onChange={(e) => setNombre(e.target.value)}
                        />
                        <label>Rol</label>
                        <input
                            type="text"
                            className="login-field"
                            placeholder="gerente o colaborador"
                            required
                            id="signUp-rol"
                            value={rol}
                            onChange={(e) => setRol(e.target.value)}
                        />
                        <label>Email</label>
                        <input
                            type="email" // Cambié el tipo a 'email' para validación automática
                            className="login-field"
                            placeholder="Escribe tu email"
                            required
                            id="signUp-email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />
                        <label>Contraseña</label>
                        <input
                            type="password"
                            className="login-field"
                            placeholder="Escribe tu contraseña"
                            required
                            id="signUp-pass"
                            value={contraseña}
                            onChange={(e) => setContraseña(e.target.value)}
                        />
                        <button className="btn-modal text-naranja" type="submit" style={{ padding: "5px", borderRadius: "20px" }}>
                            Enviar
                        </button>
                    </form>
                </section>
            </div>
            {showModalSesion && (
                <ModalSesion show={showModalSesion} onClose={() => setShowModalSesion(false)} />
            )}
        </>
    );
};
