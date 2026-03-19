import { useState } from "react";
import RegistrarFuncionarioPage from "./pages/RegistrarFuncionarioPage";
import GastosPage from "./pages/GastosPage";
import DashboardPage from "./pages/DashboardPage";

const menuItems = [
  { id: "gastos", label: "Gastos Corporativos" },
  { id: "dashboard", label: "Dashboard" },
  { id: "funcionario", label: "Registrar Funcionário" },
];

function App() {
  const [pagina, setPagina] = useState("gastos");

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <aside className="w-56 bg-gray-800 text-white flex flex-col py-6 px-4 gap-2">
        <h1 className="text-lg font-bold mb-6 text-green-400">WappsCall</h1>
        {menuItems.map((item) => (
          <button
            key={item.id}
            onClick={() => setPagina(item.id)}
            className={`text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
              pagina === item.id
                ? "bg-green-500 text-white"
                : "text-gray-300 hover:bg-gray-700"
            }`}
          >
            {item.label}
          </button>
        ))}
      </aside>

      {/* Conteúdo */}
      <main className="flex-1">
        {pagina === "gastos" && <GastosPage />}
        {pagina === "dashboard" && <DashboardPage />}
        {pagina === "funcionario" && <RegistrarFuncionarioPage />}
      </main>
    </div>
  );
}

export default App;
