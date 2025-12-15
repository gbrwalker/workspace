programa {
  funcao inicio() {
    real nota1, nota2, media

    escreva("Vamos calcular sua média escolar! \n")
    escreva("Digite a sua primeira nota: \n")
    leia(nota1)
    escreva("Digite a sua segunda nota: \n")
    leia(nota2)

    media = ((nota1 + nota2)/2)

    se(media < 5){
      escreva("Você está reprovado sem direito a Recuperação, parabéns ! \n")
    }
    senao se(media >= 5 e media < 8){
      escreva("Você está de Recuperação, parabéns ! \n")
    }
    senao {
      escreva("Você está aprovado, parabéns ! \n")
    }

  }
}
