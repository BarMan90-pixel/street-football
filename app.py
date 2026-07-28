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
    layout="centered", 
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,700;0,900;1,900&family=Inter:wght@400;600;700&display=swap');

        .stApp {
            background-color: #F8FAFC;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(255, 51, 51, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(15, 23, 42, 0.03) 0%, transparent 50%);
            color: #0F172A;
            font-family: 'Inter', sans-serif;
        }

        h1 {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            font-size: 2.2rem !important;
            font-style: italic;
            text-transform: uppercase;
            letter-spacing: 1.5px !important;
            background: linear-gradient(135deg, #0F172A 0%, #334155 60%, #FF3333 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-top: 10px !important;
            margin-bottom: 25px !important;
        }
        
        h2, h3, .stHeader {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            text-transform: uppercase;
            letter-spacing: 1px !important;
            color: #0F172A !important;
            font-size: 1.5rem !important;
            border-left: 4px solid #FF3333;
            padding-left: 12px;
            margin-top: 20px !important;
            margin-bottom: 15px !important;
        }

        label, .stCheckbox label span, .stNumberInput label, .stSelectbox label, p {
            color: #334155 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }

        div[data-baseweb="textarea"] {
            background-color: #FFFFFF !important;
            border-radius: 12px !important;
            border: 2px solid #E2E8F0 !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        }
        div[data-baseweb="textarea"] textarea {
            color: #0F172A !important;
            -webkit-text-fill-color: #0F172A !important;
            background-color: #FFFFFF !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 12px !important;
        }
        div[data-baseweb="textarea"]:focus-within {
            border-color: #FF3333 !important;
            box-shadow: 0 0 0 3px rgba(255, 51, 51, 0.2) !important;
        }

        div[data-baseweb="input"] {
            background-color: #FFFFFF !important;
            border-radius: 10px !important;
            border: 1px solid #CBD5E1 !important;
        }
        div[data-baseweb="input"] input {
            color: #0F172A !important;
            font-weight: 700 !important;
        }

        div[data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            margin-bottom: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05) !important;
            overflow: hidden;
        }
        
        div[data-testid="stExpander"] * {
            color: #0F172A !important;
        }

        .stButton>button {
            width: 100%;
            border-radius: 12px;
            height: 3.4em;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 900 !important;
            font-size: 16px !important;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            background: linear-gradient(135deg, #FF3333 0%, #DC2626 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 4px 14px rgba(255, 51, 51, 0.3);
            transition: all 0.2s ease-in-out;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 51, 51, 0.45);
            background: linear-gradient(135deg, #FF4D4D 0%, #B91C1C 100%) !important;
        }

        div[data-testid="stDataFrame"] {
            background-color: #FFFFFF !important;
            border-radius: 12px !important;
            border: 1px solid #E2E8F0 !important;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        div[data-testid="stDataFrame"] * {
            color: #0F172A !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
        }

        button[data-baseweb="tab"] {
            color: #64748B !important;
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding: 12px 15px !important;
        }
        button[aria-selected="true"] {
            color: #FF3333 !important;
            border-bottom: 3px solid #FF3333 !important;
        }

        .stCaption {
            color: #64748B !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }

        hr {
            border-color: #E2E8F0 !important;
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

# Четыре новых раздела
tab1, tab2, tab3, tab4 = st.tabs(["🎲 Жеребьевка", "📅 Календарь", "📊 Группы", "🏆 Результаты"])

# ==========================================
# 1. ЖЕРЕБЬЕВКА
# ==========================================
with tab1:
    st.header("Список участников")
    default_text = "\n".join(st.session_state.players) if st.session_state.players else "\n".join([f"Игрок {i}" for i in range(1, 17)])
    raw_players = st.text_area(
        "Введите ФИО игроков (по одному на строку):", 
        value=default_text, 
        height=180
    )
    
    if st.button("🎲 ПРОВЕСТИ ЖЕРЕБЬЕВКУ"):
        players_list = [p.strip() for p in raw_players.split("\n") if p.strip()]
        if len(players_list) < 4:
            st.error("Нужно минимум 4 игрока!")
        else:
            st.session_state.players = players_list.copy()
            random.shuffle(players_list)
            group_names = ["Группа А", "Группа Б", "Группа В", "Группа Г"]
            st.session_state.groups = {g: [] for g in group_names}
            
            for i, p in enumerate(players_list):
                g_idx = i % 4
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
                    st.write(f"**№{idx}.** <span style='color:#0F172A;'>{pl}</span>", unsafe_allow_html=True)

# Вспомогательные функции
def get_group_rounds(players):
    if len(players) < 4:
        return []
    p = players
    return [
        {"tour": 1, "matches": [(p[0], p[3]), (p[1], p[2])]}, 
        {"tour": 2, "matches": [(p[0], p[2]), (p[3], p[1])]}, 
        {"tour": 3, "matches": [(p[0], p[1]), (p[2], p[3])]}  
    ]

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

# Предварительный расчет турнирных таблиц для плей-офф
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
        st.header("📅 Групповой этап (по турам)")
        
        scores_updated = False
        
        for tour_num in range(1, 4):
            with st.expander(f"📌 ТУР {tour_num}", expanded=True):
                for g_name, g_players in st.session_state.groups.items():
                    if len(g_players) == 4:
                        rounds = get_group_rounds(g_players)
                        tour_data = rounds[tour_num - 1]
                        g_code = g_name[7:]
                        
                        for p1, p2 in tour_data["matches"]:
                            i1 = g_players.index(p1) + 1
                            i2 = g_players.index(p2) + 1
                            key = f"{g_name}_{p1}_vs_{p2}"
                            
                            old_data = st.session_state.group_scores.get(key, {})
                            def_s1 = old_data.get("s1", 0)
                            def_s2 = old_data.get("s2", 0)
                            def_p1 = old_data.get("panna1", False)
                            def_p2 = old_data.get("panna2", False)

                            st.markdown(f"**[{g_name}]** {i1}{g_code} **{p1}** vs {i2}{g_code} **{p2}**")
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
        if len(standings) < 4 or any(len(df) < 2 for df in standings.values()):
            st.info("Завершите матчи в группах, чтобы определились участники плей-офф.")
        else:
            try:
                p1A = standings["Группа А"]["Игрок"].iloc[0]
                p2A = standings["Группа А"]["Игрок"].iloc[1]
                p1B = standings["Группа Б"]["Игрок"].iloc[0]
                p2B = standings["Группа Б"]["Игрок"].iloc[1]
                p1V = standings["Группа В"]["Игрок"].iloc[0]
                p2V = standings["Группа В"]["Игрок"].iloc[1]
                p1G = standings["Группа Г"]["Игрок"].iloc[0]
                p2G = standings["Группа Г"]["Игрок"].iloc[1]
                
                if "playoff_scores" not in st.session_state:
                    st.session_state.playoff_scores = {}
                po_scores = st.session_state.playoff_scores

                def handle_po_match(match_key, title, player1, player2):
                    st.markdown(f"### {title}")
                    st.markdown(f"**<span style='color:#0F172A;'>{player1}</span>** vs **<span style='color:#0F172A;'>{player2}</span>**", unsafe_allow_html=True)
                    
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

                    winner, loser = None, None
                    if p1_panna:
                        winner, loser = player1, player2
                    elif p2_panna:
                        winner, loser = player2, player1
                    elif sc1 > sc2:
                        winner, loser = player1, player2
                    elif sc2 > sc1:
                        winner, loser = player2, player1
                    return winner, loser

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
                    ("sf_1", "1/2 #1 (Победитель 1/4 #1 vs Победитель 1/4 #2)", 
                     qf_winners[0] if qf_winners[0] else "Победитель 1/4 #1", 
                     qf_winners[1] if qf_winners[1] else "Победитель 1/4 #2"),
                    ("sf_2", "1/2 #2 (Победитель 1/4 #3 vs Победитель 1/4 #4)", 
                     qf_winners[2] if qf_winners[2] else "Победитель 1/4 #3", 
                     qf_winners[3] if qf_winners[3] else "Победитель 1/4 #4")
                ]
                
                sf_winners, sf_losers = [], []
                for m_key, title, pl1, pl2 in sf_pairs:
                    with st.expander(title, expanded=True):
                        w, l = handle_po_match(m_key, title, pl1, pl2)
                        sf_winners.append(w)
                        sf_losers.append(l)

                st.subheader("🏆 Финальная стадия")
                with st.expander("🥉 Матч за 3-е место", expanded=True):
                    pl1 = sf_losers[0] if sf_losers[0] else "Проигравший 1/2 #1"
                    pl2 = sf_losers[1] if sf_losers[1] else "Проигравший 1/2 #2"
                    m3_w, m3_l = handle_po_match("m3", "Матч за 3-е место", pl1, pl2)
                
                with st.expander("👑 ФИНАЛ", expanded=True):
                    pl1 = sf_winners[0] if sf_winners[0] else "Победитель 1/2 #1"
                    pl2 = sf_winners[1] if sf_winners[1] else "Победитель 1/2 #2"
                    fin_w, fin_l = handle_po_match("final", "Финальный матч", pl1, pl2)

            except Exception as e:
                st.warning("Заполните предыдущие стадии для корректного отображения календаря плей-офф.")

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
            p1A = standings["Группа А"]["Игрок"].iloc[0]
            p2A = standings["Группа А"]["Игрок"].iloc[1]
            p1B = standings["Группа Б"]["Игрок"].iloc[0]
            p2B = standings["Группа Б"]["Игрок"].iloc[1]
            p1V = standings["Группа В"]["Игрок"].iloc[0]
            p2V = standings["Группа В"]["Игрок"].iloc[1]
            p1G = standings["Группа Г"]["Игрок"].iloc[0]
            p2G = standings["Группа Г"]["Игрок"].iloc[1]

            qf_pairs_res = [
                ("qf_1", p1A, p2G), ("qf_2", p1V, p2B), 
                ("qf_3", p1B, p2V), ("qf_4", p1G, p2A)
            ]
            
            playoff_points = {p: 0 for p in st.session_state.players}
            qf_w, qf_l = [], []
            for m_key, pl1, pl2 in qf_pairs_res:
                if m_key in po_scores:
                    d = po_scores[m_key]
                    sc1, sc2, p1_p, p2_p = d["sc1"], d["sc2"], d["p1_panna"], d["p2_panna"]
                    if p1_p:
                        qf_w.append(pl1); qf_l.append(pl2); playoff_points[pl1] += 4
                    elif p2_p:
                        qf_w.append(pl2); qf_l.append(pl1); playoff_points[pl2] += 4
                    elif sc1 > sc2:
                        qf_w.append(pl1); qf_l.append(pl2); playoff_points[pl1] += 3
                    elif sc2 > sc1:
                        qf_w.append(pl2); qf_l.append(pl1); playoff_points[pl2] += 3
                    else:
                        qf_w.append(None); qf_l.append(None)
                else:
                    qf_w.append(None); qf_l.append(None)

            sf_w, sf_l = [], []
            if len(qf_w) == 4 and qf_w[0] and qf_w[1]:
                for idx, m_key in enumerate(["sf_1", "sf_2"]):
                    if m_key in po_scores:
                        pl1 = qf_w[idx*2]
                        pl2 = qf_w[idx*2 + 1]
                        d = po_scores[m_key]
                        sc1, sc2, p1_p, p2_p = d["sc1"], d["sc2"], d["p1_panna"], d["p2_panna"]
                        if p1_p:
                            sf_w.append(pl1); sf_l.append(pl2); playoff_points[pl1] += 4
                        elif p2_p:
                            sf_w.append(pl2); sf_l.append(pl1); playoff_points[pl2] += 4
                        elif sc1 > sc2:
                            sf_w.append(pl1); sf_l.append(pl2); playoff_points[pl1] += 3
                        elif sc2 > sc1:
                            sf_w.append(pl2); sf_l.append(pl1); playoff_points[pl2] += 3
                        else:
                            sf_w.append(None); sf_l.append(None)
                    else:
                        sf_w.append(None); sf_l.append(None)

            third_place, first_place, second_place = "Определяется...", "Определяется...", "Определяется..."
            
            if len(sf_l) == 2 and sf_l[0] and sf_l[1] and "m3" in po_scores:
                pl1, pl2 = sf_l[0], sf_l[1]
                d = po_scores["m3"]
                sc1, sc2, p1_p, p2_p = d["sc1"], d["sc2"], d["p1_panna"], d["p2_panna"]
                if p1_p:
                    third_place = pl1; playoff_points[pl1] += 4
                elif p2_p:
                    third_place = pl2; playoff_points[pl2] += 4
                elif sc1 > sc2:
                    third_place = pl1; playoff_points[pl1] += 3
                elif sc2 > sc1:
                    third_place = pl2; playoff_points[pl2] += 3

            if len(sf_w) == 2 and sf_w[0] and sf_w[1] and "final" in po_scores:
                pl1, pl2 = sf_w[0], sf_w[1]
                d = po_scores["final"]
                sc1, sc2, p1_p, p2_p = d["sc1"], d["sc2"], d["p1_panna"], d["p2_panna"]
                if p1_p:
                    first_place, second_place = pl1, pl2; playoff_points[pl1] += 4
                elif p2_p:
                    first_place, second_place = pl2, pl1; playoff_points[pl2] += 4
                elif sc1 > sc2:
                    first_place, second_place = pl1, pl2; playoff_points[pl1] += 3
                elif sc2 > sc1:
                    first_place, second_place = pl2, pl1; playoff_points[pl2] += 3

            st.header("🏆 Пьедестал почета")
            st.markdown(f"### 🥇 1 МЕСТО: <span style='color:#FF3333;'>{first_place}</span>", unsafe_allow_html=True)
            st.markdown(f"### 🥈 2 МЕСТО: <span style='color:#0F172A;'>{second_place}</span>", unsafe_allow_html=True)
            st.markdown(f"### 🥉 3 МЕСТО: <span style='color:#0F172A;'>{second_place if 'third_place' in locals() else 'Определяется...'}</span>", unsafe_allow_html=True)
            # Переопределение вывода 3 места корректно
            st.markdown(f"### 🥉 3 МЕСТО: <span style='color:#0F172A;'>{third_place}</span>", unsafe_allow_html=True)

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
