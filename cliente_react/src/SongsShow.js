import { Card, Row, Col } from 'react-bootstrap';

const SongsShow = ({ songs }) => {

  return (

    <Row md="auto" className="g-4">
      {songs.map(song => (
        <Col>
          <Card className="bg-light border-dark text-center" style={{ width: '13rem' }}>
            <Card.Img variant="top" src={song.cover} />
            <Card.Body>
              <Card.Title>{ song.title }</Card.Title>
              <Card.Subtitle className="mb-2 text-muted"> { song.artist }</Card.Subtitle>
              <Card.Text className="text-muted">
                <i>{ song.genres.join(", ") } ({ new Date(song.release_date).getFullYear() })</i> <br/>
              </Card.Text>
            </Card.Body>
          </Card>
        </Col>
      ))}
    </Row>
  );
}
 
export default SongsShow;