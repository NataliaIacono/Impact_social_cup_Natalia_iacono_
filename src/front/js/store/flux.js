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



			// En tu archivo actions.js o donde tengas tus acciones
			Usuarios: async () => {
				const token = localStorage.getItem('token');
				const backendUrl = process.env.REACT_APP_BACKEND_URL;

				try {
					const response = await fetch(`${backendUrl}/usuarios`, {
						method: 'GET',
						headers: {
							'Content-Type': 'application/json',
							'Authorization': `Bearer ${token}`
						}
					});

					if (!response.ok) {
						throw new Error('Error en la respuesta del servidor');
					}

					const data = await response.json();
					setStore({ usuarios: data }); // Guarda los datos en el store
				} catch (error) {
					console.error("Error al obtener los usuarios:", error);
					// Opcional: podrías guardar el error en el store también
				}
			}



		}
	};
};

export default getState;
