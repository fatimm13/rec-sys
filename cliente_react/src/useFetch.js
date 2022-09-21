import { useState, useEffect } from "react";

const useFetch = (url) => {
    const [data, setData] = useState(null);
    const [isPending, setIsPending] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const abortCont = new AbortController();

        fetch(url, { signal: abortCont.signal })
        .then(res => {
            if (!res.ok) { // error del servidor
                throw Error("No se ha podido realizar el fetch de los datos. Error con el servidor");
            }
            return res.json();
        })
        .then(data => {
            setIsPending(false);
            setData(data);
            setError(null);
        })
        .catch(err => {
            if (err.name === "AbortError") {
                console.log("fetch aborted")
            } else {
                // Error de la conexion
                setIsPending(false);
                setError("No se ha podido realizar el fetch de los datos. Error con el servidor.");
                console.log(err.message);
            }
        })

        // abort fetch
        return () => abortCont.abort();

    }, [url])

    return { data, isPending, error };
}
 
export default useFetch;