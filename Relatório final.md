# Simulador sistema de filas M|M|1 com prioridade e interrupção

##### Autor: Bruno Llacer Trotti - 119169008



#  Introdução 



​	O simulador desenvolvido visa replicar o funcionamento de uma sistema de duas filas com prioridade e interrupção. O simulador funciona programando apenas dois tipos de eventos de forma simultânea, o fim do próximo serviço e a próxima chegada de um novo cliente, e avança até o evento mais próximo entre esses dois. Ao atingir cada um dos eventos aplicas os tratamentos necessários: caso seja a chegada de um novo freguês verifica se ele deve entrar no servidor ou ser posto na fila de espera, caso seja o fim de um serviço verifica como tratar o freguês que acaba de terminar o serviço e insere, se houver, um novo freguês no servidor. Todo o tratamento de eventos, desde a contagem de tempo até a o tratamento das filas, fregueses e servidor são realizadas pela entidade *Manager* que está implementada dentro de *simulation.py*, lá tratamos todas as operações referentes a simulação como avanço do timestep, calculo de estatísticas, mudanças de fila e etc.

​	 Ao ocorrer cada evento as coletas são realizadas registrando o tempo em cada estrutura do sistema(fila de espera e servidor) e o número de indivíduos, por ex: ao fim de um serviço o tempo atual é subtraído do instante em que o cliente entrou em serviço e é calculado seu tempo de serviço e armazenado na sua estrutura de classe, esse processo é análogo para tempos na fila de espera 1 e 2, serviço residual e etc. Por sua vez, as estruturas utilizadas para representar cada uma das entidades foram instancias de classes, logo as filas são instancias que possuem seus próprios atributos como taxa de chegada, número de fregueses presentes e a fila destes, os freguês são instancias com tempo de serviço residual, tempo na fila de espera e assim continua. Cada instancia armazena suas próprias estatísticas que são coletadas no fim de suas vidas(quando o freguês termina o serviço ou a simulação termina), cada uma das classes foi implementada no python com seu nome sendo assim *client.py*,*fila.p*,*servidor.py*.

​	Para calculo das estatísticas foi usado o método replicativo e armazenamos todos os logs de cada rodada para no fim realizar o calculo das médias por rodada e a média geral. Todos os métodos e rotinas para cálculos das estatísticas estão no arquivo *statistics.py*. O calculo dos intervalos de confiança foi feito usando a inversa das cdf de cada distribuição, para, assim, a partir do intervalo de confiança obter os valores críticos de cada distruibuição. 

​	 Para analise dos números usamos como base $\rho=0.9$ pois entediamos que era o que continha maior variancia e portanto qualquer configuração que funcionasse pra ele funcionaria para os outros. Analisando o número de fregueses por rodada notamos convergência das médias de pessoas no sevidor e de $\rho$  após cerca de 3000 fregueses, aumentar o número de fregueses além disso não causou nenhuma variação maior que 1 desvio padrão das médias, logo foram estatisticamente insignificantes, assim sendo escolhemos como margem o número máximo de 3000 fregueses. Para controle do intervalo de confiança observamos que 200 rodadas com 3 mil coletas em cada mantem a precisão controlada, que descontando os 430 da fase transiente concluem 2570 fregueses por rodada. Todos os testes foram feitos para diferentes valores de $\rho$ mas para ilustração a baixo usamos sempre o caso de $\rho = 0.9$ uma vez que os valores se encaixaram bem para todos os cenários e o procedimento foi o mesmo.

​				

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

![N-transiente](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\N-transiente.png)



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

````
ACULDADE/AVALIAÇÃO E DESEMPENHO 2022.2/TRAB FINAL/main.py"
Estatisticas a respeito de W1:
        \ esperança: 0.11214790343904636
        \ variancia: 0.23762170831278456
        \ desvio padrão: 0.48746457134112275
        \ intervalo de confiança para média: (0.11052598071853657, 0.11376965168320809), valor médio 0.0016218354823357567, precisão: 0.01446158772660204
        \ intervalo de confiança para variancia: (0.0019367955400278677, 0.0019613347459450136) valor médio 1.226960295857291e-05, precisão:0.00629512205003723
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 0.527148614522155
        \ variancia: 1.484433822821138
        \ desvio padrão: 1.2183734332384049
        \ intervalo de confiança para média: (0.5212494142026638, 0.533047300732185), valor médio 0.005898943264760592, precisão: 0.011190290515369997
        \ intervalo de confiança para variancia: (0.08160086907197489, 0.08263475235381393) valor médio 0.0005169416409195188, precisão:0.0062951220500371535
------------------------------
Estatisticas a respeito de W:
        \ esperança: 0.6392965179612011
        \ variancia: 2.0817004676956694
        \ desvio padrão: 1.4428099208473961
------------------------------
Estatisticas a respeito de S1:
        \ esperança: 0.9993751208038042
        \ variancia: 0.996518154276011
        \ desvio padrão: 0.9982575590878393
------------------------------
Estatisticas a respeito de S2:
        \ esperança: 0.9976267644262515
        \ variancia: 0.9960016420685063
        \ desvio padrão: 0.9979988186708971
------------------------------
Estatisticas a respeito de S:
        \ esperança: 1.9970018852300562
        \ variancia: 1.990805695408507
        \ desvio padrão: 1.4109591402335175
------------------------------
Estatisticas a respeito de T1:
        \ esperança: 1.1115230242428507
        \ variancia: 1.235319111387193
        \ desvio padrão: 1.1114491042720729
        \ intervalo de confiança para média: (1.1079546724287166, 1.115091226821363), valor médio 0.003568277196323244, precisão: 0.0032102595790100092
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 1.5247753789484062
        \ variancia: 2.7005085578099663
        \ desvio padrão: 1.6433224144427552
        \ intervalo de confiança para média: (1.5176056946930405, 1.5319448926759893), valor médio 0.007169598991474402, precisão: 0.004702069230246745
------------------------------
Estatisticas a respeito de T:
        \ esperança: 2.6362984031912577
        \ variancia: 4.516075602694339
        \ desvio padrão: 2.1251060215185356
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.040996061974752536
        \ variancia: 0.048517915806650276
        \ desvio padrão: 0.22026782744343368
        \ intervalo de confiança para média: (0.040542736701368494, 0.04144935438907362), valor médio 0.0004533088438525637, precisão: 0.011057379750262431
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 0.19443788204123988
        \ variancia: 0.2856982216720536
        \ desvio padrão: 0.5345074570780595
        \ intervalo de confiança para média: (0.1925631533401479, 0.19631242748111388), valor médio 0.0018746370704829929, precisão: 0.009641320581374478
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.40776031886863
        \ variancia: 0.3326864961036238
        \ desvio padrão: 0.5767898196948553
        \ intervalo de confiança para média: (0.40706101285458496, 0.4084596098058926), valor médio 0.000699298475653809, precisão: 0.001714974351899241
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 0.5612295551973941
        \ variancia: 0.5696613379336493
        \ desvio padrão: 0.7547591257703674
        \ intervalo de confiança para média: (0.5591544158529941, 0.5633044464766398), valor médio 0.0020750153118228587, precisão: 0.0036972674571185958
------------------------------
Estatisticas a respeito de N:
        \ esperança: 0.9689898740660242
        \ variancia: 0.6714595372107067
        \ desvio padrão: 0.8194263464221215
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.20030717905567058
        \ variancia: 1.8990279644591672e-05
        \ desvio padrão: 0.004357783799661437
------------------------------
````



Para $\rho = 0.4$

````
Estatisticas a respeito de W1:
        \ esperança: 0.25054283215457396
        \ variancia: 0.5587423718727579
        \ desvio padrão: 0.7474907169141018
        \ intervalo de confiança para média: (0.2473553820530371, 0.2537294005953217), valor médio 0.0031870092711422937, precisão: 0.012720439260989529
        \ intervalo de confiança para variancia: (0.00829833683883108, 0.008403476794107401) valor médio 5.2569977638161104e-05, precisão:0.006295122050037155
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 1.5151607451172087
        \ variancia: 6.534323263253011
        \ desvio padrão: 2.556232239694393
        \ intervalo de confiança para média: (1.4974280113221077, 1.532889755687951), valor médio 0.017730872182921686, precisão: 0.011702318731026225
        \ intervalo de confiança para variancia: (2.243252446204253, 2.2716744621392726) valor médio 0.014211007967509737, precisão:0.006295122050037169  
------------------------------
Estatisticas a respeito de W:
        \ esperança: 1.7657035772717833
        \ variancia: 8.386391644886498
        \ desvio padrão: 2.8959267333422813
------------------------------
Estatisticas a respeito de S1:
        \ esperança: 0.9999759746455195
        \ variancia: 0.9963879276596236
        \ desvio padrão: 0.9981923299943872
------------------------------
Estatisticas a respeito de S2:
        \ esperança: 0.998694302059508
        \ variancia: 0.995122111792897
        \ desvio padrão: 0.9975580743961211
------------------------------
Estatisticas a respeito de S:
        \ esperança: 1.9986702767050273
        \ variancia: 1.993522858908615
        \ desvio padrão: 1.4119216900765477
------------------------------
Estatisticas a respeito de T1:
        \ esperança: 1.2505188068000936
        \ variancia: 1.5571716361556487
        \ desvio padrão: 1.2478668343039048
        \ intervalo de confiança para média: (1.245437210425607, 1.255598537937646), valor médio 0.0050806637560194545, precisão: 0.004062847769644541
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 2.513855047176717
        \ variancia: 8.037166231134295
        \ desvio padrão: 2.83498963510174
        \ intervalo de confiança para média: (2.494963939091635, 2.532741661706681), valor médio 0.018888861307523097, precisão: 0.007513909050093887
------------------------------
Estatisticas a respeito de T:
        \ esperança: 3.764373853976809
        \ variancia: 11.411248080801998
        \ desvio padrão: 3.3780538895645225
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.10033906174446772
        \ variancia: 0.1406865186083874
        \ desvio padrão: 0.3750820158423853
        \ intervalo de confiança para média: (0.09929449317319454, 0.10138355816580817), valor médio 0.0010445324963068159, precisão: 0.01041003228143073
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 0.6033269230657061
        \ variancia: 1.366854042403551
        \ desvio padrão: 1.1691253322050426
        \ intervalo de confiança para média: (0.597114025465766, 0.6095391193561591), valor médio 0.006212546945196573, precisão: 0.010297154525070094
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.5003928403318407
        \ variancia: 0.5010933533410894
        \ desvio padrão: 0.7078794765644003
        \ intervalo de confiança para média: (0.49896811859149887, 0.5018175012819838), valor médio 0.0014246913452424514, precisão: 0.002847145916070533
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 1.0033894508809598
        \ variancia: 1.7274693114421422
        \ desvio padrão: 1.3143322682800351
        \ intervalo de confiança para média: (0.9969585573393587, 1.009819559324814), valor médio 0.0064305009927276835, precisão: 0.006408781259202664
------------------------------
Estatisticas a respeito de N:
        \ esperança: 1.5037822912128005
        \ variancia: 2.0420118812955104
        \ desvio padrão: 1.4289898114736543
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.40006861194061405
        \ variancia: 7.751072779090196e-05
        \ desvio padrão: 0.008804017707325557
------------------------------
````



Para $\rho = 0.6$

```
Estatisticas a respeito de W1:
        \ esperança: 0.42849023787583934
        \ variancia: 1.0259774972807547
        \ desvio padrão: 1.0129054730233986
        \ intervalo de confiança para média: (0.42348310964559593, 0.4334975566195349), valor médio 0.00500722348696947, precisão: 0.01168573267537484
        \ intervalo de confiança para variancia: (0.028117949146030573, 0.028474203654987332) valor médio 0.0001781272544783795, precisão:0.006295122050037141
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 3.62519389659961
        \ variancia: 25.0814458128212
        \ desvio padrão: 5.00813795864503
        \ intervalo de confiança para média: (3.564987988697899, 3.685407496027155), valor médio 0.060209753664627996, precisão: 0.01660868122062482
        \ intervalo de confiança para variancia: (64.94428074860937, 65.76712500113594) valor médio 0.41142212626328245, precisão:0.006295122050037076    
------------------------------
Estatisticas a respeito de W:
        \ esperança: 4.053684134475451
        \ variancia: 29.433585755114837
        \ desvio padrão: 5.4252728737930624
------------------------------
Estatisticas a respeito de S1:
        \ esperança: 1.0008310772277327
        \ variancia: 1.0000136900164198
        \ desvio padrão: 1.000006844984783
------------------------------
Estatisticas a respeito de S2:
        \ esperança: 1.0012707287771245
        \ variancia: 1.007275518858425
        \ desvio padrão: 1.0036311667432538
------------------------------
Estatisticas a respeito de S:
        \ esperança: 2.0021018060048577
        \ variancia: 2.009832754425394
        \ desvio padrão: 1.4176857036823762
------------------------------
Estatisticas a respeito de T1:
        \ esperança: 1.429321315103572
        \ variancia: 2.022759236323057
        \ desvio padrão: 1.4222374050498943
        \ intervalo de confiança para média: (1.4223864630990235, 1.4362570358283486), valor médio 0.006935286364662563, precisão: 0.0048521519855587725
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 4.626464625376734
        \ variancia: 26.939001581821806
        \ desvio padrão: 5.1902795282934235
        \ intervalo de confiança para média: (4.565840706271486, 4.687097545205799), valor médio 0.06062841946715647, precisão: 0.013104684764858727
------------------------------
Estatisticas a respeito de T:
        \ esperança: 6.055785940480307
        \ variancia: 33.13233282836482
        \ desvio padrão: 5.756069216780217
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.185187129284552
        \ variancia: 0.30817943806365894
        \ desvio padrão: 0.5551391159553243
        \ intervalo de confiança para média: (0.18323701930579667, 0.18713710710987802), valor médio 0.0019500439020406768, precisão: 0.01053013028157438
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 1.5661825859243317
        \ variancia: 5.834680807003215
        \ desvio padrão: 2.4155083951423593
        \ intervalo de confiança para média: (1.5420004176957947, 1.5903671286031442), valor médio 0.024183355453674782, precisão: 0.015440943692734093
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.6185968657230009
        \ variancia: 0.763595623641545
        \ desvio padrão: 0.8738395869045674
        \ intervalo de confiança para média: (0.616187662206673, 0.6210058252960203), valor médio 0.0024090815446736746, precisão: 0.0038944297217995663
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 1.9993222869607312
        \ variancia: 6.289301356299437
        \ desvio padrão: 2.507847953186045
        \ intervalo de confiança para média: (1.9749370796183643, 2.023709968840893), valor médio 0.02438644461126438, precisão: 0.012197347910794411
------------------------------
Estatisticas a respeito de N:
        \ esperança: 2.617919152683732
        \ variancia: 7.029756531854815
        \ desvio padrão: 2.651368803439992
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.5999084558480154
        \ variancia: 0.0001425018807880795
        \ desvio padrão: 0.011937415163597163
------------------------------
```

`

Para $\rho = 0.8$

````
Estatisticas a respeito de W1:
        \ esperança: 0.6636711085886786
        \ variancia: 1.7790558734972948
        \ desvio padrão: 1.3338125331159902
        \ intervalo de confiança para média: (0.654426818814131, 0.672913802329541), valor médio 0.009243491757705002, precisão: 0.013927836774467978
        \ intervalo de confiança para variancia: (0.16352566720618017, 0.1655975379521513) valor médio 0.0010359353729855608, precisão:0.006295122050037176
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 10.469308045739998
        \ variancia: 155.2082801510165
        \ desvio padrão: 12.458261522018892
        \ intervalo de confiança para média: (10.17269436264265, 10.765906141784692), valor médio 0.29660588957102085, precisão: 0.02833101376649364
        \ intervalo de confiança para variancia: (7471.049130475211, 7565.707347742277) valor médio 47.329108633533, precisão:0.006295122050037158        
------------------------------
Estatisticas a respeito de W:
        \ esperança: 11.132979154328677
        \ variancia: 165.17590288015722
        \ desvio padrão: 12.8520777650992
------------------------------
Estatisticas a respeito de S1:
        \ esperança: 1.00086963009365
        \ variancia: 0.996165396474282
        \ desvio padrão: 0.9980808566816027
------------------------------
Estatisticas a respeito de S2:
        \ esperança: 1.0014678704528128
        \ variancia: 1.0019509751852476
        \ desvio padrão: 1.0009750122681622
------------------------------
Estatisticas a respeito de S:
        \ esperança: 2.0023375005464623
        \ variancia: 2.0000271941996886
        \ desvio padrão: 1.414223176941917
------------------------------
Estatisticas a respeito de T1:
        \ esperança: 1.664540738682329
        \ variancia: 2.7749409847893474
        \ desvio padrão: 1.6658154113794683
        \ intervalo de confiança para média: (1.6535279725714964, 1.6755521308440826), valor médio 0.011012079136293096, precisão: 0.006615688895556999
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 11.470775916192814
        \ variancia: 157.5657625414545
        \ desvio padrão: 12.55252016694076
        \ intervalo de confiança para média: (11.17368582201329, 11.767850180527038), valor médio 0.29708217925687386, precisão: 0.02589906615005881
------------------------------
Estatisticas a respeito de T:
        \ esperança: 13.13531665487514
        \ variancia: 169.79747513106523
        \ desvio padrão: 13.030636021739891
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.30855172952756205
        \ variancia: 0.6219815796752698
        \ desvio padrão: 0.788658087941327
        \ intervalo de confiança para média: (0.3047277041918162, 0.3123754160096803), valor médio 0.003823855908932028, precisão: 0.012392923593332222
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 4.881077228766769
        \ variancia: 37.938442699027796
        \ desvio padrão: 6.1594190228484855
        \ intervalo de confiança para média: (4.747561795548828, 5.014587180456072), valor médio 0.13351269245362207, precisão: 0.027353135622452122
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.7744735250565856
        \ variancia: 1.2004017630402932
        \ desvio padrão: 1.0956284785639214
        \ intervalo de confiança para média: (0.770111614743027, 0.7788349444347101), valor médio 0.004361664845841551, precisão: 0.00563178221998434
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 5.3483258187196405
        \ variancia: 38.52010628440496
        \ desvio padrão: 6.206456822084961
        \ intervalo de confiança para média: (5.214541574172389, 5.482104566625435), valor médio 0.1337814962265229, precisão: 0.0250137275676102
------------------------------
Estatisticas a respeito de N:
        \ esperança: 6.122799343776226
        \ variancia: 40.171642579063146
        \ desvio padrão: 6.3381103318783545
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.7998739509190008
        \ variancia: 0.0002858805119800546
        \ desvio padrão: 0.016908001418856535
````



Para $\rho = 0.9$

````
Estatisticas a respeito de W1:
        \ esperança: 0.8174345419915034
        \ variancia: 2.266702791427239
        \ desvio padrão: 1.5055573026049984
        \ intervalo de confiança para média: (0.8068323623249047, 0.8280351589293462), valor médio 0.010601398302220733, precisão: 0.012969122163595819
        \ intervalo de confiança para variancia: (0.1920874540455164, 0.1945212027254908) valor médio 0.0012168743399872117, precisão:0.00629512205003718 
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 25.545569914780753
        \ variancia: 789.7460377739973
        \ desvio padrão: 28.10242049671162
        \ intervalo de confiança para média: (24.25603949975678, 26.83483357931457), valor médio 1.289397039778894, precisão: 0.05047465279300843
        \ intervalo de confiança para variancia: (357041.7549716774, 361565.47519159433) valor médio 2261.8601099584776, precisão:0.00629512205003718     
------------------------------
Estatisticas a respeito de W:
        \ esperança: 26.36300445677225
        \ variancia: 805.0248375984473
        \ desvio padrão: 28.37295962000523
------------------------------
Estatisticas a respeito de S1:
        \ esperança: 1.0001071172472393
        \ variancia: 0.996334601938094
        \ desvio padrão: 0.9981656184912873
------------------------------
Estatisticas a respeito de S2:
        \ esperança: 0.9994380210797946
        \ variancia: 1.000838814586244
        \ desvio padrão: 1.0004193193787512
------------------------------
Estatisticas a respeito de S:
        \ esperança: 1.9995451383270337
        \ variancia: 2.001098331106286
        \ desvio padrão: 1.4146018277615389
------------------------------
Estatisticas a respeito de T1:
        \ esperança: 1.8175416592387428
        \ variancia: 3.258881580091405
        \ desvio padrão: 1.805237264209723
        \ intervalo de confiança para média: (1.8050776117195384, 1.8300039406877349), valor médio 0.012463164484098233, precisão: 0.006857158115665772
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 26.545007935860543
        \ variancia: 792.4814000398567
        \ desvio padrão: 28.15104616244051
        \ intervalo de confiança para média: (25.254534135198377, 27.835214962765072), valor médio 1.2903404137833476, precisão: 0.04860977630172473
------------------------------
Estatisticas a respeito de T:
        \ esperança: 28.362549595099274
        \ variancia: 810.3375906962132
        \ desvio padrão: 28.46642918766267
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.3946557495597
        \ variancia: 0.8739796268174561
        \ desvio padrão: 0.9348687751858311
        \ intervalo de confiança para média: (0.39000208779811524, 0.39930884310882214), valor médio 0.004653377655353452, precisão: 0.011790987488306056
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 12.168836091769014
        \ variancia: 190.1530029410127
        \ desvio padrão: 13.789597635210852
        \ intervalo de confiança para média: (11.60316222347459, 12.734391172972936), valor médio 0.5656144747491734, precisão: 0.04648079990092466
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.8775680278059648
        \ variancia: 1.5318309214163992
        \ desvio padrão: 1.237671572516877
        \ intervalo de confiança para média: (0.8723674840015351, 0.8827679397862161), valor médio 0.0052002278923405365, precisão: 0.005925728376124897
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 12.652318718872833
        \ variancia: 190.81477036213863
        \ desvio padrão: 13.81357196246281
        \ intervalo de confiança para média: (12.086291210139686, 13.218227291269406), valor médio 0.5659680405648597, precisão: 0.044732567468797606
------------------------------
Estatisticas a respeito de N:
        \ esperança: 13.529886746678796
        \ variancia: 193.27610446132127
        \ desvio padrão: 13.90237765496684
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.8974675244682351
        \ variancia: 0.0003375086964232002
        \ desvio padrão: 0.018371409756009476
------------------------------
````

​	Analisando os resultados obtidos é evidente o aumento de algumas métricas com o aumento da utilização do servidor, alinhado com o esperado, uma vez que mais tempo ocupado significa mais tempos de espera e mais pessoas no sistema. Em contra partida o tempo de serviço como independe do tempo ocupado permanece estável para todas as simulações.  Também observamos o aumento da variâncias e desvio padrão das métricas corroborando com nossa análise anterior.

​	

# Otimização



Porém em função do controle do intervalo de confiança que perdia precisão com um número menor de fregueses por rodada para estabilidade encontramos o valor de 2000 fregueses que satisfaz o intervalo para todos os valores de $\rho$ porem para $\rho = 0.6$ em específico conseguimos construir os IC com 5% de precisão utilizando um número menor de rodadas e coletas, os valores para  $\rho = 0.6$  se comportaram de forma mais calma em relação ao número de coletas

![W1freg0.6](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W1freg0.6.png)

![W2freg0.6](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W2freg0.6.png)

​																											**_Imagens para $\rho=0.6$_**



​	Tendo as médias atingindo estabilidade por volta da x=30 ou da 1500° coleta.  A repseito da fase transiente observando as métricas de W1, W2 e N para diferentes quantidades de rodadas descartadas podemos observar que para uma amostra de 500 coletas, percebemos que as médias se aproximas das médias de longo prazo em torno da 350° coleta, logo as primeiras 350 podem ser descartadas para melhor avaliação das métricas

![W1transiente0.6](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W1transiente0.6.png)

![W2transiente0.6](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\W2transiente0.6.png)

![Ntransiente0.6](C:\Users\Bruno Trotti\Documents\FACULDADE\AVALIAÇÃO E DESEMPENHO 2022.2\TRAB FINAL\img\Ntransiente0.6.png)



Por fim simulando uma fila com $\rho=0.6$, 1500 coletas por rodada e e 100 rodadas obtemos os seguintes resultados 

```
Estatisticas a respeito de W1:
        \ esperança: 0.42089571167015155
        \ variancia: 0.9746875898016587
        \ desvio padrão: 0.9872626751790319
        \ intervalo de confiança para média: (0.40777896369228517, 0.4340105643255536), valor médio 0.01311580031663423, precisão: 0.031161709382434337   
        \ intervalo de confiança para variancia: (0.037361481785860094, 0.03832575155427039) valor médio 0.0004821348842051487, precisão:0.012740190463522035
------------------------------
Estatisticas a respeito de W2:
        \ esperança: 3.6064031404971
        \ variancia: 24.859175337619025
        \ desvio padrão: 4.985897646123417
        \ intervalo de confiança para média: (3.48686858333315, 3.7260138532130664), valor médio 0.11957263493995818, precisão: 0.033155298451589287      
        \ intervalo de confiança para variancia: (55.192587972928045, 56.617064237752274) valor médio 0.7122381324121143, precisão:0.012740190463522068   
------------------------------
Estatisticas a respeito de W:
        \ esperança: 4.0272988521672515
        \ variancia: 28.99427764279719
        \ desvio padrão: 5.384633473394191
------------------------------
Estatisticas a respeito de S1:
        \ esperança: 0.9991936380826365
        \ variancia: 0.9972750829963135
        \ desvio padrão: 0.9986366120848532
------------------------------
Estatisticas a respeito de S2:
        \ esperança: 0.9969067406974236
        \ variancia: 0.9866056515703439
        \ desvio padrão: 0.993280248253404
------------------------------
Estatisticas a respeito de S:
        \ esperança: 1.99610037878006
        \ variancia: 1.9827494311543574
        \ desvio padrão: 1.4081013568469982
------------------------------
Estatisticas a respeito de T1:
        \ esperança: 1.420089349752788
        \ variancia: 1.9600417111618065
        \ desvio padrão: 1.4000148967642474
        \ intervalo de confiança para média: (1.4013366198072437, 1.4388357684826063), valor médio 0.01874957433768132, precisão: 0.013203124158932465    
------------------------------
Estatisticas a respeito de T2:
        \ esperança: 4.603309881194524
        \ variancia: 26.71937228886702
        \ desvio padrão: 5.169078475789183
        \ intervalo de confiança para média: (4.481629396422371, 4.725069947333307), valor médio 0.12172027545546804, precisão: 0.02644167489579709       
------------------------------
Estatisticas a respeito de T:
        \ esperança: 6.0233992309473114
        \ variancia: 32.684049530837676
        \ desvio padrão: 5.716996548086913
------------------------------
Estatisticas a respeito de Nq1:
        \ esperança: 0.18424640803002376
        \ variancia: 0.30632551801773217
        \ desvio padrão: 0.5534668174495488
        \ intervalo de confiança para média: (0.17907166375610992, 0.18942128018411572), valor médio 0.005174808214002902, precisão: 0.028086335432476142
------------------------------
Estatisticas a respeito de Nq2:
        \ esperança: 1.560791454775599
        \ variancia: 5.65104335663325
        \ desvio padrão: 2.3771923263870027
        \ intervalo de confiança para média: (1.5098581341430377, 1.6117583390859227), valor médio 0.05095010247144249, precisão: 0.03264340953374093     
------------------------------
Estatisticas a respeito de N1:
        \ esperança: 0.6170016211054606
        \ variancia: 0.7608292855784166
        \ intervalo de confiança para média: (0.6106927915002315, 0.62331041007763), valor médio 0.0063088092886992575, precisão: 0.0102249480076429      
------------------------------
Estatisticas a respeito de N2:
        \ esperança: 1.9942395238835469
        \ variancia: 6.105516327252235
        \ desvio padrão: 2.47093430249617
        \ intervalo de confiança para média: (1.942445129742516, 2.0460684924523544), valor médio 0.0518116813549192, precisão: 0.025980445981983305      
------------------------------
Estatisticas a respeito de N:
        \ esperança: 2.6112411449890076
        \ variancia: 6.832078118016624
        \ desvio padrão: 2.6138244237164483
        \ intervalo de confiança para média: (2.5558521460889505, 2.666664677683781), valor médio 0.055406265797415255, precisão: 0.021218223958688914    
------------------------------
Estatisticas a respeito de rho:
        \ esperança: 0.5974694868851606
        \ variancia: 0.00029713749540638475
        \ desvio padrão: 0.01723767662437095
------------------------------
```

Obtendo assim o Fator Mínimo= 1500*50 + 320 = 75320 e levando 6.685999393463135 segundos para execução do programa em uma máquina Windows com Intel Core i3-9100F e 16Gb de ram.

# Conclusões

Por fim, o desenvolvimento do simulador deu bastante trabalho principalmente para implementação da segunda fila e realização da corretude. Ter certeza do funcionamento perfeito sem o auxilio de formulas analíticas é bem complicado principalmente pela grande volatilidade da fila 2, o fator velocidade da linguagem também foi um empecilho pois gerava demora para alguns testes, sendo esse talvez uma melhora óbvia que poderia ser feita, implementar o programa em uma linguagem mais rápida como java ou C++.

​	Fiquei bem satisfeito com o método de coleta dentro das rodadas e achei bem eficiente  em questão de número de coletas, porém a manutenção de uma instancia em memória para cada freguês com suas próprias estatísticas com certeza é sacrifício de eficiência em nome de uma implementação mais limpa e fácil, apesar de limparmos os fregueses entre rodadas para liberar memória de forma automática graças aos mecanismos da linguagem, uma possivel melhora era também a remoção de fregueses durante o processo na medida que eles deixam o sistema. Além disso a forma de coleta de estatísticas entre rodadas provavelmente pode ser melhorada, fazer a iteração completa por todos os resultados da rodada adiciona uma complexidade n ao algoritmo que talvez se fosse feito de forma simultânea à simulação da rodada ou de forma acumulativa não geraria essa complexidade.

​	Por fim foi um trabalho bem interessante de se desenvolver e muito bom de ver as aplicações práticas do conteúdo aprendido, uma ótima forma de realmente exercitar as competências desenvolvidas durante o curso.

