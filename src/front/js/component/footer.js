import React from "react";
import { Link } from "react-router-dom"; // Asegúrate de importar Link

export const Footer = () => (
    <footer className="footer mt-auto py-1 text-center bg-dark">
        <Link to="/dashboard" className="text-decoration-none">
            <h4 className="mb-0 mt-2 text-naranja">
                <i className="fa-solid fa-spider"></i> Halloween
            </h4>
        </Link>
        <p className="mt-2">
            <a
                href="https://github.com/NataliaIacono"
                className="text-decoration-none text-naranja small d-block"
            >
                Made by Natalia Iacono
            </a>
        </p>
    </footer>
);
