export async function fetchGastos() {
  const response = await fetch("/gastos");
  if (!response.ok) throw new Error(`Erro ${response.status}`);
  return response.json();
}

export async function atualizarStatusGasto(gastoId, status) {
  const response = await fetch(`/gastos/${gastoId}/status`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ status }),
  });

  if (!response.ok) throw new Error(`Erro ${response.status}`);
  return response.json();
}
