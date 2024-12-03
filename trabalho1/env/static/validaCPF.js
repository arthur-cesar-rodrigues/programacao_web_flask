class ValidaCPF {
    constructor(cpfEnviado) {
        Object.defineProperty(this, "cpfLimpo", {
            writable: false,
            enumerable: false,
            configurable: false,
            value: cpfEnviado.replace(/\D+/g, "")
        });
    }

    eSequencia() {
        return this.cpfLimpo.charAt(0).repeat(this.cpfLimpo.length) === this.cpfLimpo;
        //charAt = este método retorna o valor de uma posição(dentro do parenteses) de uma string
    }

    geraNovoCpf() {
        const cpfSemDigitos = this.cpfLimpo.slice(0, -2);
        // const digito1 = this.geraDigito(cpfSemDigitos);
        // const digito2 = this.geraDigito(cpfSemDigitos + digito1)

        const digito1 = ValidaCPF.geraDigito(cpfSemDigitos);
        const digito2 = ValidaCPF.geraDigito(cpfSemDigitos + digito1)
        
        this.novoCpf = cpfSemDigitos + digito1 + digito2;
    }

    static geraDigito(cpfSemDigitos) {
        let total = 0;
        let reverso = cpfSemDigitos.length + 1;
        
        for(let stringNumerica of cpfSemDigitos) {
            total += reverso * Number(stringNumerica);
            reverso--;
        }
        
        const digito = 11 - (total % 11);

        return digito <= 9 ? String(digito) : "0";
    }


    valida() {
        if(!this.cpfLimpo) return false;
        if(typeof this.cpfLimpo !== "string") return false;
        if(this.cpfLimpo.length !== 11) return false;
        if(this.eSequencia()) return false;

        this.geraNovoCpf()

        return this.novoCpf === this.cpfLimpo;
    }
}

function validadorCPF() {
    const validacpf = new ValidaCPF(document.querySelector('input[name = "cpf"]').value);
    
    if(!validacpf.valida()) {
        alert("CPF inválido, por favor digite um CPF válido.");
        return false
    }
    return true;
}