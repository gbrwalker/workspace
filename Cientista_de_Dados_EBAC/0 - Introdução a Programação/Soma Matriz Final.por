programa {
	funcao inicio() {
		inteiro matriz1[2][2], matriz2[2][2], matrizSoma[2][2], valor1, valor2 
		
		
		/*PREENCHE A MATRIZ1*/
		escreva("Digite os valores para a primeira matriz: \n")
		para(inteiro i = 0; i < 2; i++){
		    para(inteiro j = 0; j < 2; j++){
		        escreva("Digite o valor: \n")
		        leia(valor1)
		        matriz1[i][j] = valor1
		    }
		}
		/*IMPRIME A MATRIZ1*/
		para(inteiro i = 0; i < 2; i++){
		    para(inteiro j = 0; j < 2; j++){
		        escreva(" ", matriz1[i][j], " ")
		    }
		    escreva("\n")
		}
		
		escreva("\n\n")
		
		/*PREENCHE A MATRIZ2*/
		escreva("Digite os valores para a segunda matriz: \n")
		para(inteiro i = 0; i < 2; i++){
		    para(inteiro j = 0; j < 2; j++){
		        escreva("Digite o valor: \n")
		        leia(valor2)
		        matriz2[i][j] = valor2
		    }
		}
		/*IMPRIME A MATRIZ2*/
		para(inteiro i = 0; i < 2; i++){
		    para(inteiro j = 0; j < 2; j++){
		        escreva(" ", matriz2[i][j], " ")
		    }
		    escreva("\n")
		}
		
		escreva("\n\n")
		
		
		/*PREENCHE A MATRIZ SOMA*/
		para(inteiro i = 0; i < 2; i++){
		    para(inteiro j = 0; j < 2; j++){
		        matrizSoma[i][j] = matriz1[i][j] + matriz2[i][j]
		    }
		}
		escreva("\n\nA matriz soma é: \n\n")
		/*IMPRIME A MATRIZ SOMA*/
		para(inteiro i = 0; i < 2; i++){
		    para(inteiro j = 0; j < 2; j++){
		        escreva(" ", matrizSoma[i][j], " ")
		    }
		    escreva("\n")
		}
		
	}
}
