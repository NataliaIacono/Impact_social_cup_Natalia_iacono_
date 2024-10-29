import React, { useState, useContext } from "react";
import { Context } from "../store/appContext";
import { useNavigate } from 'react-router-dom';
import { ModalRegistro } from '../component/modalRegistro';
import { ForgottenPassword } from "./modalForgottenPassword";
import '../../styles/modal.css';

export const ModalSesion = ({ show, onClose }) => {
    const { actions } = useContext(Context);
    const showHideClassName = show ? "modal display-block" : "modal display-none";
    const [emailValor, setEmailValor] = useState('');
    const [passValor, setPassValor] = useState('');
    const navigate = useNavigate();
    const [showRegistro, setShowRegistro] = useState(false);
    const [showForgottenPassword, setShowForgottenPassword] = useState(false);



    const login = async (e) => {
        e.preventDefault();
        const data = { email: emailValor, contraseña: passValor };
        const userLogin = await actions.login(data);
        
        if (userLogin) {
            onClose(); // Cierra el modal de sesión
            navigate('/home'); // Redirige al Home
        } else {
            alert('Incorrect username or password');
        }
    };

    const handleClickHere = () => {
        onClose(); // Cierra el modal de sesión
        setShowRegistro(true); // Abre el modal de registro
    };

    const handleEmail = () => {
        onClose();
        setShowForgottenPassword(true);

    }

    return (
        <>
            <div className={showHideClassName + " modal-overlay"}>
                <section className="modal-main">
                    <button className="close-button" onClick={onClose}>&times;</button>
                    <p>Iniciar sesión</p>
                    <form onSubmit={login}>
                        <label>Email</label>
                        <input
                            type="text"
                            className="login-field"
                            placeholder="Write your email"
                            required
                            value={emailValor}
                            onChange={(e) => setEmailValor(e.target.value)}
                        />
                        <label>Contraseña</label>
                        <input
                            type="password"
                            className="login-field"
                            placeholder="Write your password"
                            required
                            value={passValor}
                            onChange={(e) => setPassValor(e.target.value)}
                        />
                        <button type="button" className="botonClickHere" onClick={handleEmail}>Has olvidado tu coontraseña?</button>
                        <br></br>
                        <br></br>
                        <br></br>
                        <h6>Si no estás registrado,
                            <button type="button" className="botonClickHere" onClick={handleClickHere}>click aquí</button>
                        </h6>
                        <button className="btn-modal" type="submit" style={{padding: "5px" , borderRadius: "20px"}}> Login </button>
                    </form>
                </section>
            </div>
            {/* Renderiza el ModalRegistro si showRegistro es true */}
            {showRegistro && (
                <ModalRegistro show={showRegistro} onClose={() => setShowRegistro(false)} />
            )}
            {/* Renderiza el ForgottenPassword si showForgottenPassword es true */}
            {showForgottenPassword && (
                <ForgottenPassword show={showForgottenPassword} onClose={() => setShowForgottenPassword(false)} />
            )}

        </>
    );
};