# SRE Case - Py-Twit
Colete as últimas postagens do Twitter, dado o seguinte conjunto de tags.
```text
#openbanking, #remediation, #devops, #sre, #microservices, #observability, #oauth, #metrics, #logmonitoring, #opentracing
```
Obtenha os dados sumarizados sobre usuários e postagens por hora e por local/idioma através da API fornecida.

## Código
Escrito em Python, usando as bibliotecas [flask](https://flask.palletsprojects.com/en/1.1.x/),
[request](https://requests.readthedocs.io/en/master/user/quickstart/), 
[sqlite3](https://docs.python.org/3/library/sqlite3.html),
[logging](https://docs.python.org/3/library/logging.html) e 
[prometheus_client](https://github.com/prometheus/client_python).

## Logging
Logs gerados pela biblioteca padrão do Python e enviados para um
[elastic search](https://medium.com/@bcoste/powerful-logging-with-docker-filebeat-and-elasticsearch-8ad021aecd87)
usando [filebeats](https://www.elastic.co/guide/en/beats/filebeat/current/load-kibana-dashboards.html).
Estatísticas básicas podem ser obtidas usando queries no Kibana com a
[lucene syntax](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html) ou
[query DSL](https://lucene.apache.org/core/2_9_4/queryparsersyntax.html).

## Métricas
Métricas sobre a aplicacão serão exportadas usando o formato do
[Prometheus](https://prometheus.io/).
Para as métricas temporais, posso usar o plugin do timelion para o
[prometheus](https://github.com/lmangani/timelion-prometheus) e utilizar nova o Kibana para montar dashboards.

## Facilidade de Deploy
A aplicacão deverá rodar, com containers individuais para cada componotente da infraestrutura,
sendo coordenada por um arquivo de configuracão do docker-compose.
Dependências extras devem ser resolvidas usando um simples script bash.