import React, { useEffect } from 'react';
import { useState } from 'react'
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Rating } from 'primereact/rating';

const Productos = ({ producto }) => {
    const [products, setProducts] = useState([]);
    console.log(producto);

    useEffect(() => {
        const fetchData = async () => {
            try {
                if(producto == "men" || producto == "women" || producto == "electronics" || producto == "jewelry" || producto == undefined){
                    const response = await fetch(`http://localhost:8000/etienda/api/productosCategoria/${producto}`);
                    const data = await response.json();
                    setProducts(data);
                    console.log(data);
                }else{
                    const response = await fetch(`http://localhost:8000/etienda/api/productosBusqueda/${producto}`);
                    const data = await response.json();
                    setProducts(data);
                    console.log(data);
                }
            } catch (error) {
                console.error('Error:', error);
            }
        };

        fetchData();
    }, [producto]);

    return (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem' }}>
            {products.map((product) => (
                <Card style={{ width: '18rem' }}>
                    <Card.Img variant="top" src={`../static/${product.image}`} />
                    <Card.Body>
                        <Card.Title>{product.title}</Card.Title>
                        <Card.Text>{product.description} </Card.Text>
                        <Rating value={product.rating.rate} disabled cancel={false} class="text-centered" />
                        <Button variant="primary">Comprar</Button>
                    </Card.Body>
                </Card>
            ))}
        </div>
    );
}
export default Productos