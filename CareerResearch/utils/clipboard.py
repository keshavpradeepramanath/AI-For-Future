import streamlit.components.v1 as components

def copy_button(text: str):
    components.html(
        f"""
        <textarea id="copyText" style="display:none;">
{text}
        </textarea>

        <button
            onclick="
                const t = document.getElementById('copyText').value;
                navigator.clipboard.writeText(t);
                this.innerText='✅ Copied!';
                setTimeout(() => this.innerText='📋 Copy Full Answer', 2000);
            "
            style="
                padding:10px 16px;
                font-size:14px;
                border-radius:6px;
                border:none;
                background:#4CAF50;
                color:white;
                cursor:pointer;
            "
        >
            📋 Copy Full Answer
        </button>
        """,
        height=80
    )
