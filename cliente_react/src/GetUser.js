import { Container, Row, Col, Button, Image, InputGroup, FormControl } from 'react-bootstrap';
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

const UserID = () => {

    const [id, setId] = useState("");
    const navigate = useNavigate();

    const limpiarFiltro = ()=>{
        setId("");
    }

    const handleSubmit = ()=>{
        navigate(`/userDetails/${id}`)
    }
    
    return (
        <Container>

            <Row>
                <Col></Col>
                <Col md="auto"><h1>Inicio del Sistema de Recomendación de música</h1></Col>
                <Col></Col>
            </Row>

            <br/>

            <Row>
                <Col></Col>
                <Col md="auto"> <p>
                    Este sistema de recomendación hace uso de la API de Deezer, para obtener el ID de usuario, 
                    inicie sesión en la <a href="https://www.deezer.com/es/" aria-label="Deezer"> web de Deezer</a> y 
                    al ir al perfil, lo obtendrá.
                </p> </Col>
                <Col></Col>
            </Row>
            
            <br/>

            <Row>
                <Col></Col>
                <Col md="auto">
                    <InputGroup className="mb-3">
                        <InputGroup.Text id="basic-addon1">🔎</InputGroup.Text>
                        <FormControl type="number" placeholder="ID de Deezer" aria-label="Recipient's userid" aria-describedby="basic-addon2" value={id} onChange={(e)=>{setId(e.target.value)}} />
                        <Button onClick={handleSubmit} variant="outline-success" id="button-addon2"> Buscar usuario </Button>
                        <Button onClick={limpiarFiltro} variant="outline-danger" id="button-addon2"> Limpiar búsqueda </Button>
                    </InputGroup>
                </Col>
                <Col></Col>
            </Row>

            <br/>
            <br/>

            <Row>
                <Col></Col>
                <Col md="auto">
                    <a href="https://www.deezer.com/es/" aria-label="Deezer">
                        <Image fluid="true" src="deezer_logo.png"/>
                    </a>
                </Col>
                <Col></Col>
            </Row>
            
        </Container>
    );
}
 
export default UserID;