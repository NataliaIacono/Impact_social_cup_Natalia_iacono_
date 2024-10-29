const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			demo: [
				{
					title: "FIRST",
					background: "white",
					initial: "white"
				},
				{
					title: "SECOND",
					background: "white",
					initial: "white"
				}
			],
			usuarios: []
		},
		actions: {
			// Use getActions to call a function within a fuction
			exampleFunction: () => {
				getActions().changeColor(0, "green");
			},

			getMessage: async () => {
				try {
					// fetching data from the backend
					const resp = await fetch(process.env.BACKEND_URL + "/api/hello")
					const data = await resp.json()
					setStore({ message: data.message })
					// don't forget to return something, that is how the async resolves
					return data;
				} catch (error) {
					console.log("Error loading message from backend", error)
				}
			},
			changeColor: (index, color) => {
				//get the store
				const store = getStore();

				//we have to loop the entire demo array to look for the respective index
				//and change its color
				const demo = store.demo.map((elm, i) => {
					if (i === index) elm.background = color;
					return elm;
				});

				//reset the global store
				setStore({ demo: demo });
			},


			signUp: async (nombre, email, contraseña, rol) => {
				try {
					const response = await fetch(process.env.BACKEND_URL + "/api/signUp", {
						             
						method: "POST", // Método de la solicitud
						headers: {
							"Content-Type": "application/json", // Indica que el cuerpo de la solicitud es JSON
						},
						body: JSON.stringify({
							nombre: nombre,         // Nombre del usuario
							email: email,          // Email del usuario
							contraseña: contraseña, // Contraseña del usuario
							rol: rol               // Rol del usuario (por ejemplo, 'colaborador')
						}),
					});
			
					// Verificamos si la respuesta no fue exitosa
					if (!response.ok) {
						const errorText = await response.json(); // Obtiene el texto de error en formato JSON
						throw new Error(`Error en la solicitud de registro: ${errorText.msg}`);
					}
			
					const data = await response.json(); // Procesa la respuesta en formato JSON
					console.log('Registro exitoso:', data); // Manejo del registro exitoso
					return data; // Devuelve los datos del usuario registrado
				} catch (error) {
					console.error("Error en la solicitud de registro:", error);
					throw error; // Re-lanza el error para manejo posterior
				}
			},
			


			login: async (dataUser) => {
				try {
					const response = await fetch(process.env.BACKEND_URL + "/api/login", {
						method: "POST",
						body: JSON.stringify(dataUser),
						headers: {
							"Content-Type": "application/json"
						}
					});
			
					const data = await response.json();
					console.log("Respuesta del servidor:", data);
			
					if (response.status !== 200) {
						return false; // Manejo de errores si la respuesta no es exitosa
					} else {
						localStorage.setItem("token", data.token);
						localStorage.setItem("user_id", data.user_id);
						localStorage.setItem("user_nombre", data.nombre);
						localStorage.setItem("user_email", dataUser.email);
			
						return true; // Login exitoso
					}
				} catch (error) {
					console.error("Error en el login:", error); // Captura y muestra cualquier error
					return false; // Devuelve false en caso de error
				}
			},
			

			




			Usuarios: async () => {
				const token = localStorage.getItem('token');
				try {
					const response = await fetch(process.env.BACKEND_URL + '/api/usuarios', {
						             
						method: 'GET',
						headers: {
							'Content-Type': 'application/json',
							'Authorization': `Bearer ${token}`
						}
					});
			
					if (!response.ok) {
						// Si la respuesta no es ok, registra el estado y el texto completo de la respuesta
						const errorText = await response.text();
						console.error('Error en la respuesta del servidor:', response.status, errorText);
						throw new Error('Error en la respuesta del servidor');
					}
			
					const data = await response.json();
					setStore({ usuarios: data });
				} catch (error) {
					console.error("Error al obtener los usuarios:", error);
				}
			}
	
			

		}
	};
};

export default getState;
