import "./GastosTable.css";

const formatValor = (valor) =>
  new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(valor);

const formatData = (data) => {
  if (!data) return "-";
  return new Intl.DateTimeFormat("pt-BR").format(new Date(data));
};

function StatusBadge({ aprovado, extornado }) {
  if (extornado) return <span className="status-badge status-extornado">Extornado</span>;
  if (aprovado) return <span className="status-badge status-aprovado">Aprovado</span>;
  return <span className="status-badge status-pendente">Pendente</span>;
}

function GastosTable({ gastos }) {
  return (
    <div className="gastos-table-wrapper">
      <table className="gastos-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Motivo</th>
            <th>Descrição</th>
            <th>Valor</th>
            <th>Data</th>
            <th>Empresa</th>
            <th>Categoria</th>
            <th>Tipo de Gasto</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {gastos.map((gasto) => (
            <tr key={gasto.id}>
              <td>{gasto.id}</td>
              <td>{gasto.motivo ?? "-"}</td>
              <td className="col-descricao" title={gasto.descricao}>{gasto.descricao ?? "-"}</td>
              <td className="col-valor">{gasto.valor != null ? formatValor(gasto.valor) : "-"}</td>
              <td>{formatData(gasto.data)}</td>
              <td>{gasto.empresa ?? "-"}</td>
              <td>{gasto.categoria ?? "-"}</td>
              <td>{gasto.tipo_gasto ?? "-"}</td>
              <td>
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
