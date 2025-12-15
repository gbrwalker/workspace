programa {
  funcao inicio() {
    //Tipo de Operação
    //Dolar para real = 1
    //Real para dolar = 2
    real cotacaoDolar, tipoOperacao, valorEntrada, valorSaida
    cotacaoDolar = 0
    tipoOperacao = 0
    valorEntrada = 0
    valorSaida = 0

    escreva("Bem vindo ao conversor de Moedas! \n")
    escreva("Digite a cotação do Dolar Hoje em Reais:  \n")
    leia(cotacaoDolar)
    escreva("Digite o número da opção que deseja converter:  \n 1 - Dolar para Real \n 2 - Real para Dolar \n ")
    leia(tipoOperacao)
    escreva("Digite o valor a ser convertido: \n ")
    leia(valorEntrada)

    se(tipoOperacao == 1)
    {
      valorSaida = valorEntrada * cotacaoDolar
      escreva("Valor em Reais: \n ", valorSaida)
    }
    se(tipoOperacao == 2)
    {
      valorSaida = valorEntrada / cotacaoDolar
      arredondar(valorSaida)
      escreva("Valor em Dolar: \n ", valorSaida)
    }

    
  }
}
