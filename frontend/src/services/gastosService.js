export async function fetchGastos() {
  const response = await fetch("/gastos");
  if (!response.ok) throw new Error(`Erro ${response.status}`);
  return response.json();
}
