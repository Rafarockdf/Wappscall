import { useState, useEffect } from "react";
import GastosTable from "../components/GastosTable/GastosTable";
import { fetchGastos, atualizarStatusGasto } from "../services/gastosService";

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

  const handleStatusChange = async (gastoId, novoStatus) => {
    await atualizarStatusGasto(gastoId, novoStatus);

    // Atualizar o gasto na lista local
    setGastos(prevGastos =>
      prevGastos.map(gasto =>
        gasto.id === gastoId
          ? {
              ...gasto,
              boolean_aprovado: novoStatus === 'Aprovado',
              boolean_extornado: novoStatus === 'Extornado'
            }
          : gasto
      )
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Gastos Corporativos</h1>

      {loading && (
        <div className="flex items-center gap-2 text-gray-500">
          <div className="w-5 h-5 border-2 border-gray-300 border-t-green-500 rounded-full animate-spin" />
          Carregando gastos...
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-300 text-red-700 rounded-lg p-4">
          <strong>Erro ao carregar os gastos: </strong>{error.message}
        </div>
      )}

      {!loading && !error && <GastosTable gastos={gastos} onStatusChange={handleStatusChange} />}
    </div>
  );
}

export default GastosPage;
