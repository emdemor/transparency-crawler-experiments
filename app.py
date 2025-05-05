import random
import time

import pandas as pd
import streamlit as st


class MockTransparencyAgent:
    """Versão simulada do agente de transparência para demonstração da interface."""

    def search_transparency_portal(self, city, state):
        """Simula a busca por portais de transparência."""
        # Simulando um tempo de processamento
        with st.spinner(f"Buscando portais de transparência para {city}/{state}..."):
            time.sleep(2)

        # Gera URLs fictícias baseadas na cidade e estado
        mock_urls = [
            f"https://transparencia.{city.lower()}.{state.lower()}.gov.br",
            f"https://www.{city.lower()}.{state.lower()}.gov.br/transparencia",
            f"https://portal.{city.lower()}.{state.lower()}.gov.br/dadosabertos",
            f"https://www.transparencia.{state.lower()}.gov.br/{city.lower()}",
        ]
        return mock_urls

    def analyze_pages(self, urls):
        """Simula a análise das páginas encontradas."""
        results = []
        with st.spinner("Analisando páginas encontradas..."):
            for url in urls:
                # Simular um tempo de processamento para cada URL
                time.sleep(1)

                # Gerar categorias aleatórias de dados disponíveis
                categories = random.sample(
                    [
                        "Licitações",
                        "Contratos",
                        "Despesas",
                        "Receitas",
                        "Servidores",
                        "Diárias",
                        "Orçamento",
                        "Convênios",
                    ],
                    k=random.randint(3, 6),
                )

                results.append(
                    {
                        "url": url,
                        "title": f"Portal de Transparência - {url.split('//')[1].split('.')[0].capitalize()}",
                        "categories": categories,
                        "last_update": f"{random.randint(1, 28)}/{random.randint(1, 12)}/2024",
                        "data_format": random.choice(
                            ["CSV", "XLS", "PDF", "XLSX", "JSON"]
                        ),
                    }
                )
        return results

    def download_data(self, selected_portals, selected_categories):
        """Simula o download dos dados selecionados."""
        downloads = []
        with st.spinner("Baixando dados selecionados..."):
            for portal in selected_portals:
                for category in selected_categories:
                    if category in portal["categories"]:
                        # Simular tempo de download
                        time.sleep(1.5)

                        # Simular resultado de download
                        file_format = portal["data_format"]
                        downloads.append(
                            {
                                "portal": portal["title"],
                                "category": category,
                                "filename": f"{category.lower()}_{portal['url'].split('//')[1].split('.')[0]}_{random.randint(1000, 9999)}.{file_format.lower()}",
                                "size": f"{random.randint(100, 9999)} KB",
                                "status": random.choices(
                                    ["Concluído", "Erro"], weights=[0.9, 0.1]
                                )[0],
                            }
                        )
        return downloads


def main():
    st.set_page_config(
        page_title="Agente de Portais de Transparência", page_icon="🔍", layout="wide"
    )

    st.title("🔍 Agente de Busca em Portais de Transparência")
    st.markdown(
        """
    Este aplicativo simula um agente de IA que busca, analisa e faz download de dados de portais de transparência municipais.
    
    **Instruções:**
    1. Insira o nome da cidade e o estado
    2. Inicie a busca por portais de transparência
    3. Selecione as fontes e tipos de dados desejados
    4. Inicie o download dos dados
    """
    )

    # Inicializar o agente simulado
    agent = MockTransparencyAgent()

    # Formulário de busca
    with st.form("search_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            city = st.text_input("Cidade", placeholder="Ex: São Paulo")
        with col2:
            state = st.text_input("Estado (UF)", placeholder="Ex: SP", max_chars=2)

        submitted = st.form_submit_button("Buscar Portais de Transparência")

    # Resultados da busca
    if submitted and city and state:
        # Armazenar os resultados na sessão para persistência entre interações
        st.session_state.city = city
        st.session_state.state = state
        st.session_state.search_results = agent.search_transparency_portal(city, state)
        st.session_state.analyzed_pages = agent.analyze_pages(
            st.session_state.search_results
        )

        # Mostrar análise
        st.subheader("Portais de Transparência Encontrados")

        # Tabela de resultados analisados
        if st.session_state.analyzed_pages:
            result_data = []
            for portal in st.session_state.analyzed_pages:
                result_data.append(
                    {
                        "Portal": portal["title"],
                        "URL": portal["url"],
                        "Categorias": ", ".join(portal["categories"]),
                        "Última Atualização": portal["last_update"],
                        "Formato": portal["data_format"],
                    }
                )

            st.dataframe(pd.DataFrame(result_data), use_container_width=True)

            # Seleção de portais e categorias para download
            st.subheader("Selecionar Dados para Download")

            col1, col2 = st.columns(2)
            with col1:
                selected_portals_indices = st.multiselect(
                    "Selecione os portais:",
                    options=range(len(st.session_state.analyzed_pages)),
                    format_func=lambda i: st.session_state.analyzed_pages[i]["title"],
                )

            # Obter todas as categorias únicas dos portais selecionados
            all_categories = set()
            for idx in selected_portals_indices:
                all_categories.update(
                    st.session_state.analyzed_pages[idx]["categories"]
                )

            with col2:
                selected_categories = st.multiselect(
                    "Selecione as categorias de dados:",
                    options=sorted(list(all_categories)),
                )

            if (
                st.button("Iniciar Download dos Dados", type="primary")
                and selected_portals_indices
                and selected_categories
            ):
                selected_portals = [
                    st.session_state.analyzed_pages[i] for i in selected_portals_indices
                ]
                downloads = agent.download_data(selected_portals, selected_categories)

                st.subheader("Resultados do Download")

                # Tabela de downloads
                download_data = []
                for item in downloads:
                    download_data.append(
                        {
                            "Portal": item["portal"],
                            "Categoria": item["category"],
                            "Arquivo": item["filename"],
                            "Tamanho": item["size"],
                            "Status": item["status"],
                        }
                    )

                st.dataframe(pd.DataFrame(download_data), use_container_width=True)

                # Resumo dos downloads
                success_count = sum(
                    1 for item in downloads if item["status"] == "Concluído"
                )
                error_count = len(downloads) - success_count

                st.success(f"✅ {success_count} arquivos baixados com sucesso")
                if error_count > 0:
                    st.error(f"❌ {error_count} arquivos com erro")
        else:
            st.warning("Nenhum portal de transparência encontrado.")


if __name__ == "__main__":
    main()
