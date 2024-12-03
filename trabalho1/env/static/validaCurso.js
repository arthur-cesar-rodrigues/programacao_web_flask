function validaCurso() {
    // Verifica se pelo menos um checkbox foi selecionado
    const checkboxes = document.querySelectorAll('input[name="cursos"]:checked');
    if (checkboxes.length === 0) {
        alert("Por favor, selecione pelo menos um curso.");
        return false; // Cancela o envio do formulário
    }
    return true;
}