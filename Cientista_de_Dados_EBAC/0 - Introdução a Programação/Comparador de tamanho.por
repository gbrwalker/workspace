programa {
  funcao inicio() {
    real num1, num2, padrao
    num1 = 0
    num2 = 0
    padrao = 25

    escreva("Olá, vamos comparar o tamanho dos objetos: \n")
    escreva("Digite o tamanho do Objeto 1: \n")
    leia(num1)
    escreva("Digite o tamanho do Objeto 2: \n")
    leia(num2)

    se(num1 < padrao){
      escreva("Objeto 1 Menor que o padrão ! \n")
    }
    senao se(num1 > padrao){
      escreva("Objeto 1 Maior que o padrão ! \n")
    }
    se(num2 < padrao){
      escreva("Objeto 2 Menor que o padrão ! \n")
    }
    senao se(num2 > padrao){
      escreva("Objeto 2 Maior que o padrão ! \n")
    }

  }
}
