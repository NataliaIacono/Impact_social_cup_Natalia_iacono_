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
