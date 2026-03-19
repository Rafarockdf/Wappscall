export async function cadastraUser(payload) {
  const formData = new FormData();
  formData.append("nome", payload.nome);
  formData.append("cargo", payload.cargo);
  formData.append("salario", payload.salario);
  formData.append("telefone", payload.telefone);
  formData.append("data_contratacao", payload.data_contratacao);

  const response = await fetch("/cadastra_user", {
    method: "POST",
    body: formData, // sem Content-Type manual
  });
  if (!response.ok) throw new Error(`Erro ${response.status}`);
  return response.json();
}
