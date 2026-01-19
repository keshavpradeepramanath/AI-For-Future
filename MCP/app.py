import streamlit as st
from llm_router import route_query
from mcp.client import MCPClient

st.set_page_config(page_title="MCP Streamlit Demo")
st.title("🔌 MCP + Streamlit Demo")

query = st.text_input("Ask something:")

if query:
    decision = route_query(query)

    if decision["tool"]:
        client = MCPClient("http://localhost:8000")
        result = client.call_tool(
            decision["tool"],
            decision["args"]
        )
        st.success(f"Tool Result: {result}")
    else:
        st.info(decision["response"])
