programa {
  funcao inicio() {
    inteiro matriz1[2][2], matriz2[2][2], matriz3[2][2]

    para(inteiro i = 0; i < 2; i++){
      para(inteiro j = 0; j < 2; j++){
        escreva("Digite um valor : \n")
        leia(matriz1[i][j])
      }
    }
    
    escreva("Vamos preencher a segunda matriz!\n")

    para(inteiro i = 0; i < 2; i++){
      para(inteiro j = 0; j < 2; j++){
        escreva("Digite um valor : \n")
        leia(matriz2[i][j])
      }
    }
    escreva("A Matriz 1 ficou da seguinte forma : \n[", matriz1[0][0], "][", matriz1[0][1],"] \n", "[", matriz1[1][0], "][", matriz1[1][1],"] \n")
    escreva("A Matriz 2 ficou da seguinte forma : \n[", matriz2[0][0], "][", matriz2[0][1],"] \n", "[", matriz2[1][0], "][", matriz2[1][1],"] \n")

    para(inteiro i = 0; i < 2; i++){
      para(inteiro j = 0; j < 2; j++){
        matriz3[i][j] = matriz1[i][j] + matriz2[i][j]
      }
    }

    escreva("A soma das Matrizes ficou da seguinte forma : \n[", matriz3[0][0], "][", matriz3[0][1],"] \n", "[", matriz3[1][0], "][", matriz3[1][1],"] \n")
  }
}
