import React from "react";
import { Link } from "react-router-dom";
import '../../styles/global.css';


export const Navbar = () => {
	return (
		<nav className="navbar rounded-top bg-dark">
			<div className="container">
				<Link to="/" className="text-decoration-none">
					<h4 className="mb-0 text-naranja"><i class="fa-solid fa-spider"></i> Halloween</h4>
				</Link>
				<div className="ml-auto">
					<Link to="/demo">
						<button className="btn btn-naranja me-3">Registrarse</button>
					</Link>
					<Link to="/demo">
						<button className="btn btn-naranja">Iniciar sesión</button>
					</Link>
				</div>
			</div>
		</nav>
	);
};
