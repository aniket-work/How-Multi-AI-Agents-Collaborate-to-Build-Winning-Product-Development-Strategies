import os

import streamlit as st
import time

from langgraph.constants import END

from graph_builder import build_graph
import constants

import streamlit as st
import time
import os
from graph_builder import build_graph
import constants


def format_agent_response(response):
    # Remove the agent prefix and extract the content
    content = response.split("content=", 1)[-1].strip('"')

    # Replace \n with actual newlines
    formatted_content = content.replace("\\n", "\n")

    return formatted_content


def handle_ui(query):

    st.sidebar.title("AI Product Dev Org Chat")
    st.sidebar.image("org_chart.png")

    if query:
        with st.spinner(constants.PROCESSING_MESSAGE):
            start_time = time.time()
            graph, initial_state = build_graph(query)
            outputs = []
            for output in graph.stream(initial_state):
                if output is END:
                    break
                elif isinstance(output, tuple) and len(output) == 2:
                    node_name, node_output = output
                    outputs.append((node_name, node_output))
                    st.write(f"Received output from {node_name}")
                else:
                    outputs.append(("Unknown", output))
            end_time = time.time()

        if outputs:
            st.success(constants.SUCCESS_MESSAGE.format(end_time - start_time))

            agent_outputs = {"agent1": "", "agent2": "", "agent3": ""}
            summary = ""

            for item in outputs:
                if isinstance(item, tuple) and len(item) == 2:
                    _, node_output = item
                    if isinstance(node_output, dict):
                        for agent, content in node_output.items():
                            if agent in ["agent1", "agent2", "agent3"]:
                                agent_outputs[agent] = content.get("messages", [""])[0]
                            elif agent == "summarizer":
                                summary = content.get("messages", [""])[0]

            st.markdown("""
            <style>
            .agent-output {
                background-color: #f0f2f6;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 20px;
            }
            .agent-name {
                font-weight: bold;
                font-size: 1.2em;
                margin-bottom: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<div class="agent-output">', unsafe_allow_html=True)
                st.markdown('<p class="agent-name">👨‍💼 AI Employee 1 (llama-3.1)</p>', unsafe_allow_html=True)
                st.markdown(format_agent_response(agent_outputs["agent1"]))
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="agent-output">', unsafe_allow_html=True)
                st.markdown('<p class="agent-name">👨‍💼 AI Employee  2 (mixtral)</p>', unsafe_allow_html=True)
                st.markdown(format_agent_response(agent_outputs["agent2"]))
                st.markdown('</div>', unsafe_allow_html=True)

            with col3:
                st.markdown('<div class="agent-output">', unsafe_allow_html=True)
                st.markdown('<p class="agent-name">👨‍💼 AI Employee  3 (llama-3.2-11b)</p>', unsafe_allow_html=True)
                st.markdown(format_agent_response(agent_outputs["agent3"]))
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="agent-output">', unsafe_allow_html=True)
            st.markdown('<p class="agent-name">👨‍💼 AI Supervisor (llama-3.2-1b-preview) Final Summary</p>', unsafe_allow_html=True)
            st.markdown(format_agent_response(summary))
            st.markdown('</div>', unsafe_allow_html=True)

            # Debug information
            st.sidebar.subheader("Raw Outputs")
            st.sidebar.json(outputs)
        else:
            st.error(constants.ERROR_MESSAGE)
    else:
        st.warning(constants.WARNING_MESSAGE)