# pbd-indice-hash

Primeiro trabalho da disciplina de Projeto de Banco de Dados, sobre a implementação e o teste de um Índice Hash.

EPIC 1: Carga e Organização dos Dados

    [x] CA01: O sistema permite selecionar um arquivo .txt e carrega os registros.

    [x] CA02: O sistema informa o total de palavras carregadas.

    [x] CA03: O sistema trata e informa erro se o arquivo estiver vazio ou ilegível.

    [x] CA04: Existe um campo na interface para digitar o tamanho da página.

    [x] CA05: Se o valor do tamanho da página for inválido (zero, negativo ou vazio), o sistema impede a continuação.

    [x] CA06: Após carregar o arquivo, o sistema exibe a quantidade total de páginas calculada.

    [?] CA07: O sistema exibe na interface a primeira e a última página, contendo o número da página e os primeiros 5 registros dela.

EPIC 2: Construção do Índice Hash Estático

    [x] CA08: O sistema calcula e exibe o número de buckets (NB).

    [x] CA09: O sistema cria NB buckets com capacidade FR.

    [x] CA10: O sistema impede que NB≤NR/FR.

    [x] CA11: Dada uma chave, o sistema retorna sempre o mesmo bucket (determinismo).

    [x] CA12: A função hash sempre retorna um bucket dentro do intervalo válido [0..NB-1].

    [x] CA13: Ao final da construção, o índice contém todos os registros do arquivo.

    [x] CA14: O sistema exibe o tempo de construção do índice.

EPIC 3: Tratamento de Colisões e Overflow

    [x] CA15: O sistema insere registros mesmo quando múltiplas chaves geram o mesmo bucket.

    [x] CA16: O sistema contabiliza colisões que excedem o tamanho definido para o bucket.

    [x] CA17: Quando a capacidade (FR) for excedida, o sistema usa a estratégia de bucket overflow.

    [ ] CA18: O sistema contabiliza quantos buckets entraram em overflow.

EPIC 4: Pesquisa por Índice

    [?] CA19: Ao buscar uma chave, o sistema mostra se foi encontrada, em qual página está e o *custo estimado em leituras de página*.

    [x] CA20: Se a chave não existir, o sistema informa "não encontrada".

EPIC 5: Table Scan e Comparação

    [ ] CA21: O sistema exibe os registros lidos durante o table scan.

    [ ] CA22: O sistema informa o número da página onde encontrou a chave e o custo (páginas lidas) do scan.

    [ ] CA23: O sistema exibe o tempo de execução da busca com índice e do table scan.

    [ ] CA24: O sistema exibe o custo estimado (páginas lidas) de ambos e a diferença percentual entre eles.

EPIC 6: Estatísticas e Métricas

    [ ] CA25: A interface mostra o percentual de colisões após construir o índice.

    [ ] CA26: A interface mostra o percentual de overflow após construir o índice.

EPIC 7: Interface Gráfica e Visualização

    [x] CA27: O usuário consegue visualizar a primeira e a última página.

    [x] CA28: O usuário consegue visualizar os buckets e seus conteúdos.

    [ ] CA29: Durante a busca, o bucket e a página acessados são destacados visualmente.
