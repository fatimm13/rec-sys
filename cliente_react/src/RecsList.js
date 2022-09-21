import RecsShow from "./RecsShow";
import useFetch from "./useFetch";
import { Row, Spinner } from "react-bootstrap";


const RecsList = (datos) => {
  const{url} = datos
  const { error, isPending, data: viajes } = useFetch(url)

  return (
    <div className="home">
      { error && <div>{ error }</div> }
      { isPending && <div>LOADING <Spinner animation="grow" size="sm" /><Spinner animation="grow" size="sm" /><Spinner animation="grow" size="sm" /></div>  }
      { viajes && 
        <Row> 
            <br/>
            <h1>Resultados de búsqueda:</h1>
            <br/>
            {viajes.length === 0 && <p>No se han encontrado resultados.</p>}
            <RecsShow viajes={viajes} /> 
        </Row>
        }
      
    </div>
  );
}
 
export default RecsList;