# Case Twitter
1. Coletar últimas mensagens no twitter dada uma #tag
	1. pip module requests, json
2. Base de dados para armazenar informacões
	1. SQLite3
3. Processar os dados com python
	1. 5 usuários da amostra com mais seguidores
	2. Total de postagens agrupadas por hora
	3. Total de postagens para cada tag por idioma/país do usuário que postou
4. API REST
	1. Flask
5. Postman
6. Logging
	1. standard library logging
	2. elastic search
7. Monitoring
	1. Prometheus and kibana
8. Docs - README.md no Github
	- Projeto
	- APIs
	- Arquitetura
	- Deploy
	- Logs e dashboards
9. Django for the interface

# Plano de desenvolvimento

## Fase 1
### Aplicacão básica
* Capacidade de recuperar dados da API do Twitter
* Capacidade de responder RESTful requests
* Escrever dados no SQLite
* Escrever logs

* Dockerfile com aplicacao
* Mapear volume com logs
* Mapear volume com sqlite
* Configurar interfaces de rede do container

### Logging
* Container do elastic search com docker compose
    * Se necessário, escrever dockerfile

* Configuracão do filebeats
* Configuracão do elastic search

### Monitoring
* Container do Kibana com docker compose
    * Se necessário, escrever dockerfile
 
* Métricas do prometheus mais básicas dentro da aplicacão
* Container do Prometheus com docker compose
    * Se necessário, escrever dockerfile
* Configurar Kibana com timelion para consumir dados do Prometheus

## Fase 2
### Aplicacão
* Processamento dos dados do Twitter
* API RESTful completa
* Melhorar logs de acordo com nível de verbosidade
* Métricas do prometheus para erros, latência e volume

### Logging e monitoramento
* Dashboards para logs, com as queries necessárias
* Dashboards para métricas, com as queries necessárias

### Outros
* Colecão do Postman
* Persistência dos containers *stateful*
* Refinar docker-compose e dockerfiles
* Script all-in-one para criar e configurar todas as dependências

## Fase 3 (adicionais)
* Front-end (django)
* Database SQL relacional a parte
* Cloud implementation
