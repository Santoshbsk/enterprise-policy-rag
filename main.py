import streamlit as st

from rag import ask_question


st.set_page_config(
    page_title="Company Policy Assistant",
    page_icon="💬",
    layout="centered",
)

st.title("Company Policy Assistant")
st.caption("Ask questions about company policies and get answers grounded in the policy documents.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("Retrieved sources"):
                for source in message["sources"]:
                    st.write(
                        f"{source['name']} | chunk={source['chunk']} "
                        f"| distance={source['distance']:.4f}"
                    )

question = st.chat_input("Ask about leave, benefits, travel, or work from home...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Checking the policy documents..."):
            try:
                answer, results = ask_question(question, top_k=3)
                sources = [
                    {
                        "name": metadata.get("source", "Unknown source"),
                        "chunk": metadata.get("chunk_id", "Unknown"),
                        "distance": results["distances"][0][index],
                    }
                    for index, metadata in enumerate(results["metadatas"][0])
                ]
                st.markdown(answer)
                with st.expander("Retrieved sources"):
                    for source in sources:
                        st.write(
                            f"{source['name']} | chunk={source['chunk']} "
                            f"| distance={source['distance']:.4f}"
                        )
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer, "sources": sources}
                )
            except Exception as error:
                message = f"I couldn't answer that right now: {error}"
                st.error(message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": message}
                )