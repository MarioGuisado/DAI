import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import { useState } from 'react'

const Busqueda = ({ onProductoSeleccionado }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };


  return (
    
    <Navbar expand="lg" className="bg-body-tertiary fixed-top">
      <Container fluid>
        <Navbar.Brand href="#">Tienda</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll">
          <Nav
            className="me-auto my-2 my-lg-0"
            style={{ maxHeight: '100px' }}
            navbarScroll
          >
            <NavDropdown title="Categorías" id="navbarScrollingDropdown">
              <NavDropdown.Item onClick={() => onProductoSeleccionado("men")}>Men's Fashion</NavDropdown.Item>
              <NavDropdown.Item onClick={() => onProductoSeleccionado("women")}>Women's Fashion</NavDropdown.Item>
              <NavDropdown.Item onClick={() => onProductoSeleccionado("electronics")}>Electronics</NavDropdown.Item>
              <NavDropdown.Item onClick={() => onProductoSeleccionado("jewelry")}>Jewelry</NavDropdown.Item>
            </NavDropdown>
          </Nav>

          <Form className="d-flex ms-auto">
            <Form.Control
              type="search"
              placeholder="Search"
              className="me-2"
              aria-label="Search"
              value={searchTerm}
              onChange={handleSearchChange}
            />
            <Button variant="outline-success" onClick={() => onProductoSeleccionado(searchTerm)}>Buscar</Button>
          </Form>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}
export default Busqueda



