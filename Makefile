# Makefile para o projeto de Agente de Portais de Transparência

# Variáveis
IMAGE_NAME = transparency-portal
CONTAINER_NAME = transparency-agent
PORT = 8501

# Cores para output
GREEN = \033[0;32m
YELLOW = \033[0;33m
RED = \033[0;31m
NC = \033[0m # No Color

# Comandos principais
.PHONY: help build run stop restart logs shell clean status all

# Comando padrão - mostra ajuda
help:
	@echo "${GREEN}=== Makefile para Agente de Portais de Transparência ===${NC}"
	@echo ""
	@echo "${YELLOW}Comandos disponíveis:${NC}"
	@echo "  ${GREEN}make build${NC}    - Constrói a imagem Docker"
	@echo "  ${GREEN}make run${NC}      - Inicia o container (constrói a imagem se necessário)"
	@echo "  ${GREEN}make stop${NC}     - Para a execução do container"
	@echo "  ${GREEN}make restart${NC}  - Reinicia o container"
	@echo "  ${GREEN}make logs${NC}     - Exibe os logs do container"
	@echo "  ${GREEN}make shell${NC}    - Abre um shell dentro do container"
	@echo "  ${GREEN}make status${NC}   - Verifica o status do container"
	@echo "  ${GREEN}make clean${NC}    - Remove o container e a imagem"
	@echo "  ${GREEN}make all${NC}      - Constrói e executa o container"
	@echo ""
	@echo "${YELLOW}Acesso:${NC}"
	@echo "  A aplicação estará disponível em: http://localhost:${PORT}"

# Constrói a imagem Docker
build:
	@echo "${GREEN}Construindo a imagem Docker...${NC}"
	docker build -t $(IMAGE_NAME) .

# Verifica se a imagem existe, caso contrário constrói
ensure-image:
	@if [ -z "$(shell docker images -q $(IMAGE_NAME) 2>/dev/null)" ]; then \
		echo "${YELLOW}Imagem não encontrada. Construindo...${NC}"; \
		$(MAKE) build; \
	fi

# Inicia o container
run: ensure-image
	@echo "${GREEN}Iniciando o container...${NC}"
	@if [ -z "$(shell docker ps -a -q -f name=$(CONTAINER_NAME) 2>/dev/null)" ]; then \
		docker run -d --name $(CONTAINER_NAME) -p $(PORT):$(PORT) $(IMAGE_NAME); \
		echo "${GREEN}Container iniciado em http://localhost:${PORT}${NC}"; \
	else \
		echo "${YELLOW}Container já existe. Use 'make restart' ou 'make stop' e depois 'make run'.${NC}"; \
		$(MAKE) status; \
	fi

# Para a execução do container
stop:
	@echo "${YELLOW}Parando o container...${NC}"
	@if [ -n "$(shell docker ps -q -f name=$(CONTAINER_NAME) 2>/dev/null)" ]; then \
		docker stop $(CONTAINER_NAME); \
		echo "${GREEN}Container parado.${NC}"; \
	else \
		echo "${YELLOW}Container não está em execução.${NC}"; \
	fi

# Reinicia o container
restart:
	@echo "${YELLOW}Reiniciando o container...${NC}"
	@if [ -n "$(shell docker ps -a -q -f name=$(CONTAINER_NAME) 2>/dev/null)" ]; then \
		docker restart $(CONTAINER_NAME); \
		echo "${GREEN}Container reiniciado em http://localhost:${PORT}${NC}"; \
	else \
		echo "${YELLOW}Container não existe. Criando novo...${NC}"; \
		$(MAKE) run; \
	fi

# Exibe os logs do container
logs:
	@if [ -n "$(shell docker ps -a -q -f name=$(CONTAINER_NAME) 2>/dev/null)" ]; then \
		docker logs -f $(CONTAINER_NAME); \
	else \
		echo "${RED}Container não existe.${NC}"; \
	fi

# Abre um shell dentro do container
shell:
	@if [ -n "$(shell docker ps -q -f name=$(CONTAINER_NAME) 2>/dev/null)" ]; then \
		docker exec -it $(CONTAINER_NAME) /bin/bash || docker exec -it $(CONTAINER_NAME) /bin/sh; \
	else \
		echo "${RED}Container não está em execução.${NC}"; \
	fi

# Verifica o status do container
status:
	@if [ -n "$(shell docker ps -q -f name=$(CONTAINER_NAME) 2>/dev/null)" ]; then \
		echo "${GREEN}Container está em execução em http://localhost:${PORT}${NC}"; \
	elif [ -n "$(shell docker ps -a -q -f name=$(CONTAINER_NAME) 2>/dev/null)" ]; then \
		echo "${YELLOW}Container existe mas não está em execução.${NC}"; \
	else \
		echo "${RED}Container não existe.${NC}"; \
	fi

# Remove o container e a imagem
clean: stop
	@echo "${YELLOW}Removendo o container...${NC}"
	@if [ -n "$(shell docker ps -a -q -f name=$(CONTAINER_NAME) 2>/dev/null)" ]; then \
		docker rm $(CONTAINER_NAME); \
		echo "${GREEN}Container removido.${NC}"; \
	else \
		echo "${YELLOW}Container não existe.${NC}"; \
	fi
	
	@echo "${YELLOW}Removendo a imagem...${NC}"
	@if [ -n "$(shell docker images -q $(IMAGE_NAME) 2>/dev/null)" ]; then \
		docker rmi $(IMAGE_NAME); \
		echo "${GREEN}Imagem removida.${NC}"; \
	else \
		echo "${YELLOW}Imagem não existe.${NC}"; \
	fi

# Constrói e executa o container (tudo de uma vez)
all: build run
	@echo "${GREEN}Projeto construído e em execução em http://localhost:${PORT}${NC}"