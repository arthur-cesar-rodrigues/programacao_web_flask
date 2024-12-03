function verificaDigitos(digitos) {
    if (digitos[0] !== "(" || digitos[4] !== ")" || digitos[10] !== "-") return false;
    
    return true;
}

function verificaNumeros(numeros) {
    for(i = 0; i < numeros.length; i++) {
        if (i === 0 || i === 4 || i === 10) i++;
        if(isNaN(parseInt(numeros[i]))) return false;
    }
    return true;
}

function validaTelefone() {
    const telefone = document.querySelector('input[name = "telefone"]').value 
    if(!verificaNumeros(telefone) || !verificaDigitos(telefone)) {
        alert("Número inválido, digite um número válido (exemplo: (099)99999-9999)");
        return false;
    } 
    return true
}

