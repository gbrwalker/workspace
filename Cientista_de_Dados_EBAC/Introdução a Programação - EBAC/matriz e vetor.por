programa {
	funcao inicio() {
		real matrizNotas[2][3]
		cadeia vetorNomes[2], vetorTitulos[4] = {"Nome","Nota 1", "Nota 2", "Média"}
		
		para(inteiro i = 0; i < 2; i++){
		    escreva("Digite o nome: \n")
		    leia(vetorNomes[i])
		}
		
		para(inteiro j = 0; j < 2; j++){
		    para(inteiro z = 0; z < 2; z++){
		        escreva("Digite a nota: \n")
		        leia(matrizNotas[j][z])
		    }
		    matrizNotas[j][2] = (matrizNotas[j][0] + matrizNotas[j][1]) / 2
		}
		
		para(inteiro i = 0; i < 4; i++){
		    escreva("|||",vetorTitulos[i],"\t\t")
		}
		
		escreva("\n\n")
		
		para(inteiro i = 0; i < 4; i++){
		    se(i < 1){
		        escreva("|||",vetorNomes[i],"\t\t","|||", matrizNotas[i][i],"   ","\t\t","|||",matrizNotas[i][i + 1],"   ","\t\t","|||",matrizNotas[i][i + 2],"\n")
		    }
		    senao se(i == 1){
		        escreva("|||",vetorNomes[i],"\t","|||", matrizNotas[i][i - 1],"   ","\t\t","|||",matrizNotas[i][i],"   ","\t\t","|||",matrizNotas[i][i + 1],"\n")
		    }
	}
		
	}
}
