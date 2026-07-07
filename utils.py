import streamlit as st


def add_footer():

    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            bottom: 8px;
            width: 100%;
            text-align: center;
            font-size: 12px;
            color: white;
        }
        </style>

        <div class="footer">
            Pulmo
        </div>
        """,
        unsafe_allow_html=True
    )
