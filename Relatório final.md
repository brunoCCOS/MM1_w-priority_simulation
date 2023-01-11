# Simulador sistema de filas M|M|1 com prioridade e interrupção

##### Autor: Bruno Llacer Trotti - 119169008



#  Introdução 



​	O simulador desenvolvido visa replicar o funcionamento de uma sistema de duas filas com prioridade e interrupção. O simulador funciona programando apenas dois tipos de eventos de forma simultânea, o fim do próximo serviço e a próxima chegada de um novo cliente, e avança até o evento mais próximo entre esses dois. Ao atingir cada um dos eventos aplicas os tratamentos necessários: caso seja a chegada de um novo freguês verifica se ele deve entrar no servidor ou ser posto na fila de espera, caso seja o fim de um serviço verifica como tratar o freguês que acaba de terminar o serviço e insere, se houver, um novo freguês no servidor. Todo o tratamento de eventos, desde a contagem de tempo até a o tratamento das filas, fregueses e servidor são realizadas pela entidade *Manager* que está implementada dentro de *simulation.py*, lá tratamos todas as operações referentes a simulação como avanço do timestep, calculo de estatísticas, mudanças de fila e etc.

​	 Ao ocorrer cada evento as coletas são realizadas registrando o tempo em cada estrutura do sistema(fila de espera e servidor) e o número de indivíduos, por ex: ao fim de um serviço o tempo atual é subtraído do instante em que o cliente entrou em serviço e é calculado seu tempo de serviço e armazenado na sua estrutura de classe, esse processo é análogo para tempos na fila de espera 1 e 2, serviço residual e etc. Por sua vez, as estruturas utilizadas para representar cada uma das entidades foram instancias de classes, logo as filas são instancias que possuem seus próprios atributos como taxa de chegada, número de fregueses presentes e a fila destes, os freguês são instancias com tempo de serviço residual, tempo na fila de espera e assim continua. Cada instancia armazena suas próprias estatísticas que são coletadas no fim de suas vidas(quando o freguês termina o serviço ou a simulação termina), cada uma das classes foi implementada no python com seu nome sendo assim *client.py*,*fila.p*,*servidor.py*.

​	Para calculo das estatísticas foi usado o método replicativo e armazenamos todos os logs de cada rodada para no fim realizar o calculo das médias por rodada e a média geral. Todos os métodos e rotinas para cálculos das estatísticas estão no arquivo *statistics.py*. O calculo dos intervalos de confiança foi feito usando a inversa das cdf de cada distribuição, para, assim, a partir do intervalo de confiança obter os valores críticos de cada distruibuição. 

​	 Para analise dos números usamos como base $\rho=0.9$ pois entediamos que era o que continha maior variancia e portanto qualquer configuração que funcionasse pra ele funcionaria para os outros. Analisando o número de fregueses por rodada notamos convergência das médias de pessoas no sevidor e de $\rho$  após cerca de 3000 fregueses, aumentar o número de fregueses além disso não causou nenhuma variação maior que 1 desvio padrão das médias, logo foram estatisticamente insignificantes, assim sendo escolhemos como margem o número máximo de 3000 fregueses. Para controle do intervalo de confiança observamos que 200 rodadas com 3 mil coletas em cada mantem a precisão controlada, que descontando os 430 da fase transiente concluem 2570 fregueses por rodada. Todos os testes foram feitos para diferentes valores de $\rho$ mas para ilustração a baixo usamos sempre o caso de $\rho = 0.9$ uma vez que os valores se encaixaram bem para todos os cenários e o procedimento foi o mesmo.

​	Os intervalos de confiança foram gerados usando amostras das Médias e Variâncias de cada rodada e construindo um intervalo a partir da t-student usando a inversa da cdf para encontrar o ponto crítico.

​	O cálculo do número de pessoas nas filas foi realizado de forma alternativa. Como não iteramos sobre os instantes de tempo, para dimensionar a quantidade de pessoas que temos de forma correta, para cada vez que havia uma chegada ou partida na fila fazíamos o produto entre o número de fregueses até aquele momento pelo tempo que permaneceu naquele estado (N fregueses * intervalo com N fregueses) gerando assim uma lista do número de pessoas ponderado pelo tempo em que aquela quantidade permaneceu na fila. Ex: se no instante 2 a fila tinha 10 fregueses e no instante 4 acontece uma partida/chegada, então o calculávamos (4-2)*10. Por fim como no final tínhamos na verdade lista de tempos escaladas pelo número de fregueses, para partir de Nq para N, apenas somávamos o tempo em serviço que os fregueses de uma determinada fila ficaram em serviço durante todo o processo, pois matematicamente para calculo da média é equivalente fazermos o calculo dos tempos com 1 freguês ou somarmos essa quantidade posteriormente.

​	Para a implementação da geração de números aleatórios foi usado as funções nativas da biblioteca numpy que oferece um gerador de números pseudo-aleatórios e a seleção da semente inicial é deixada por padrão, onde a biblioteca usa o tempo atual do sistema operacional para seleciona-la. Como o método utilizado para coleta de estatísticas foi o replicativo, mantemos as estruturas geradoras de números vivas até o fim da execução continuando a simulação de onde ela parou na rodada anterior.

​	A programação do simulador foi feita usando a linguagem python que é uma linguagem interpretada então significativamente mais lenta que outras alternativas, porém em função da familiaridade e facilidade da linguagem para lidar com operações de dados, arrays e etc foi preferida essa mesmo apesar da sua menor velocidade. Os testes foram realizados em uma máquina Windows 10, com processador Intel i3-9100F  e com 16GB de RAM DDR4

# Corretude

​	Os teste de corretude foram realizados verificando a consistência da simulação com os valores inciais. Como o $\rho$ é um parametro passado do qual derivamos a taxa de chegada, uma forma de ver se o sistema estava se comportando de forma correta era verificar se ao final da simulação o  $\rho$ se mantinha próximo ao dado como entrada, e vimos que isso foi verdade na maioria dos casos e convergia para tal quanto maior o n° de fregueses.

![rho_time_series](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\rho_time_series.png)

​				**O número de fregueses de cada simulação era dado pelo número da simulação + 1 * 60**

​						          	**ex: simulação 25 teve n_fregueses = 26 * 60 = 1560 **

​	Também foi usado a fila 1 como métrica de corretude, esperamos que o tempo média de espera na fila convirja para um valor especifico e não tenda a explodir (demonstrando equilíbrio) para um cada vez maior número de fregueses. Verificamos também que para cenário com 10 

![W1_avanço do n fregueses](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W1_avanço do n fregueses.png)

​						                         **O número de fregueses de cada simulação era dado pelo número da simulação + 1 * 60**

​						          	                                    **ex: simulação 25 teve n_fregueses = 26 * 60 = 1560 **



**_Todos os testes foram feitos para diferentes valores de $\rho$ mas para ilustração usamos sempre o caso de $\rho = 0.9$ uma vez que os valores se encaixaram bem para todos os cenários e o procedimento foi o mesmo_**

# Estimativa da fase transiente

​	Para a estimativa da fase transiente foram realizadas simulações acompanhando a cada rodada o comportamento das métricas e das médias móveis de cada estatísticas e através de uma avaliação empírica estipulamos o momento em que estas pareciam começar a repetir o padrão ou manter uma consistência. Também comparamos a média obtida após o corte de um certo número de fregueses em um intervalo menor de tempo com a obtida para uma simulação bem longa. Foi dado alguma margem para erro na estimativa da fase transiente de forma a garantir que não comecemos a coletar estatísticas de forma equivocada.

Média para simulação com 10000 fregueses:



W1 = 0.424804095012947

W2 = 4.0328801756439985

N  = 2.772663644847354



Valores para diferentes fases transientes simulando 500 fregueses

![W1-transiente](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W1-transiente.png)

![W2-transiente](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W2-transiente.png)



 Analisando os resultados aumentando gradativamente a fase transiente, vimos que na maioria das simulações a média fica mais próxima da original a partir da faixa dos 430 fregueses(para o caso do número de pessoas na fila, a partir do instante que o 430° freguês chegar). Logo escolhemos esse threshold como determinante da nossa fase transiente



**_Todos os testes foram feitos para diferentes valores de $\rho$ mas para ilustração usamos sempre o caso de $\rho = 0.9$ uma vez que os valores se encaixaram bem para todos os cenários e o procedimento foi o mesmo_**

# Resultados

A simulação para diferentes valores de $\rho$  resultaram nas seguintes tabelas de resultados.

Para otimização buscamos o menor número necessário de fregueses a partir do qual a média começa a convergir para diferetes $\rho$ para usar como número minimo de fregueses. Observando as médias de W1 e W2 vimos que isso acontece por volta da 60° iteração(quando estamos testando para 60*50=3000fregueses) e a partir desta os desvios respeitam o intervalo de até um desvio padrão se devendo apenas a aleatoriedade.



![W1freg](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W1freg.png)

![W2freg](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W2freg.png)



​																											**_Imagens para $\rho=0.9$_**



Assim realizamos as simulações para diferentes valores de $\rho$ utilizando 3000 coletas por rodada e descartando 430 delas.

Para $\rho = 0.2$

```
Soluções Analíticas 

W1: 0.11111111111111112
T1: 1.1111111111111112
W2 0.5277777777777777
T2 1.5277777777777777
Nq1: 0.011
N1: 0.111
Nq2: 0.05277777777777777
N2: 0.1527777777777778
```

````
Estatisticas a respeito de T1:
        \ esperança: 1.112304781275521
        \ variancia: 1.2317265756019842
        \ desvio padrão: 1.1098317780645786
        \ intervalo de confiança para média: (1.1090012469426778, 1.11560844669289), valor médio 1.1123048468177839, precisão: 0.002970048979429899
------------------------------
Estatisticas a respeito de W1:
        \ esperança: 0.11171551158671816
        \ variancia: 0.2346208841874424
        \ desvio padrão: 0.4843767998030484
        \ intervalo de confiança para média: (0.11011397710902261, 0.11331686048309846), valor médio 0.11171541879606053, precisão: 0.014335010370962275
        \ intervalo de confiança para variancia: (0.22833624699893945, 0.2406404471282056) valor médio 0.23448834706357252, precisão:0.026236272043681404 
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.11119244831896304
        \ variancia: 1.0148561895270875e-05
        \ desvio padrão: 0.003185680758530408
        \ intervalo de confiança para média: (0.11074824214057426, 0.11163665449735181), valor médio 0.11119244831896304, precisão: 0.00399493117657184   
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.011173032234439741
        \ variancia: 1.4903605351445507e-06
        \ desvio padrão: 0.0012208032335903074
        \ intervalo de confiança para média: (0.011002805403799, 0.011343259065080482), valor médio 0.011173032234439741, precisão: 0.015235508774067078  
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 1.5260894000453549
        \ variancia: 2.713041883935662
        \ desvio padrão: 1.6471314106456905
        \ intervalo de confiança para média: (1.5189624802180377, 1.5332140164103227), valor médio 1.5260882483141802, precisão: 0.004669302777224134
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 0.5270924752893164
        \ variancia: 1.4946733640020187
        \ desvio padrão: 1.222568347374501
        \ intervalo de confiança para média: (0.5210702015540681, 0.5331133364104198), valor médio 0.527091768982244, precisão: 0.011424134813948652
        \ intervalo de confiança para variancia: (1.4505818535438328, 1.5350209500114256) valor médio 1.4928014017776292, precisão:0.028282093105969283   
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 0.15257025237484856
        \ variancia: 3.877188076306215e-05
        \ desvio padrão: 0.006226707056146303
        \ intervalo de confiança para média: (0.15170201040240647, 0.15343849434729065), valor médio 0.15257025237484856, precisão: 0.005690768409485976  
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 0.05270842541266129
        \ variancia: 2.1469183655479775e-05
        \ desvio padrão: 0.0046334850442706485
        \ intervalo de confiança para média: (0.05206233974364826, 0.05335451108167432), valor médio 0.05270842541266129, precisão: 0.012257730409412523  
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.19988124304671054
        \ variancia: 1.731890029794212e-05
        \ desvio padrão: 0.004161598286469048
------------------------------
````



Para $\rho = 0.4$

```
Soluçoes analíticas

W1: 0.25
T1: 1.25
W2 1.5
T2 2.5
N1: 0.25
Nq1: 0.05
Nq2: 0.30000000000000004
N2: 0.5
```



````
Estatisticas a respeito de T1:
        \ esperança: 1.254441019264655
        \ variancia: 1.5673514095731955
        \ desvio padrão: 1.2519390598480404
        \ intervalo de confiança para média: (1.2494322788436354, 1.2594506557261922), valor médio 1.2544414672849138, precisão: 0.003993162353059151
------------------------------
Estatisticas a respeito de W1:
        \ esperança: 0.25138629849897476
        \ variancia: 0.5669486483262148
        \ desvio padrão: 0.7529599247810037
        \ intervalo de confiança para média: (0.2483630015940181, 0.25440989429437266), valor médio 0.2513864479441954, precisão: 0.012027085687803035
        \ intervalo de confiança para variancia: (0.550524452624005, 0.5824351260851399) valor médio 0.5664797893545724, precisão:0.028165765187750904    
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.2506908571117251
        \ variancia: 8.319395621744987e-05
        \ desvio padrão: 0.009121072098029369
        \ intervalo de confiança para média: (0.24941902955379264, 0.2519626846696576), valor médio 0.2506908571117251, precisão: 0.005073290556287289    
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.05025076329690185
        \ variancia: 2.1464726145802216e-05
        \ desvio padrão: 0.004633004008826478
        \ intervalo de confiança para média: (0.04960474470269402, 0.050896781891109674), valor médio 0.05025076329690185, precisão: 0.012855896146112003 
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 2.5067679949739805
        \ variancia: 7.878502962041384
        \ desvio padrão: 2.806867108012309
        \ intervalo de confiança para média: (2.489905881016413, 2.523627730586571), valor médio 2.506766805801492, precisão: 0.006726164055650199
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 1.5070085994691464
        \ variancia: 6.383661906787819
        \ desvio padrão: 2.5265909654686527
        \ intervalo de confiança para média: (1.4907972588639942, 1.5232181957084376), valor médio 1.507007727286216, precisão: 0.010756725482365751
        \ intervalo de confiança para variancia: (6.185041508324702, 6.555250132854204) valor médio 6.370145820589453, precisão:0.02905809654568041       
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 0.5010255390837931
        \ variancia: 0.0007780092082516651
        \ desvio padrão: 0.02789281642738261
        \ intervalo de confiança para média: (0.49713620982299694, 0.5049148683445892), valor médio 0.5010255390837931, precisão: 0.007762736542149936    
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 0.30125201844222815
        \ variancia: 0.0006396452130866299
        \ desvio padrão: 0.025291208217217104
        \ intervalo de confiança para média: (0.2977254532272668, 0.3047785836571895), valor médio 0.30125201844222815, precisão: 0.011706362112350998    
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.40021361445638814
        \ variancia: 7.782414705700427e-05
        \ desvio padrão: 0.008821799536205993
------------------------------
````



Para $\rho = 0.6$



````
Soluções analíticas

T1: 1.4285714285714286
W1: 0.4285714285714286
N1: 0.426
Nq1: 0.126
W2 3.6428571428571432
T2 4.642857142857143
Nq2: 1.092857142857143
N2: 1.392857142857143
````



```
Estatisticas a respeito de T1:
        \ esperança: 1.4281108743141613
        \ variancia: 2.0449516764995357
        \ desvio padrão: 1.4300180685919797
        \ intervalo de confiança para média: (1.4214418721848248, 1.4347806310597189), valor médio 1.4281112516222718, precisão: 0.004670069947191391
------------------------------
Estatisticas a respeito de W1:
        \ esperança: 0.42728826731923114
        \ variancia: 1.0453860170384024
        \ desvio padrão: 1.0224412046853366
        \ intervalo de confiança para média: (0.4221710298962791, 0.43240602161082486), valor médio 0.427288525753552, precisão: 0.011976675124256717
        \ intervalo de confiança para variancia: (1.0166610361857598, 1.0714194839048718) valor médio 1.0440402600453158, precisão:0.0262242989157982     
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.42805287683648496
        \ variancia: 0.00030563064490489217
        \ desvio padrão: 0.017482295184125342
        \ intervalo de confiança para média: (0.4256151738392809, 0.43049057983368905), valor médio 0.42805287683648496, precisão: 0.005694864184116391   
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.12810853048734824
        \ variancia: 0.0001394106389244882
        \ desvio padrão: 0.011807228249021369
        \ intervalo de confiança para média: (0.12646214965530236, 0.12975491131939412), valor médio 0.12810853048734824, precisão: 0.012851453574424328  
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 4.643232768548803
        \ variancia: 27.76840720821034
        \ desvio padrão: 5.269573721679045
        \ intervalo de confiança para média: (4.5887080276895595, 4.697763695185042), valor médio 4.643235861437301, precisão: 0.011743498580505524
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 3.642244793016531
        \ variancia: 25.920126320486833
        \ desvio padrão: 5.091181230371478
        \ intervalo de confiança para média: (3.588674400477554, 3.695820459790863), valor médio 3.6422474301342085, precisão: 0.014708783706844572
        \ intervalo de confiança para variancia: (24.746688814862296, 26.798421086990096) valor médio 25.772554950926196, precisão:0.03980459593615236    
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 1.3925524280210617
        \ desvio padrão: 0.13071460544434924
        \ intervalo de confiança para média: (1.374325794612001, 1.4107790614301223), valor médio 1.3925524280210617, precisão: 0.013088651487945947      
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 1.0925529489786365
        \ variancia: 0.01577999515439588
        \ desvio padrão: 0.12561845069254707
        \ intervalo de confiança para média: (1.0750369151551478, 1.1100689828021253), valor médio 1.0925529489786365, precisão: 0.01603220588975891      
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.5999438253915621
        \ variancia: 0.00018514897792136321
        \ desvio padrão: 0.013606945943942132
------------------------------
```

`

Para $\rho = 0.8$

```
Soluções analíticas 

W1: 0.6666666666666667
T1: 1.6666666666666667
W2 10.66666666666667
T2 11.66666666666667
Nq1: 0.264
N1: 0.664
Nq2: 4.266666666666668
N2: 4.666666666666668
```



````
Estatisticas a respeito de T1:
        \ esperança: 1.6678778462980837
        \ variancia: 2.783915205176451
        \ desvio padrão: 1.6685068789718702
        \ intervalo de confiança para média: (1.6579729462554622, 1.6777827687324194), valor médio 1.6678778574939408, precisão: 0.005938631053811786
------------------------------
Estatisticas a respeito de W1:
        \ esperança: 0.665724435475754
        \ variancia: 1.7787987384674362
        \ desvio padrão: 1.3337161386394918
        \ intervalo de confiança para média: (0.6577815637901692, 0.6736671539713406), valor médio 0.6657243588807549, precisão: 0.011931056727351069
        \ intervalo de confiança para variancia: (1.7332850137461835, 1.8178227224076167) valor médio 1.7755538680769, precisão:0.02380601067119294
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.666455515142272
        \ variancia: 0.0011302500353323778
        \ desvio padrão: 0.033619191473507774
        \ intervalo de confiança para média: (0.6617677093962069, 0.6711433208883371), valor médio 0.666455515142272, precisão: 0.007033936458706259      
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.2660865334218988
        \ variancia: 0.0006077904850840902
        \ desvio padrão: 0.024653407169884047
        \ intervalo de confiança para média: (0.26264890215458725, 0.26952416468921037), valor médio 0.2660865334218988, precisão: 0.012919223017802834   
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 11.670774706435216
        \ variancia: 175.15949349556234
        \ desvio padrão: 13.234783469916021
        \ intervalo de confiança para média: (11.356632756929447, 11.984908188479928), valor médio 11.670770472704687, precisão: 0.02691662187256087
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 10.672418307273777
        \ variancia: 172.79146516201965
        \ desvio padrão: 13.145016742553798
        \ intervalo de confiança para média: (10.358966710552956, 10.985861954325003), valor médio 10.67241433243898, precisão: 0.029369888773273577
        \ intervalo de confiança para variancia: (151.79902177530684, 183.67902717596522) valor médio 167.73902447563603, precisão:0.09502858830948109    
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 4.670974530322657
        \ desvio padrão: 0.9531335063226977
        \ intervalo de confiança para média: (4.538071134022137, 4.803877926623177), valor médio 4.670974530322657, precisão: 0.02845303382361616
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 4.272113258203035
        \ variancia: 0.8967745961725733
        \ desvio padrão: 0.9469818351861736
        \ intervalo de confiança para média: (4.1400676409875485, 4.4041588754185215), valor médio 4.272113258203035, precisão: 0.03090873514693016       
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.7992302538399959
        \ variancia: 0.00036090054476696964
        \ desvio padrão: 0.018997382576738556
------------------------------
````



Para $\rho = 0.9$

```
Soluções analíticas

W1: 0.8181818181818181
T1: 1.8181818181818181
W2 25.363636363636367
T2 26.363636363636367
Nq1: 0.3645
N1: 0.8145
Nq2: 11.413636363636366
N2: 11.863636363636365
```



````
Estatisticas a respeito de T1:
        \ esperança: 1.8137254477085647
        \ variancia: 3.2612591610412403
        \ desvio padrão: 1.8058956672635438
        \ intervalo de confiança para média: (1.802254901077593, 1.825194871510294), valor médio 1.8137248862939435, precisão: 0.0063239939546661525
------------------------------
Estatisticas a respeito de W1:
        \ esperança: 0.8135322623390598
        \ variancia: 2.263582338682241
        \ desvio padrão: 1.5045206341829416
        \ intervalo de confiança para média: (0.8036481481491278, 0.8234157580122241), valor médio 0.8135319530806759, precisão: 0.012149252274751174
        \ intervalo de confiança para variancia: (2.1990980872639936, 2.3180229475169005) valor médio 2.258560517390447, precisão:0.02632757885768617     
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.8153975799998017
        \ variancia: 0.0018522487594576547
        \ desvio padrão: 0.04303775969375793
        \ intervalo de confiança para média: (0.8093964643171373, 0.821398695682466), valor médio 0.8153975799998017, precisão: 0.007359741836204407      
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.3658324246750498
        \ variancia: 0.0011815501614175503
        \ desvio padrão: 0.03437368414088822
        \ intervalo de confiança para média: (0.36103941369035497, 0.3706254356597446), valor médio 0.3658324246750498, precisão: 0.013101657101478084    
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 25.529641973351307
        \ variancia: 678.5456409648167
        \ desvio padrão: 26.048908632893177
        \ intervalo de confiança para média: (24.586025401054016, 26.473264149838975), valor médio 25.529644775446496, precisão: 0.03696171187231008
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 24.53078762835707
        \ variancia: 675.8900098475694
        \ desvio padrão: 25.99788471871451
        \ intervalo de confiança para média: (23.58788096708892, 25.473700085170393), valor médio 24.530790526129657, precisão: 0.03843779751151392
        \ intervalo de confiança para variancia: (579.1522522423685, 681.1762765314883) valor médio 630.1642643869284, precisão:0.08095034108953837       
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 11.504086347059555
        \ variancia: 10.117211435611214
        \ desvio padrão: 3.1807564250679765
        \ intervalo de confiança para média: (11.060566809773336, 11.947605884345775), valor médio 11.504086347059555, precisão: 0.03855321699663554      
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 11.05513197472921
        \ variancia: 10.073918642122567
        \ desvio padrão: 3.1739437049391044
        \ intervalo de confiança para média: (10.612562392131569, 11.497701557326852), valor médio 11.05513197472921, precisão: 0.040032953347757964      
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.8985195276550982
        \ variancia: 0.00036836911673367807
        \ desvio padrão: 0.019192944451898935
------------------------------
````

​	Analisando os resultados obtidos é evidente o aumento de algumas métricas com o aumento da utilização do servidor, alinhado com o esperado, uma vez que mais tempo ocupado significa mais tempos de espera e mais pessoas no sistema. Em contra partida o tempo de serviço como independe do tempo ocupado permanece estável para todas as simulações.  Também observamos o aumento da variâncias e desvio padrão das métricas corroborando com nossa análise anterior.

​	Também fica claro que todos os tempos estimados compactuam com os da solução analíticas e estão contidos nos intervalos de confiança estimados, comprovando a corretude e funcionamento das nossas simulações para esse cenário conhecido.

​	

# Otimização



Porém em função do controle do intervalo de confiança que perdia precisão com um número menor de fregueses por rodada para estabilidade encontramos o valor de 2000 fregueses que satisfaz o intervalo para todos os valores de $\rho$ porem para $\rho = 0.6$ em específico conseguimos construir os IC com 5% de precisão utilizando um número menor de rodadas e coletas, os valores para  $\rho = 0.6$  se comportaram de forma mais calma em relação ao número de coletas

![W1freg0.6](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W1freg0.6.png)

![W2freg0.6](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W2freg0.6.png)

​																											**_Imagens para $\rho=0.6$_**



​	Tendo as médias atingindo estabilidade por volta da x=30 ou da 1500° coleta.  A repseito da fase transiente observando as métricas de W1, W2 e N para diferentes quantidades de rodadas descartadas podemos observar que para uma amostra de 500 coletas, percebemos que as médias se aproximas das médias de longo prazo em torno da 350° coleta, logo as primeiras 350 podem ser descartadas para melhor avaliação das métricas

![W1transiente0.6](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W1transiente0.6.png)

![W2transiente0.6](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W2transiente0.6.png)



Por fim simulando uma fila com $\rho=0.6$, 1500 coletas por rodada e e 100 rodadas obtemos os seguintes resultados 

```
Estatisticas a respeito de T1:
        \ esperança: 1.4363801801121192
        \ variancia: 2.091920997847153
        \ desvio padrão: 1.4463474678814745
        \ intervalo de confiança para média: (1.4236437192310742, 1.4491223338871222), valor médio 1.4363830265590982, precisão: 0.008869018285840786     
------------------------------
Estatisticas a respeito de W1:
        \ esperança: 0.43229351231260765
        \ variancia: 1.0789685917878795
        \ desvio padrão: 1.0387341294998829
        \ intervalo de confiança para média: (0.42222995448526385, 0.4423620092996388), valor médio 0.43229598189245133, precisão: 0.023285035782941322   
        \ intervalo de confiança para variancia: (1.0190564042434713, 1.1337736537937546) valor médio 1.076415029018613, precisão:0.05328671862509811     
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.4284801073862725
        \ variancia: 0.0006192418330340846
        \ desvio padrão: 0.02488457017981393
        \ intervalo de confiança para média: (0.4235424687880931, 0.43341774598445193), valor médio 0.4284801073862725, precisão: 0.011523612212242474    
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.12905039428152523
        \ variancia: 0.00027916143592844817
        \ desvio padrão: 0.01670812484776338
        \ intervalo de confiança para média: (0.1257351398264397, 0.13236564873661077), valor médio 0.12905039428152523, precisão: 0.025689611206094174   
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 4.541640391610515
        \ variancia: 25.875150036188895
        \ desvio padrão: 5.086762235075362
        \ intervalo de confiança para média: (4.433563849282104, 4.649777281512257), valor médio 4.5416705653971805, precisão: 0.02380329320641129        
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 3.5419881913559372
        \ variancia: 24.061328022824338
        \ desvio padrão: 4.905234757157331
        \ intervalo de confiança para média: (3.4352848256206356, 3.6487498125061815), valor médio 3.5420173190634086, precisão: 0.03013325001781625
        \ intervalo de confiança para variancia: (21.981385353436604, 25.563827704275997) valor médio 23.7726065288563, precisão:0.07534811856854774      
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 1.3567362700263212
        \ variancia: 0.034760749120453134
        \ desvio padrão: 0.18644234798042297
        \ intervalo de confiança para média: (1.3197420632921377, 1.3937304767605048), valor médio 1.3567362700263212, precisão: 0.027267058124321994     
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 1.058623419979999
        \ variancia: 0.032122987635588796
        \ desvio padrão: 0.17922886942562796
        \ intervalo de confiança para média: (1.0230605238885924, 1.0941863160714058), valor médio 1.058623419979999, precisão: 0.03359352855813319       
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.5975425631510694
        \ variancia: 0.000355710101681182
        \ desvio padrão: 0.01886027840942922
```

Obtendo assim o Fator Mínimo= 1500*50 + 320 = 75320 e levando 6.685999393463135 segundos para execução do programa em uma máquina Windows com Intel Core i3-9100F e 16Gb de ram.

# Conclusões

Por fim, o desenvolvimento do simulador deu bastante trabalho principalmente para implementação da segunda fila e realização da corretude. Ter certeza do funcionamento perfeito sem o auxilio de formulas analíticas é bem complicado principalmente pela grande volatilidade da fila 2, o fator velocidade da linguagem também foi um empecilho pois gerava demora para alguns testes, sendo esse talvez uma melhora óbvia que poderia ser feita, implementar o programa em uma linguagem mais rápida como java ou C++.

​	Fiquei bem satisfeito com o método de coleta dentro das rodadas e achei bem eficiente  em questão de número de coletas, porém a manutenção de uma instancia em memória para cada freguês com suas próprias estatísticas com certeza é sacrifício de eficiência em nome de uma implementação mais limpa e fácil, apesar de limparmos os fregueses entre rodadas para liberar memória de forma automática graças aos mecanismos da linguagem, uma possivel melhora era também a remoção de fregueses durante o processo na medida que eles deixam o sistema. Além disso a forma de coleta de estatísticas entre rodadas provavelmente pode ser melhorada, fazer a iteração completa por todos os resultados da rodada adiciona uma complexidade n ao algoritmo que talvez se fosse feito de forma simultânea à simulação da rodada ou de forma acumulativa não geraria essa complexidade.

​	Por fim foi um trabalho bem interessante de se desenvolver e muito bom de ver as aplicações práticas do conteúdo aprendido, uma ótima forma de realmente exercitar as competências desenvolvidas durante o curso.

