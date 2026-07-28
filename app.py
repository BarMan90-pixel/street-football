import streamlit as st
import random
import pandas as pd
import json
import os

DATA_FILE = "tournament_data.json"

def save_data():
    data = {
        "players": st.session_state.get("players", []),
        "groups": st.session_state.get("groups", {}),
        "group_scores": st.session_state.get("group_scores", {}),
        "playoff_scores": st.session_state.get("playoff_scores", {})
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                st.session_state.players = data.get("players", [])
                st.session_state.groups = data.get("groups", {})
                st.session_state.group_scores = data.get("group_scores", {})
                st.session_state.playoff_scores = data.get("playoff_scores", {})
        except Exception as e:
            st.error(f"Ошибка загрузки данных: {e}")

st.set_page_config(
    page_title="Лига уличного футбола", 
    page_icon="⚽",
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Ультрасовременный дизайн: скругления, плавные тени, микроанимации и стильный стеккломорфизм
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,700;0,900;1,900&family=Inter:wght@400;500;600;700&display=swap');

        .stApp {
            background-color: #0B0F19;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(239, 68, 68, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(59, 130, 246, 0.08) 0%, transparent 40%);
            color: #F8FAFC;
            font-family: 'Inter', sans-serif;
        }

        h1 {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            font-size: 2.3rem !important;
            font-style: italic;
            text-transform: uppercase;
            letter-spacing: 1.5px !important;
            background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 60%, #EF4444 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-top: 10px !important;
            margin-bottom: 30px !important;
        }
        
        h2, h3, .stHeader {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            text-transform: uppercase;
            letter-spacing: 1px !important;
            color: #F8FAFC !important;
            font-size: 1.4rem !important;
            border-left: 4px solid #EF4444;
            padding-left: 12px;
            margin-top: 25px !important;
            margin-bottom: 15px !important;
        }

        label, .stCheckbox label span, .stNumberInput label, .stSelectbox label, p {
            color: #94A3B8 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        /* Поля ввода и тексты с эффектом мягкого стекла */
        div[data-baseweb="textarea"] {
            background-color: rgba(30, 41, 59, 0.5) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(12px);
            transition: all 0.3s ease;
        }
        div[data-baseweb="textarea"] textarea {
            color: #F8FAFC !important;
            -webkit-text-fill-color: #F8FAFC !important;
            background-color: transparent !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            padding: 14px !important;
        }
        div[data-baseweb="textarea"]:focus-within {
            border-color: #EF4444 !important;
            box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.15) !important;
        }

        div[data-baseweb="input"] {
            background-color: rgba(30, 41, 59, 0.5) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(8px);
        }
        div[data-baseweb="input"] input {
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }

        /* Контейнеры-экспандеры с плавной тенью и закруглениями */
        div[data-testid="stExpander"] {
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 18px !important;
            margin-bottom: 14px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5) !important;
            backdrop-filter: blur(16px);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        div[data-testid="stExpander"]:hover {
            border-color: rgba(239, 68, 68, 0.3) !important;
            transform: translateY(-1px);
        }
        div[data-testid="stExpander"] * {
            color: #F8FAFC !important;
        }

        /* Кнопки с живой микроанимацией нажатия и градиентом */
        .stButton>button {
            width: 100%;
            border-radius: 14px;
            height: 3.4em;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            font-size: 15px !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 4px 20px rgba(239, 68, 68, 0.35);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(239, 68, 68, 0.5);
            background: linear-gradient(135deg, #F87171 0%, #B91C1C 100%) !important;
        }

        .stButton>button:active {
            transform: scale(0.97) translateY(1px);
            box-shadow: 0 2px 10px rgba(239, 68, 68, 0.3);
        }

        /* Датафреймы в лаконичном стиле */
        div[data-testid="stDataFrame"] {
            background-color: rgba(15, 23, 42, 0.5) !important;
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }
        div[data-testid="stDataFrame"] * {
            color: #F8FAFC !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
        }

        /* Навигационные табы */
        button[data-baseweb="tab"] {
            color: #64748B !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 12px 16px !important;
            transition: color 0.2s ease;
        }
        button[aria-selected="true"] {
            color: #EF4444 !important;
            border-bottom: 3px solid #EF4444 !important;
        }

        .stCaption {
            color: #64748B !important;
            font-weight: 500 !important;
            font-size: 13px !important;
        }

        hr {
            border-color: rgba(255, 255, 255, 0.06) !important;
            margin: 25px 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ ЛИГА УЛИЧНОГО ФУТБОЛА")

if "initialized" not in st.session_state:
    st.session_state.players = []
    st.session_state.groups = {}
    st.session_state.group_scores = {}
    st.session_state.playoff_scores = {}
    load_data()
    st.session_state.initialized = True

with st.sidebar:
    st.subheader("💾 Управление данными")
    if st.button("💾 Сохранить турнир"):
        save_data()
        st.success("Данные сохранены!")
        
    if st.button("🗑 Сбросить турнир"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.session_state.players = []
        st.session_state.groups = {}
        st.session_state.group_scores = {}
        st.session_state.playoff_scores = {}
        st.success("Турнир сброшен!")
        st.rerun()

tab1, tab2, tab3, tab4 = st.tabs(["🎲 Жеребьевка", "📅 Календарь", "📊 Группы", "🏆 Результаты"])

# ==========================================
# 1. ЖЕРЕБЬЕВКА С ВЫБОРОМ КОЛИЧЕСТВА ГРУПП
# ==========================================
with tab1:
    st.header("Список участников и настройки")
    
    col_set1, col_set2 = st.columns(2)
    num_groups = col_set1.selectbox("Количество групп:", options=[1, 2, 3, 4], index=3)
    
    default_text = "\n".join(st.session_state.players) if st.session_state.players else "\n".join([f"Игрок {i}" for i in range(1, 13)])
    raw_players = st.text_area(
        "Введите ФИО игроков (по одному на строку):", 
        value=default_text, 
        height=180
    )
    
    if st.button("🎲 ПРОВЕСТИ ЖЕРЕБЬЕВКУ"):
        players_list = [p.strip() for p in raw_players.split("\n") if p.strip()]
        min_players = num_groups * 3
        if len(players_list) < min_players:
            st.error(f"Для {num_groups} групп(ы) нужно минимум {min_players} игроков (по 3 человека в группу)! У вас: {len(players_list)}.")
        else:
            st.session_state.players = players_list.copy()
            random.shuffle(players_list)
            
            all_group_names = ["Группа А", "Группа Б", "Группа В", "Группа Г"]
            group_names = all_group_names[:num_groups]
            st.session_state.groups = {g: [] for g in group_names}
            
            for i, p in enumerate(players_list):
                g_idx = i % num_groups
                st.session_state.groups[group_names[g_idx]].append(p)
                
            st.session_state.group_scores = {}
            st.session_state.playoff_scores = {}
            save_data()
            st.success("Игроки распределены по группам!")

    if st.session_state.groups:
        st.markdown("---")
        st.subheader("🛠 Ручная корректировка групп")
        st.caption("Выберите новую группу для любого игрока, если нужно изменить распределение:")

        group_names = list(st.session_state.groups.keys())
        
        for player in st.session_state.players:
            current_group = next((g for g, p_list in st.session_state.groups.items() if player in p_list), group_names[0])
            
            new_group = st.selectbox(
                f"Игрок: {player}",
                options=group_names,
                index=group_names.index(current_group),
                key=f"select_{player}"
            )
            
            if new_group != current_group:
                st.session_state.groups[current_group].remove(player)
                st.session_state.groups[new_group].append(player)
                save_data()
                st.rerun()

        st.markdown("---")
        st.subheader("Состав групп (Итоговый)")
        for g_name, g_players in st.session_state.groups.items():
            with st.expander(f"📌 {g_name} ({len(g_players)} чел.)", expanded=True):
                for idx, pl in enumerate(g_players, 1):
                    st.write(f"**№{idx}.** <span style='color:#F8FAFC;'>{pl}</span>", unsafe_allow_html=True)

def get_group_matches(players):
    matches = []
    n = len(players)
    for i in range(n):
        for j in range(i + 1, n):
            matches.append((players[i], players[j]))
    return matches

def calculate_cross_table(g_name, players):
    n = len(players)
    stats = {p: {"И": 0, "В": 0, "Н": 0, "П": 0, "МЗ": 0, "МП": 0, "Очки": 0} for p in players}
    pair_res = {p1: {p2: "—" for p2 in players} for p1 in players}
    
    for p in players:
        pair_res[p][p] = "❌"
        
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = players[i], players[j]
            key1 = f"{g_name}_{p1}_vs_{p2}"
            key2 = f"{g_name}_{p2}_vs_{p1}"
            
            key = key1 if key1 in st.session_state.group_scores else key2
            
            if key in st.session_state.group_scores:
                data = st.session_state.group_scores[key]
                s1, s2 = data.get("s1", 0), data.get("s2", 0)
                panna1, panna2 = data.get("panna1", False), data.get("panna2", False)
                
                if key == key2:
                    s1, s2 = s2, s1
                    panna1, panna2 = panna2, panna1
                
                txt1 = f"{s1}:{s2}" + (" 🔴" if panna1 else "")
                txt2 = f"{s2}:{s1}" + (" 🔴" if panna2 else "")
                pair_res[p1][p2] = txt1
                pair_res[p2][p1] = txt2
                
                stats[p1]["И"] += 1; stats[p2]["И"] += 1
                stats[p1]["МЗ"] += s1; stats[p1]["МП"] += s2
                stats[p2]["МЗ"] += s2; stats[p2]["МП"] += s1
                
                if panna1:
                    stats[p1]["В"] += 1; stats[p1]["Очки"] += 4; stats[p2]["П"] += 1
                elif panna2:
                    stats[p2]["В"] += 1; stats[p2]["Очки"] += 4; stats[p1]["П"] += 1
                elif s1 > s2:
                    stats[p1]["В"] += 1; stats[p1]["Очки"] += 3; stats[p2]["П"] += 1
                elif s1 < s2:
                    stats[p2]["В"] += 1; stats[p2]["Очки"] += 3; stats[p1]["П"] += 1
                else:
                    stats[p1]["Н"] += 1; stats[p2]["Н"] += 1
                    stats[p1]["Очки"] += 1; stats[p2]["Очки"] += 1

    temp_df = pd.DataFrame.from_dict(stats, orient="index")
    temp_df["Разница"] = temp_df["МЗ"] - temp_df["МП"]
    temp_df = temp_df.sort_values(by=["Очки", "Разница", "МЗ"], ascending=False)
    
    rows = []
    for idx, (p, row_stat) in enumerate(temp_df.iterrows(), 1):
        row_dict = {"Место": idx, "Игрок": p}
        for o_idx, opp in enumerate(players, 1):
            row_dict[f"№{o_idx}"] = pair_res[p][opp]
            
        row_dict.update({
            "И": row_stat["И"],
            "В": row_stat["В"],
            "Н": row_stat["Н"],
            "П": row_stat["П"],
            "Разница": row_stat["Разница"],
            "Очки": row_stat["Очки"]
        })
        rows.append(row_dict)
        
    df_cross = pd.DataFrame(rows)
    df_standings = temp_df.reset_index().rename(columns={"index": "Игрок"})
    return df_cross, df_standings

def get_current_standings():
    standings = {}
    if "groups" in st.session_state and st.session_state.groups:
        for g_name, g_players in st.session_state.groups.items():
            _, df_standing = calculate_cross_table(g_name, g_players)
            standings[g_name] = df_standing
    return standings

# ==========================================
# 2. КАЛЕНДАРЬ ИГР (ГРУППЫ + ПЛЕЙ-ОФФ)
# ==========================================
with tab2:
    if not st.session_state.groups:
        st.info("Проведите жеребьевку на первой вкладке.")
    else:
        st.subheader("📋 Легенда посева (номера игроков в группах)")
        for g_name, g_players in st.session_state.groups.items():
            num_legend = ", ".join([f"**{g_name[7:]}{i+1}**: {p}" for i, p in enumerate(g_players)])
            st.markdown(f"**{g_name}:** {num_legend}")
            
        st.markdown("---")
        st.header("📅 Матчи группового этапа")
        
        scores_updated = False
        
        for g_name, g_players in st.session_state.groups.items():
            with st.expander(f"📌 {g_name} (Матчи)", expanded=True):
                matches = get_group_matches(g_players)
                g_code = g_name[7:]
                
                for p1, p2 in matches:
                    i1 = g_players.index(p1) + 1
                    i2 = g_players.index(p2) + 1
                    key = f"{g_name}_{p1}_vs_{p2}"
                    
                    old_data = st.session_state.group_scores.get(key, {})
                    def_s1 = old_data.get("s1", 0)
                    def_s2 = old_data.get("s2", 0)
                    def_p1 = old_data.get("panna1", False)
                    def_p2 = old_data.get("panna2", False)

                    st.markdown(f"{i1}{g_code} **{p1}** vs {i2}{g_code} **{p2}**")
                    c1, c2 = st.columns(2)
                    s1 = c1.number_input(f"Голы {p1}", min_value=0, value=def_s1, key=f"{key}_s1")
                    s2 = c2.number_input(f"Голы {p2}", min_value=0, value=def_s2, key=f"{key}_s2")
                    
                    cp1, cp2 = st.columns(2)
                    panna1 = cp1.checkbox(f"🔴 ПАННА от {p1}", value=def_p1, key=f"{key}_panna1")
                    panna2 = cp2.checkbox(f"🔴 ПАННА от {p2}", value=def_p2, key=f"{key}_panna2")
                    
                    new_val = {"s1": s1, "s2": s2, "panna1": panna1, "panna2": panna2}
                    if old_data != new_val:
                        st.session_state.group_scores[key] = new_val
                        scores_updated = True
                        
                    st.markdown("<hr style='margin:10px 0 !important;'>", unsafe_allow_html=True)

        if scores_updated:
            save_data()

        st.markdown("---")
        st.header("🥊 Плей-офф")
        
        standings = get_current_standings()
        num_groups = len(st.session_state.groups)
        
        if len(standings) != num_groups or any(len(df) < 2 for df in standings.values()):
            st.info("Завершите матчи в группах, чтобы сформировалась сетка плей-офф.")
        else:
            try:
                if "playoff_scores" not in st.session_state:
                    st.session_state.playoff_scores = {}
                po_scores = st.session_state.playoff_scores

                def handle_po_match(match_key, title, player1, player2):
                    st.markdown(f"### {title}")
                    st.markdown(f"**<span style='color:#F8FAFC;'>{player1}</span>** vs **<span style='color:#F8FAFC;'>{player2}</span>**", unsafe_allow_html=True)
                    
                    old_po = po_scores.get(match_key, {})
                    c1, c2 = st.columns(2)
                    sc1 = c1.number_input("Счет 1", min_value=0, value=old_po.get("sc1", 0), key=f"po_{match_key}_1")
                    sc2 = c2.number_input("Счет 2", min_value=0, value=old_po.get("sc2", 0), key=f"po_{match_key}_2")
                    p1_panna = c1.checkbox("Панна", value=old_po.get("p1_panna", False), key=f"po_panna_{match_key}_1")
                    p2_panna = c2.checkbox("Панна", value=old_po.get("p2_panna", False), key=f"po_panna_{match_key}_2")
                    
                    new_po = {"sc1": sc1, "sc2": sc2, "p1_panna": p1_panna, "p2_panna": p2_panna}
                    if old_po != new_po:
                        po_scores[match_key] = new_po
                        save_data()

                    winner, loser = player1, player2
                    if p1_panna:
                        winner, loser = player1, player2
                    elif p2_panna:
                        winner, loser = player2, player1
                    elif sc1 > sc2:
                        winner, loser = player1, player2
                    elif sc2 > sc1:
                        winner, loser = player2, player1
                    return winner, loser

                group_names_keys = list(standings.keys())
                
                if num_groups == 4:
                    p1A = standings["Группа А"]["Игрок"].iloc[0]
                    p2A = standings["Группа А"]["Игрок"].iloc[1]
                    p1B = standings["Группа Б"]["Игрок"].iloc[0]
                    p2B = standings["Группа Б"]["Игрок"].iloc[1]
                    p1V = standings["Группа В"]["Игрок"].iloc[0]
                    p2V = standings["Группа В"]["Игрок"].iloc[1]
                    p1G = standings["Группа Г"]["Игрок"].iloc[0]
                    p2G = standings["Группа Г"]["Игрок"].iloc[1]

                    qf_pairs = [
                        ("qf_1", "1/4 #1 (1А vs 2Г)", p1A, p2G),
                        ("qf_2", "1/4 #2 (1В vs 2Б)", p1V, p2B),
                        ("qf_3", "1/4 #3 (1Б vs 2В)", p1B, p2V),
                        ("qf_4", "1/4 #4 (1Г vs 2А)", p1G, p2A),
                    ]
                    qf_winners, qf_losers = [], []
                    for m_key, title, pl1, pl2 in qf_pairs:
                        with st.expander(title, expanded=True):
                            w, l = handle_po_match(m_key, title, pl1, pl2)
                            qf_winners.append(w)
                            qf_losers.append(l)

                    st.subheader("🔥 1/2 Финала")
                    sf_pairs = [
                        ("sf_1", "1/2 #1", qf_winners[0], qf_winners[1]),
                        ("sf_2", "1/2 #2", qf_winners[2], qf_winners[3])
                    ]
                    sf_winners, sf_losers = [], []
                    for m_key, title, pl1, pl2 in sf_pairs:
                        with st.expander(title, expanded=True):
                            w, l = handle_po_match(m_key, title, pl1, pl2)
                            sf_winners.append(w)
                            sf_losers.append(l)

                    st.subheader("🏆 Финальная стадия")
                    with st.expander("🥉 Матч за 3-е место", expanded=True):
                        handle_po_match("m3", "Матч за 3-е место", sf_losers[0], sf_losers[1])
                    with st.expander("👑 ФИНАЛ", expanded=True):
                        handle_po_match("final", "Финальный матч", sf_winners[0], sf_winners[1])

                elif num_groups == 2:
                    p1A = standings["Группа А"]["Игрок"].iloc[0]
                    p2A = standings["Группа А"]["Игрок"].iloc[1]
                    p1B = standings["Группа Б"]["Игрок"].iloc[0]
                    p2B = standings["Группа Б"]["Игрок"].iloc[1]

                    st.subheader("🔥 1/2 Финала (Перекрестный плей-офф)")
                    sf_pairs = [
                        ("sf_1", "1/2 #1 (1А vs 2Б)", p1A, p2B),
                        ("sf_2", "1/2 #2 (1Б vs 2А)", p1B, p2A)
                    ]
                    sf_winners, sf_losers = [], []
                    for m_key, title, pl1, pl2 in sf_pairs:
                        with st.expander(title, expanded=True):
                            w, l = handle_po_match(m_key, title, pl1, pl2)
                            sf_winners.append(w)
                            sf_losers.append(l)

                    st.subheader("🏆 Финальная стадия")
                    with st.expander("🥉 Матч за 3-е место", expanded=True):
                        handle_po_match("m3", "Матч за 3-е место", sf_losers[0], sf_losers[1])
                    with st.expander("👑 ФИНАЛ", expanded=True):
                        handle_po_match("final", "Финальный матч", sf_winners[0], sf_winners[1])

                elif num_groups == 3:
                    p1A = standings["Группа А"]["Игрок"].iloc[0]
                    p1B = standings["Группа Б"]["Игрок"].iloc[0]
                    p1V = standings["Группа В"]["Игрок"].iloc[0]
                    second_places = []
                    for g in ["Группа А", "Группа Б", "Группа В"]:
                        second_places.append((standings[g]["Игрок"].iloc[1], standings[g]["Очки"].iloc[1], standings[g]["Разница"].iloc[1]))
                    second_places.sort(key=lambda x: (x[1], x[2]), reverse=True)
                    best_2nd = second_places[0][0]

                    st.subheader("🔥 1/2 Финала")
                    sf_pairs = [
                        ("sf_1", "1/2 #1 (1А vs Лучший 2-й)", p1A, best_2nd),
                        ("sf_2", "1/2 #2 (1Б vs 1В)", p1B, p1V)
                    ]
                    sf_winners, sf_losers = [], []
                    for m_key, title, pl1, pl2 in sf_pairs:
                        with st.expander(title, expanded=True):
                            w, l = handle_po_match(m_key, title, pl1, pl2)
                            sf_winners.append(w)
                            sf_losers.append(l)

                    st.subheader("🏆 Финальная стадия")
                    with st.expander("🥉 Матч за 3-е место", expanded=True):
                        handle_po_match("m3", "Матч за 3-е место", sf_losers[0], sf_losers[1])
                    with st.expander("👑 ФИНАЛ", expanded=True):
                        handle_po_match("final", "Финальный матч", sf_winners[0], sf_winners[1])

                elif num_groups == 1:
                    g_name = group_names_keys[0]
                    p1 = standings[g_name]["Игрок"].iloc[0]
                    p2 = standings[g_name]["Игрок"].iloc[1]
                    p3 = standings[g_name]["Игрок"].iloc[2]
                    p4 = standings[g_name]["Игрок"].iloc[3]

                    st.subheader("🔥 1/2 Финала")
                    sf_pairs = [
                        ("sf_1", "1/2 #1 (1-й vs 4-й)", p1, p4),
                        ("sf_2", "1/2 #2 (2-й vs 3-й)", p2, p3)
                    ]
                    sf_winners, sf_losers = [], []
                    for m_key, title, pl1, pl2 in sf_pairs:
                        with st.expander(title, expanded=True):
                            w, l = handle_po_match(m_key, title, pl1, pl2)
                            sf_winners.append(w)
                            sf_losers.append(l)

                    st.subheader("🏆 Финальная стадия")
                    with st.expander("🥉 Матч за 3-е место", expanded=True):
                        handle_po_match("m3", "Матч за 3-е место", sf_losers[0], sf_losers[1])
                    with st.expander("👑 ФИНАЛ", expanded=True):
                        handle_po_match("final", "Финальный матч", sf_winners[0], sf_winners[1])

            except Exception as e:
                st.warning("Для формирования сетки плей-офф требуется полностью завершить матчи группового этапа.")

# ==========================================
# 3. ГРУППЫ (ШАХМАТКИ С РЕЗУЛЬТАТАМИ)
# ==========================================
with tab3:
    if not st.session_state.groups:
        st.info("Проведите жеребьевку на первой вкладке.")
    else:
        st.header("📊 Турнирные таблицы групп")
        for g_name, g_players in st.session_state.groups.items():
            st.subheader(f"📌 {g_name}")
            df_cross, _ = calculate_cross_table(g_name, g_players)
            st.dataframe(
                df_cross, 
                use_container_width=True,
                hide_index=True
            )

# ==========================================
# 4. РЕЗУЛЬТАТЫ (ПОБЕДИТЕЛИ, ПРИЗЕРЫ + РЕЙТИНГ)
# ==========================================
with tab4:
    if not st.session_state.groups:
        st.info("Данные турнира отсутствуют.")
    else:
        standings = get_current_standings()
        po_scores = st.session_state.get("playoff_scores", {})
        
        try:
            playoff_points = {p: 0 for p in st.session_state.players}

            st.header("🏆 Пьедестал почета")
            st.markdown(f"### 🥇 1 МЕСТО: <span style='color:#EF4444;'>Итоги турнира</span>", unsafe_allow_html=True)

            st.markdown("---")
            st.header("📊 Итоговый рейтинг всех участников")
            
            group_points_map = {}
            for g_name, df_g in standings.items():
                for _, row in df_g.iterrows():
                    group_points_map[row["Игрок"]] = row["Очки"]
            
            all_results = []
            for player in st.session_state.players:
                g_pts = group_points_map.get(player, 0)
                po_pts = playoff_points.get(player, 0)
                total_pts = g_pts + po_pts
                all_results.append({
                    "Игрок": player,
                    "Очки (Группа)": g_pts,
                    "Очки (Плей-офф)": po_pts,
                    "Всего очков": total_pts
                })
            
            df_final = pd.DataFrame(all_results)
            df_final = df_final.sort_values(by=["Всего очков", "Очки (Плей-офф)", "Очки (Группа)"], ascending=False)
            df_final.reset_index(drop=True, inplace=True)
            df_final.index += 1
            df_final.reset_index(inplace=True)
            df_final.rename(columns={"index": "Место"}, inplace=True)
            
            st.dataframe(
                df_final[["Место", "Игрок", "Очки (Группа)", "Очки (Плей-офф)", "Всего очков"]], 
                use_container_width=True,
                hide_index=True
            )

        except Exception as e:
            st.info("Заполните результаты группового и финального этапов для формирования итоговой таблицы.")
