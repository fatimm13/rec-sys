import useFetch from './useFetch';
import SongsShow from './SongsShow';
import { Container, Row, Spinner, Tab, Tabs } from "react-bootstrap";
import { useParams } from 'react-router-dom';

const Bienvenida = () => {

    let { userId } = useParams();
    const { error, isPending, data: user } = useFetch(`http://127.0.0.1:5000/usuario/${userId}`);

    return (
        <div className="home">

          { error && <div> <i>{ error }</i></div> }

          { isPending &&
            <div>
              <h3>
              <Spinner animation="grow" size="sm" /><Spinner animation="grow" />
              {' '}Obteniendo los datos y recomendaciones, este proceso puede tardar{' '}
              <Spinner animation="grow" /><Spinner animation="grow" size="sm" />
              </h3>
            </div> }

          { user && 
            <Container fluid>
              <Row>
                <h1>Bienvenido {user.name} de {user.country}</h1>
              </Row>
              <br/>
              <Row>
                <Tabs defaultActiveKey="fav" id="justify-tab-example" className="mb-3" justify>
                  <Tab eventKey="fav" title="Canciones favoritas">
                    <h2>Canciones favoritas:</h2>
                    <br/>
                    {user.songs_fav.length === 0 && <p>No se han encontrado canciones favoritas.</p>}
                    <SongsShow songs={user.songs_fav} /> 
                  </Tab>
                  <Tab eventKey="chart" title="Canciones top Deezer">
                    <h2>Canciones en el top de Deezer:</h2>
                    <br/>
                    {user.songs_chart.length === 0 && <p>No se han encontrado canciones en su top de Deezer.</p>}
                    <SongsShow songs={user.songs_chart} /> 
                  </Tab>
                  <Tab eventKey="recommender" title="Canciones recomendadas">
                    <h2>Canciones recomendadas:</h2>
                    <br/>
                    {user.recommendations.length === 0 && <p>No se han encontrado recomendaciones.</p>}
                    <SongsShow songs={user.recommendations} />
                  </Tab>
                </Tabs>
              </Row>
            </Container>
            }
          
        </div>
      );
    
}
 
export default Bienvenida;