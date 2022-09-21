import { Navbar, Container } from 'react-bootstrap';

const NavbarUp = () => {
    
    return ( 
        <Navbar fixed="top" bg="info" variant="dark">
            <Container fluid>
                <Navbar.Brand href="/">
                    <img alt="" src="logo_bw_128.png" id="logo" width="30" height="30" className="d-inline-block align-top" /> {' '}
                    RecSys
                </Navbar.Brand>
                <Navbar.Toggle aria-controls="navbarScroll" />                
            </Container>
        </Navbar>
    );
}
 
export default NavbarUp;