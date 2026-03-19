import { useState } from 'react';

const formatValor = (valor) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(valor);

const formatData = (data) => {
  if (!data) return "-";
  return new Intl.DateTimeFormat("pt-BR").format(new Date(data));
};

function StatusDropdown({ gasto, onStatusChange }) {
  const [isLoading, setIsLoading] = useState(false);

  const getStatusText = () => {
    if (gasto.boolean_extornado) return 'Extornado';
    if (gasto.boolean_aprovado) return 'Aprovado';
    return 'Pendente';
  };

  const getStatusClass = () => {
    if (gasto.boolean_extornado) return 'bg-red-100 text-red-700';
    if (gasto.boolean_aprovado) return 'bg-green-100 text-green-700';
    return 'bg-yellow-100 text-yellow-700';
  };

  const handleStatusChange = async (newStatus) => {
    if (isLoading) return;

    setIsLoading(true);
    try {
      await onStatusChange(gasto.id, newStatus);
    } catch (error) {
      console.error('Erro ao alterar status:', error);
      alert('Erro ao alterar status do gasto');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <select
      value={getStatusText()}
      onChange={(e) => handleStatusChange(e.target.value)}
      disabled={isLoading}
      className={`px-2 py-1 text-xs font-semibold rounded border-none cursor-pointer disabled:cursor-not-allowed disabled:opacity-50 ${getStatusClass()}`}
    >
      <option value="Pendente">Pendente</option>
      <option value="Aprovado">Aprovado</option>
      <option value="Extornado">Extornado</option>
    </select>
  );
}

function GastosTable({ gastos, onStatusChange }) {
  return (
    <div className="overflow-x-auto rounded-lg shadow">
      <table className="min-w-full bg-white text-sm text-gray-700">
        <thead className="bg-gray-50 text-xs text-gray-500 uppercase tracking-wider">
          <tr>
            {["ID","Funcionário", "Motivo","Valor", "Data", "Razão Social", "CNPJ", "Categoria", "Tipo de Gasto", "Status"].map((col) => (
              <th key={col} className="px-4 py-3 text-left">{col}</th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {gastos.map((gasto) => (
            <tr key={gasto.id} className="hover:bg-gray-50 transition-colors">
              <td className="px-4 py-3">{gasto.id}</td>
              <td className="px-4 py-3">{gasto.funcionario_nome ?? "-"}</td>
              <td className="px-4 py-3">{gasto.motivo ?? "-"}</td>
              <td className="px-4 py-3 font-medium">{gasto.valor != null ? formatValor(gasto.valor) : "-"}</td>
              <td className="px-4 py-3">{formatData(gasto.data)}</td>
              <td className="px-4 py-3">{gasto.razao_social ?? "-"}</td>
              <td className="px-4 py-3">{gasto.cnpj ?? "-"}</td>
              <td className="px-4 py-3">{gasto.categoria ?? "-"}</td>
              <td className="px-4 py-3">{gasto.tipo_gasto ?? "-"}</td>
              <td className="px-4 py-3">
                <StatusDropdown gasto={gasto} onStatusChange={onStatusChange} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default GastosTable;
