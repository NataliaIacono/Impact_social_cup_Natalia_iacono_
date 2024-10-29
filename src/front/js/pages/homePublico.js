import React, { useEffect, useContext } from 'react';
import { Context } from '../store/appContext';
import { CardEquipo } from '../component/cardEquipo';

export const HomePublico = () => {
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
            
        </div>
    );
};
