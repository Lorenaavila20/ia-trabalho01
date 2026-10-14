# Registro de uso de IA

## Ferramenta: Claude (Anthropic), via chat

| Finalidade | Partes afetadas | Como verifiquei |
|---|---|---|
| Esclarecimento do enunciado e planejamento: cronograma, decisões de projeto (descoberto na inserção, teste de objetivo ao retirar, obsolescência no heap, definição das métricas) | Estrutura geral de `src/search.py` | Confrontei com as seções 2.3 e 2.6 do enunciado |
| Explicação em linguagem natural da lógica de cada algoritmo e das heurísticas (roteiros passo a passo, sem código pronto), usada como guia para eu escrever o código | `src/heuristics.py`, `src/search.py` | Escrevi o código a partir do roteiro, rodei os testes e comparei os resultados com simulações feitas à mão |
| Criação de casos de teste (mapas pequenos e asserts) | `tests/test_search.py` | Li cada caso, executei e conferi à mão os valores esperados |
| Revisão do meu código, apontando erros em versões iniciais (argumentos do `SearchResult`, contagem de `generated` em reinserções, estados distintos na fronteira, tupla `(f, h, ordem)` do A*) | `bfs`, `dfs`, `uniform_cost`, `greedy`, `astar` em `src/search.py` | Corrigi no meu código, rodei os testes e comparei com simulações feitas à mão |
| Esqueleto do script de experimentos (estrutura e medição de tempo); completei a mediana e a impressão da tabela | `scripts/run_experiments.py` | Comparei a saída com os resultados obtidos nas execuções individuais |
| Orientação sobre Git e ambiente virtual (comandos) | Repositório | Executei e conferi `git status` e o resultado |
| Rascunho do `README.md` e deste arquivo | `README.md`, `IA_USAGE.md` | Revisei e ajustei ao que realmente fiz |

| Revisão do `conflicts`, `moves`, `hill_climbing` e `random_restart` e casos de teste das 8 rainhas | `src/eight_queens.py`, `src/hill_climbing.py`, `tests/test_queens.py` | Executei os testes, comparei com contas à mão e rodei as 100 sementes |
| Revisão crítica do relatório (números, erros factuais, respostas às 11 questões) | `modelo_relatorio/relatorio_sbc.tex` | Conferi cada afirmação com a saída de `scripts/run_experiments.py` |

## Outras ferramentas

Nenhuma.

## Recursos externos consultados

Documentação oficial do Python (`heapq` e `collections.deque`) e o material da disciplina de Inteligência Artificial.