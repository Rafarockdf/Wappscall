
async def extract_user_data(message):
    """Extrai informações do usuário com fallback para o primeiro nome."""
    user = message.from_user
    
    # Se o @username não existir, pegamos o First Name. 
    # Se nem o First Name existir (raro), fica "Usuário".
    nome_para_exibir = user.username or user.first_name or "Usuário"
    
    return {
        "id": user.id,
        "username": nome_para_exibir,
        "full_name": f"{user.first_name or ''} {user.last_name or ''}".strip(),
        "text": message.text
    }