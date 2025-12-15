programa {
	funcao inicio() {
	    real hip, catB, catC
		
		escreva("Vamos verificar se o triângulo é um triângulo retângulo?\n")
		escreva("Digite o maior valor: \n")
		leia(hip)
		
		escreva("Digite o maior valor do próximo lado: \n")
		leia(catB)
		
		escreva("Digite o maior valor do último lado: \n")
		leia(catC)
		
		se(quadrado(hip) == (quadrado(catB))+(quadrado(catC))){
		    escreva("É um triângulo retângulo!\n")
		}
		senao{
		    escreva("Não é um triângulo retângulo!\n")
		}
		
	}
	
	funcao real quadrado(real valor){
	    real quad
	    quad = valor*valor
	    retorne quad
	}
}
