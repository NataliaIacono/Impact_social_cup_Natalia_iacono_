import React, { useEffect, useContext } from 'react';
import { Context } from '../store/appContext';
import { CardEquipo } from '../component/cardEquipo';

export const Home = () => {
    const { store, actions } = useContext(Context);

    useEffect(() => {
        actions.Usuarios(); // Llama a la acción para obtener usuarios
    }, []);

    return (
        <div 
            style={{
                backgroundImage: `url('https://img.pikbest.com/wp/202345/1080p-hd-halloween-wallpaper-images_9589328.jpg!sw800')`,
                backgroundSize: 'cover', // Asegura que la imagen cubra todo el contenedor
                backgroundPosition: 'center', // Centra la imagen
                minHeight: '100vh', // Asegura que el contenedor tenga una altura mínima
                // display: 'flex', // Usamos flex para centrar contenido
                flexDirection: 'column', // Alinea los elementos en columna
                // justifyContent: 'center', // Centra verticalmente
                // alignItems: 'center', // Centra horizontalmente
                padding: '20px', // Agrega un poco de espacio alrededor del contenido
                // textAlign: 'center', // Alinea el texto al centro
                backdropFilter: 'blur(5px)', // Opcional: agrega un efecto de desenfoque
            }}
        >
            <div className='mt-3 ms-5 me-5'>
            <h1 className='text-naranja'>Equipo</h1>
            <div className="d-flex flex-wrap justify-content-center">
                {store.usuarios.map((usuario) => (
                    <CardEquipo 
                        key={usuario.id} 
                        rol={usuario.rol} 
                        nombre={usuario.nombre} 
                        email={usuario.email} 
                    />
                ))}
            </div>
            </div>
        </div>
    );
};
