import { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Tooltip,
  Legend,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import { fetchGastos } from "../services/gastosService";

const COLORS = ["#22c55e", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"];

function agregaPorCategoria(gastos) {
  const map = {};
  for (const g of gastos) {
    const cat = g.categoria || "Sem categoria";
    map[cat] = (map[cat] || 0) + (g.valor || 0);
  }
  return Object.entries(map).map(([name, value]) => ({ name, value: parseFloat(value.toFixed(2)) }));
}

function agregaPorMes(gastos) {
  const map = {};
  for (const g of gastos) {
    if (!g.data) continue;
    const mes = g.data.substring(0, 7); // "YYYY-MM"
    map[mes] = (map[mes] || 0) + (g.valor || 0);
  }
  return Object.entries(map)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([mes, total]) => ({ mes, total: parseFloat(total.toFixed(2)) }));
}

function agregaPorFuncionario(gastos) {
  const map = {};
  for (const g of gastos) {
    const nome = g.funcionario_nome || `Funcionário ${g.funcionario_id}`;
    map[nome] = (map[nome] || 0) + (g.valor || 0);
  }
  return Object.entries(map)
    .sort(([, a], [, b]) => b - a)
    .map(([nome, total]) => ({ nome, total: parseFloat(total.toFixed(2)) }));
}

export default function DashboardPage() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchGastos()
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-gray-500">Carregando dashboard...</div>;
  if (error) return <div className="p-8 text-red-500">Erro: {error}</div>;

  const porCategoria = agregaPorCategoria(data);
  const porMes = agregaPorMes(data);
  const porFuncionario = agregaPorFuncionario(data);

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <h2 className="text-2xl font-bold text-gray-800 mb-8">Dashboard de Gastos</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Pizza — por categoria */}
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Gastos por Categoria</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={porCategoria}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {porCategoria.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => `R$ ${v.toFixed(2)}`} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Colunas — por mês */}
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Gastos por Mês</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={porMes}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="mes" />
              <YAxis tickFormatter={(v) => `R$${v}`} />
              <Tooltip formatter={(v) => `R$ ${v.toFixed(2)}`} />
              <Bar dataKey="total" fill="#22c55e" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Horizontal — ranking funcionários */}
        <div className="bg-white rounded-xl shadow p-6 lg:col-span-2">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Ranking de Gastos por Funcionário</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={porFuncionario} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" tickFormatter={(v) => `R$${v}`} />
              <YAxis type="category" dataKey="nome" width={120} />
              <Tooltip formatter={(v) => `R$ ${v.toFixed(2)}`} />
              <Bar dataKey="total" fill="#3b82f6" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
