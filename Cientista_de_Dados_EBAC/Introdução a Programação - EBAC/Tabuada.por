programa {
  funcao inicio() {
    inteiro termo, contador, numTab

    termo = 0
    numTab = 0
    contador = 1

    escreva("Vamos calcular a tabuada ! \n")
    escreva("Digite um numero para calcularmos: \n")
    leia(numTab)
    escreva("O número que você digitou é ", numTab, "! \n")

    enquanto(contador <= 10){
    termo = termo + numTab
    escreva(numTab, " X ", contador, " = ", termo, "\n")
    contador = contador + 1


   }
  }
}
