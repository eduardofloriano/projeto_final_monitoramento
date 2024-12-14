# Montoramento de Sistemas - Projeto Final

Neste projeto final vocês podem formar as mesmas equipes do proejto anterior.
A ideia é configurar um serviço de monitoramento ativo e passivo para uma aplicação backend!

Monitoramento Passivo - Usando o Prometheus e Grafana
Monitoramento Ativo - Usando o JMeter

1) Elaborar um repositório para monitoramento ativo contendo

 - Uma instância do Prometheus
 - Uma instância do Loki
 - Uma instância do Grafana
 - Uma aplicação Flask realizando operações CRUD em uma tabela de BD (GET, POST e DELETE)
 - Monitoramento da aplicação com o módulo do Prometheus (metrics)
 - Logs da aplicação com o módulo de logs do Python

 Vocês podem se basear no repositório: https://github.com/gmcalixto/flask_loki

Além da elaboração do projeto, devem ser coletadas as seguintes evidências (pode ser por prints e depois enviado ao repositório)
 - Geração de logs
 - Explore ou Dashbord de uma das métricas enviadas pelo Prometheus.
 - Explore ou Dashboard de uma das métricas geradas pelo Loki.

2) Elaborar um repositório com monitoramento passivo com JMeter contendo

 - Uma instância do JMeter
 - Script de teste testando um endpoint GET da aplicação Flask com 1 thread e 100 requisições, com espaço de 10 milisegundos por disparo. 
 - Script de teste testando um endpoint GET da aplicação Flask com 100 thread e 100 requisições, com espaço de 10 milisegundos por disparo.
 - Script de teste testando um endpoint POST da aplicação Flask com 100 thread e 100 requisições, com espaço de 10 milisegundos por disparo.

Abrir o resultado de cada teste, capturar três gráficos e adicionar ao repositório.


  - Vocês podem se basear no repositório https://github.com/gmcalixto/jmeterdevops


  Toda entrega deve ser realizada em um único repositório do grupo.
