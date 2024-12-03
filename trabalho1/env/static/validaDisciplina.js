function validaDisciplina() {
    // Verifica se pelo menos um checkbox foi selecionado
    const checkboxes = document.querySelectorAll('input[name="disciplinas"]:checked');
    if (checkboxes.length === 0) {
        alert("Por favor, selecione pelo menos uma disciplina.");
        return false; // Cancela o envio do formulário
    }
    return true;
}