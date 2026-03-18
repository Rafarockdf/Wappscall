const formatValor = (valor) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(valor);

const formatData = (data) => {
  if (!data) return "-";
  return new Intl.DateTimeFormat("pt-BR").format(new Date(data));
};

function StatusBadge({ aprovado, extornado }) {
  if (extornado)
    return <span className="px-2 py-1 text-xs font-semibold rounded-full bg-red-100 text-red-700">Extornado</span>;
  if (aprovado)
    return <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-700">Aprovado</span>;
  return <span className="px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-700">Pendente</span>;
}

function GastosTable({ gastos }) {
  return (
    <div className="overflow-x-auto rounded-lg shadow">
      <table className="min-w-full bg-white text-sm text-gray-700">
        <thead className="bg-gray-50 text-xs text-gray-500 uppercase tracking-wider">
          <tr>
            {["ID", "Motivo", "Descrição", "Valor", "Data", "Empresa", "Categoria", "Tipo de Gasto", "Status"].map((col) => (
              <th key={col} className="px-4 py-3 text-left">{col}</th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {gastos.map((gasto) => (
            <tr key={gasto.id} className="hover:bg-gray-50 transition-colors">
              <td className="px-4 py-3">{gasto.id}</td>
              <td className="px-4 py-3">{gasto.motivo ?? "-"}</td>
              <td className="px-4 py-3 max-w-xs truncate" title={gasto.descricao}>{gasto.descricao ?? "-"}</td>
              <td className="px-4 py-3 font-medium">{gasto.valor != null ? formatValor(gasto.valor) : "-"}</td>
              <td className="px-4 py-3">{formatData(gasto.data)}</td>
              <td className="px-4 py-3">{gasto.empresa ?? "-"}</td>
              <td className="px-4 py-3">{gasto.categoria ?? "-"}</td>
              <td className="px-4 py-3">{gasto.tipo_gasto ?? "-"}</td>
              <td className="px-4 py-3">
                <StatusBadge aprovado={gasto.boolean_aprovado} extornado={gasto.boolean_extornado} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default GastosTable;
