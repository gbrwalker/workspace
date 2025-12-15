programa {
	funcao inicio() {
		inteiro numeroTeste, resto, contaMultiplos = 0
		
		escreva("Olá! Digite um número para sabermos quantos múltiplos ele possui: ")
		leia(numeroTeste)
		
		para(inteiro i = 1; i <= numeroTeste; i++){
		    resto = numeroTeste % i
		    se(resto == 0){
		        contaMultiplos = contaMultiplos + 1
		    }
		}
		
		escreva("O número digitado possui ", contaMultiplos, " múltiplos!")
	}
}
