/*####Jogo da Velha####*/

programa {
	funcao inicio() {
	    /*Parтmetros iniciais do jogo*/
	    /*A variсvel jogador serс alterada no decorrer do jogo. Serс alternada entre 1 e 2 para cada jogada.*/
	    /*As variсveis (linha) e (coluna) alimentarуo nossa matrix [3] por [3].*/
	    /*A variсvel (numeroJogadas) terс valor mсximo igual a 9. Corresponde ao total de jogadas do Jogo da Velha.*/
		
		inteiro jogador = 1, linha, coluna, numeroJogadas = 0, vencedor = 0
		caracter tabuleiro[3][3]
		
		/*Vamos desenhar o tabuleiro de referъncia*/
		
		escreva("Olс! Este щ um jogo da velha! Vocъ deve jogar com outra pessoa!\n")
		escreva("Digite a posiчуo da sua jogada na seguinte forma: (linha,coluna).\nOu seja, linha 2 e coluna 2 serс: (1,1)\n")
		escreva("Antes de comeчarmos veja as posiчѕes para as jogadas:\n")
		escreva("[ (0,0) ]\t[ (0,1) ]\t[ (0,2) ]\n")
		escreva("[ (1,0) ]\t[ (1,1) ]\t[ (1,2) ]\n")
		escreva("[ (2,0) ]\t[ (2,1) ]\t[ (2,2) ]\n")
		escreva("\n")
		escreva("A primeira pessoa que jogar serс (X) e a segunda pessoa que jogar serс (O).\n")
		escreva("Ganha quem fizer linha, coluna ou diagonal. Bom jogo!\n")
		
		/*Este trecho preenche a matriz com espaчos vazios.*/
		para(inteiro i = 0; i < 3; i++){
		    para(inteiro j = 0; j < 3; j++){
		        tabuleiro[i][j] = ' '
		    }
		}
		
		escreva("#####################################################\n")
		escreva("Este щ o nosso tabuleiro, por favor, inicie a jogada!\n")
		escreva("#####################################################\n")
		
		/*Apresenta a matriz na tela.*/
		para(inteiro i = 0; i < 3; i++){
		    para(inteiro j = 0; j < 3; j++){
		        escreva("[",tabuleiro[i][j],"]")
		    }
		    escreva("\n")
		}
		
		enquanto((vencedor == 0)e(numeroJogadas < 9)){
		    se(jogador == 1){
		        escreva("\nVocъ щ o jogador ",jogador,". Por favor escolha sua jogada:\n")
		        escreva("\nDigite uma linha: ")
		        leia(linha)
		        escreva("\nDigite uma coluna: ")
		        leia(coluna)
		        se((linha < 3)e(coluna < 3)e(tabuleiro[linha][coluna] == ' ')){
		            escreva("Vocъ digitou: (",linha,",",coluna,").\n")
		            tabuleiro[linha][coluna] = 'X'
		            escreva("A posiчуo (",linha,",",coluna,"). Serс preenchida com (X).\n\n")
		            jogador = 2
		            
		            para(inteiro i = 0; i < 3; i++){
		                para(inteiro j = 0; j < 3; j++){
		                escreva("[",tabuleiro[i][j],"]")
		                }
		                escreva("\n")
		            }
		        }
		        senao{
		            escreva("#################################\n")
		            escreva("Vocъ digitou: uma opчуo invсlida!\n")
		            escreva("#################################\n")
		            para(inteiro i = 0; i < 3; i++){
		                para(inteiro j = 0; j < 3; j++){
		                    escreva("[",tabuleiro[i][j],"]")
		                }
		                escreva("\n")
		            }
		        }
		    } 
		    senao se(jogador == 2){
		        escreva("\nVocъ щ o jogador ",jogador,". Por favor escolha sua jogada:\n")
		        escreva("\nDigite uma linha: ")
		        leia(linha)
		        escreva("\nDigite uma coluna: ")
		        leia(coluna)
		        se((linha < 3)e(coluna < 3)e(tabuleiro[linha][coluna] == ' ')){
		            escreva("Vocъ digitou: (",linha,",",coluna,").\n")
		            tabuleiro[linha][coluna] = 'O'
		            escreva("A posiчуo (",linha,",",coluna,"). Serс preenchida com (O).\n\n")
		            jogador = 1
		            
		            para(inteiro i = 0; i < 3; i++){
		                para(inteiro j = 0; j < 3; j++){
		                    escreva("[",tabuleiro[i][j],"]")
		                }
		                escreva("\n")
		            }
		        }
		        senao{
		            escreva("#################################\n")
		            escreva("Vocъ digitou: uma opчуo invсlida!\n")
		            escreva("#################################\n")
		            para(inteiro i = 0; i < 3; i++){
		                para(inteiro j = 0; j < 3; j++){
		                    escreva("[",tabuleiro[i][j],"]")
		                }
		                escreva("\n")
		            }
		        }
		    }
		    
		    escreva("\n\n")
		
		/*Aqui comeчa o teste para verificar quem vence.*/
		    se(vencedor == 0){
		    /*Teste para as linhas.*/
		    para(inteiro i = 0; i < 3; i++){
		        se((tabuleiro[i][0] == 'X')e(tabuleiro[i][1] == 'X')e(tabuleiro[i][2] == 'X')){
		            vencedor = 1
		        }
		        senao se((tabuleiro[i][0] == 'O')e(tabuleiro[i][1] == 'O')e(tabuleiro[i][2] == 'O')){
		            vencedor = 2
		        }
		    }
		
		    /*Teste para as colunas.*/
		    para(inteiro i = 0; i < 3; i++){
		        se((tabuleiro[0][i] == 'X')e(tabuleiro[1][i] == 'X')e(tabuleiro[2][i] == 'X')){
		            vencedor = 1
		        }
		        senao se((tabuleiro[0][i] == 'O')e(tabuleiro[1][i] == 'O')e(tabuleiro[2][i] == 'O')){
		            vencedor = 2
		        }
		    }
		
		    /*Teste para a primeira diagonal.*/
	        se((tabuleiro[0][0] == 'X')e(tabuleiro[1][1] == 'X')e(tabuleiro[2][2] == 'X')){
	            vencedor = 1
		    }
            senao se((tabuleiro[0][0] == 'O')e(tabuleiro[1][1] == 'O')e(tabuleiro[2][2] == 'O')){
		        vencedor = 2
            }
        
            /*Teste para a segunda diagonal.*/
	        se((tabuleiro[0][2] == 'X')e(tabuleiro[1][1] == 'X')e(tabuleiro[2][0] == 'X')){
	            vencedor = 1
		    }
            senao se((tabuleiro[0][2] == 'O')e(tabuleiro[1][1] == 'O')e(tabuleiro[2][0] == 'O')){
		        vencedor = 2
            }
            
            numeroJogadas = numeroJogadas++
            /*escreva("Jogada: ",numeroJogadas,"\n")*/
		}
	}
	
		/*TESTE PARA VERFICAR VENCEDOR*/
		se(vencedor == 1){
		    escreva("\nA pessoa que escolheu (X) venceu!\n")
		}
		senao se(vencedor == 2){
		    escreva("\nA pessoa que escolheu (O) venceu!\n")
		}
		senao{
		    escreva("\nDeu VELHA! Jogue novamente!\n")
		}
	}
}
