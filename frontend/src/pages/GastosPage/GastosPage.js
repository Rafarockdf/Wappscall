import { useState, useEffect } from "react";
import GastosTable from "../../components/GastosTable/GastosTable";
import { fetchGastos } from "../../services/gastosService";
import "./GastosPage.css";

function GastosPage() {
  const [gastos, setGastos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchGastos()
      .then(setGastos)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="gastos-page">
      <h1>Gastos Corporativos</h1>

      {loading && (
        <div className="gastos-loading">
          <div className="gastos-spinner" />
          Carregando gastos...
        </div>
      )}

      {error && (
        <div className="gastos-error">
          <strong>Erro ao carregar os gastos</strong>
          {error.message}
        </div>
      )}

      {!loading && !error && <GastosTable gastos={gastos} />}
    </div>
  );
}

export default GastosPage;
