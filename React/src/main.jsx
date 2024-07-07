import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import Busqueda from './Busqueda.jsx'
import Productos from './Productos.jsx'
import './index.css'
import { useState } from 'react'

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";	


function Main() {
  const [producto, setProducto] = useState(null);

  const handleProductoSeleccionado = (productoSeleccionado) => {
    setProducto(productoSeleccionado);
  };

  return (
    <React.StrictMode>
      <Busqueda onProductoSeleccionado={handleProductoSeleccionado} />
      <Productos producto={producto} />
    </React.StrictMode>
  );
}
ReactDOM.createRoot(document.getElementById('root')).render(<Main />)
