import { useState } from "react";
import { cadastraUser } from "../services/userService";

export default function RegistrarFuncionarioPage() {
  const [form, setForm] = useState({nome: "", cargo: "", salario: "", data_contratacao: "" ,telefone: ""});
  const [resultado, setResultado] = useState(null);
  const [erro, setErro] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErro("");
    setResultado(null);
    setLoading(true);
    try {
      const data = await cadastraUser(form);
      setResultado(data);
    } catch (err) {
      setErro(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white rounded-xl shadow-md p-8 w-full max-w-md">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Registrar Funcionário</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-600 mb-1">Nome</label>
            <input
              type="text"
              name="nome"
              value={form.nome}
              onChange={handleChange}
              required
              placeholder="Ex: João Silva"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
            />
          </div>
          
          <div>
            <label className="block text-sm text-gray-600 mb-1">Cargo</label>
            <input
              type="text"
              name="cargo"
              value={form.cargo}
              onChange={handleChange}
              required
              placeholder="Ex: Analista de TI"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
            />
          </div>

          <div>
            <label className="block text-sm text-gray-600 mb-1">Salário</label>
            <input
              type="number"
              name="salario"
              value={form.salario}
              onChange={handleChange}
              required
              placeholder="Ex: 3500.00"
              min="0"
              step="0.01"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
            />
          </div>

          <div>
            <label className="block text-sm text-gray-600 mb-1">Telefone</label>
            <input
              type="text"
              name="telefone"
              value={form.telefone}
              onChange={handleChange}
              required
              placeholder="Ex: (11) 99999-9999"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
            />
          </div>


          <div>
            <label className="block text-sm text-gray-600 mb-1">Data de Contratação</label>
            <input
              type="text"
              name="data_contratacao"
              value={form.data_contratacao}
              onChange={handleChange}
              required
              placeholder="Ex: 2023-01-01"
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
            />
          </div>

          {erro && <p className="text-red-500 text-sm">{erro}</p>}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-green-500 hover:bg-green-600 disabled:opacity-50 text-white font-semibold py-2 rounded-lg transition-colors"
          >
            {loading ? "Registrando..." : "Registrar Funcionário"}
          </button>
        </form>

        {resultado && (
          <div className="mt-6 bg-gray-50 border border-gray-200 rounded-lg p-4">
            <h4 className="text-sm font-semibold text-gray-700 mb-2">Resposta da API</h4>
            <pre className="text-xs text-gray-800 whitespace-pre-wrap break-all">
              {JSON.stringify(resultado, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
