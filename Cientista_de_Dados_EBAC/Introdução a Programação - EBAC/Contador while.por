programa {
  funcao inicio() {
    inteiro tamanhoSequencia, par = 0, contador = 1

    escreva("Digite o tamanho da sequencia desejada: \n")
    leia(tamanhoSequencia)

    enquanto(contador <= tamanhoSequencia){
      escreva(par," - ")
      contador = contador + 1
      par = par + 2
    }    
  }
}
