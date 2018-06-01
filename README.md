# interpreterlib

## Fases do projeto:

### 1. Análise léxica
Nesta fase você precisa apenas criar uma varredura do programa, isto é, basta classificar cada token e imprimir na tela dentro de um laço de repetição.

### 2. Análise sintática
Nesta fase você deve integrar a análise léxica com a sintática, isto é, agora o seu analisador léxico deve fornecer uma função get_token() que o analisador sintático pode usar para validar a gramática, além de gerar uma árvore de sintaxe abstrata para o programa. Nesta fase é interessante criar uma função que imprime a árvore, pois pode ajudar com debug.

Original Grammar  
 Start ::= {Dec} Exp  
 Dec  ::= Var '=' Exp  
 Exp  ::= Exp BinOp Exp  
		  | UnOp Exp  
		  | Num  
		  | '@' Var|  
	    | '(' Exp ')'  
 BinOp::= '+' | '-' | '/' | '\*' | '^'  
 Var  ::= 'x' | 'y' | 'z'  
 Num	::= [0-9]+[(.)[0-9]]+  

Implemented Grammar  

Start = Declaration Expression {TkEnd}  
Declaration = Declaration Declaration  
		  | {TkVar} {TkEqual} Expression {TkEnd}  
      | ''  
Expression = Term [+-] Expression  
      | Term  
Term = Factor [\*/^] Term  
      | Factor  
Factor = Element  
      | '-' Element  
Element = Terminal  
      | Terminal '^' Factor  
Terminal = {TkNum}  
      | {TkVarAccess} {TkVar}  
      | {TkOpenParentesis} Expression {TkCloseParentesis}  


### 3. Interpretação com análise semântica
Nesta fase você deve integrar a análise sintática com a interpretação do programa. E nesta fase que você também deve fazer a análise semântica das expressões e declarações de variáveis, o que pode ocorrer durante a interpretação, parecido com o que ocorre em linguagens dinamicamente tipadas. Em resumo, você deve percorrer a árvore gerada pela análise sintática e imprimir o resultado da interpretação do programa. Se existir algum problema semântico a interpretação é abortada e uma mensagem de erro deve ser exibida. O exemplo disponibilizado pelo professor mostra como integrar as fases do projeto.

#### Erros:
• divisão por zero;  
• declaração de variável duplicada;  
• uso de variável não declarada.  
