# Algoritmo Genético otimizações simples
Classe para realizar um algoritmo genético

Dados os parâmetros informados pelo usuário, a classe tem implementadas funções para:

* Criar populações com genótipo binário;
* Reproduzir a população;
* Criar mutações nos genótipos de forma binária;
* Adquirir os fenótipos através das cadeias de genótipos, sejam variáveis discretas ou não;
* Penalizar valores de aptidão não factíveis usando regra própria;
* Adquirir os reprodutores para a próxima geração através do sistema de ranking;
* Caso seja captada uma convergência inválida (que viola alguma das restrições), há também a possibilidade de eliminar parte da população;
* Imigrar novos indivíduos após a eliminação;

As populações tem tamanho fixo e a taxa de reprodução é de 100%, onde todos os indivíduos reproduzem entre si.
