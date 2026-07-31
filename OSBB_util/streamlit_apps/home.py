# G:\Programming\Py\OSBB_util\streamlit_apps\home.py
"""
Главная страница OSBB Data Explorer
"""

import sys
from pathlib import Path

STREAMLIT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(STREAMLIT_ROOT))

import streamlit as st
from utils.db import get_conn

st.set_page_config(
    page_title="OSBB Data Explorer",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 OSBB Data Explorer")
st.caption("Работа с базой данных OSBB через Streamlit")

# Проверка подключения
conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM apartments")
count = cur.fetchone()[0]
conn.close()

st.success(f"✅ Подключено к БД. Квартир: {count}")

# ==========================================
# НАВИГАЦИЯ
# ==========================================

st.markdown("## 📚 Доступные разделы")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏠 Карточка квартиры", use_container_width=True):
        st.switch_page("pages/01_apartment_card.py")

with col2:
    if st.button("💰 Платежи", use_container_width=True):
        st.switch_page("pages/03_payments_viewer.py")

# Информация о проекте
with st.expander("ℹ️ О проекте"):
    st.markdown("""
    **OSBB Data Explorer** — вспомогательный инструмент для просмотра данных проекта OSBB.
    
    - База данных: `osbb_test.db`
    - Количество таблиц: ~100+
    - Интерфейс: Streamlit
    """)