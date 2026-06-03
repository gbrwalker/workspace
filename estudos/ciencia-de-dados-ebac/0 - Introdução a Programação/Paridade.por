programa {
  funcao inicio() {
    inteiro num, resto
    num = 0
    resto = 0

    escreva("Vamos descobrir a paridade do numero que você digitar abaixo: \n")
    leia(num)
    
    resto = num % 2

    se(resto != 0){
      escreva(num, " se trata de um número impar.")
    }
    senao{
      escreva(num, " se trata de um número par.")
    }
  }
}
