programa {
  funcao inicio() {
    real idade
    escreva("Vamos verificar qual classificação indicativa é recomendada para você de acordo com sua idade! \n")
    escreva("Informe sua idade: \n")
    leia(idade)
    escreva("Você escreveu ", idade,"! \n")
    

    se(idade < 10){
      escreva("Você é uma criança, veja programas com a classificação (L)! \n")
    }
    senao se((idade >= 10)e(idade < 12)){
      escreva("Você ainda é uma criança, veja programas com a classificação (10)! \n")
    }
    senao se((idade >= 12)e(idade < 14)){
      escreva("Você ainda é uma criança, veja programas com a classificação (12)! \n")
    }
    senao se((idade >= 14)e(idade < 16)){
      escreva("Você ainda é uma criança, veja programas com a classificação (14)! \n")
    }
    senao se((idade >= 16)e(idade < 18)){
      escreva("Você ainda é uma criança, veja programas com a classificação (16)! \n")
    }
    senao se(idade > 18){
      escreva("Escolha programas de sua preferencia! \n")
    }

  }
}
