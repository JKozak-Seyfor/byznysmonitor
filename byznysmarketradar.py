# app.py
import json
import requests
import streamlit as st

WEBHOOK_URL = "https://hook.eu2.make.com/hpp92lgjkfbhsd6w89mjovjkbeap58pw"

st.set_page_config(page_title="JSON → Webhook sender", page_icon="📨", layout="centered")
st.title("📨 Odeslání JSON souboru na webhook")

st.write("Nahraj JSON soubor, zkontroluj náhled a odešli ho na webhook.")

uploaded = st.file_uploader("Vyber .json soubor", type=["json"])

json_data = None

if uploaded is not None:
    try:
        raw_bytes = uploaded.read()
        raw_text = raw_bytes.decode("utf-8")
        json_data = json.loads(raw_text)

        st.success("JSON je validní ✅")
        st.subheader("Náhled JSON")
        st.json(json_data)

    except UnicodeDecodeError:
        st.error("Soubor nejde dekódovat jako UTF-8. Ujisti se, že je uložený v UTF-8.")
    except json.JSONDecodeError as e:
        st.error(f"Nevalidní JSON: {e}")

st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    send_btn = st.button("Odeslat na webhook", type="primary", disabled=(json_data is None))

with col2:
    st.caption("Odesílá se jako HTTP POST s hlavičkou `Content-Type: application/json`.")

if send_btn and json_data is not None:
    try:
        with st.spinner("Odesílám…"):
            # Requests umí poslat JSON a zároveň nastaví Content-Type
            resp = requests.post(
                WEBHOOK_URL,
                json=json_data,
                timeout=20,
            )

        st.subheader("Výsledek")
        st.write(f"Status: **{resp.status_code}**")

        # Make webhook často vrací krátkou odpověď; zobrazíme ji, pokud existuje
        if resp.text:
            st.code(resp.text[:4000])
        else:
            st.info("Webhook nevrátil žádné tělo odpovědi.")

        if 200 <= resp.status_code < 300:
            st.success("Odesláno ✅")
        else:
            st.error("Webhook vrátil chybu ❌")

    except requests.exceptions.Timeout:
        st.error("Timeout při odesílání. Zkus to znovu nebo zvedni timeout.")
    except requests.exceptions.RequestException as e:
        st.error(f"Chyba při HTTP požadavku: {e}")
