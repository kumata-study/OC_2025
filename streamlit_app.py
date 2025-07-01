import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="ネットワーク問題体験", layout="centered")

# 初期化
if "page" not in st.session_state:
    st.session_state.page = "top"

# ページ遷移関数
def go_to(page_name):
    st.session_state.page = page_name
    st.experimental_rerun()

# トップページ
if st.session_state.page == "top":
    st.title("ネットワークの謎を解け！")
    st.subheader("〜最短経路と最大流チャレンジ〜")
    st.markdown("🚀 限られた時間と資源をどう使う？\
                最適ルートや最大限の輸送量を探してみよう！")
    if st.button("▶ スタート"):
        go_to("shortest")


# 最短経路問題
elif st.session_state.page == "shortest":
    st.header("問題①：最短経路を探せ！")
    st.markdown("AからFまで、所要時間が最も短くなる経路を選んでください。")

    # グラフ描画
    G = nx.Graph()
    edges = [("A", "B", 2), ("A", "C", 4), ("B", "D", 7),
             ("C", "D", 1), ("D", "E", 3), ("E", "F", 2)]
    G.add_weighted_edges_from(edges)
    pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color='lightblue', ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    st.pyplot(fig)

    answer = st.radio("あなたが考える最短経路は？", 
                      ["A-B-D-E-F", "A-C-D-E-F", "A-B-C-D-E-F"])
    if st.button("解答する"):
        if answer == "A-C-D-E-F":
            st.success("正解！Dijkstra法でもそのルートが最短です。")
        else:
            st.error("残念、もう一度考えてみましょう。")
        st.button("次へ", on_click=lambda: go_to("maxflow"))

# 最大流問題
elif st.session_state.page == "maxflow":
    st.header("問題②：最大流を求めよ！")
    st.markdown("以下のネットワークで、A→Fの最大流はいくつになるか？")

    # 流量付きグラフ
    G = nx.DiGraph()
    G.add_edge("A", "B", capacity=10)
    G.add_edge("A", "C", capacity=5)
    G.add_edge("B", "D", capacity=4)
    G.add_edge("C", "D", capacity=8)
    G.add_edge("D", "F", capacity=10)

    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots()
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', ax=ax)
    edge_labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    st.pyplot(fig)

    flow_guess = st.number_input("最大流は何ですか？", min_value=0)
    if st.button("答え合わせ"):
        # Ford-Fulkersonで正答確認
        flow_value, _ = nx.maximum_flow(G, "A", "F")
        if flow_guess == flow_value:
            st.success(f"正解！最大流は {flow_value} です。")
        else:
            st.warning(f"惜しい！正解は {flow_value} です。")
        st.button("結果と解説を見る", on_click=lambda: go_to("summary"))

# 解説ページ
elif st.session_state.page == "summary":
    st.header("📝 結果と解説")

    st.markdown("""
    **最短経路**  
    - 解法：Dijkstra法（重み付きグラフに有効）
    - 応用例：ナビアプリ、避難経路の設計など

    **最大流**  
    - 解法：Ford-Fulkerson法（増加パスを探して繰り返し）
    - 応用例：物流ネットワーク設計、サーバの通信設計など
    """)

    st.success("経営工学や情報科学の世界では、このような数学が社会課題の解決に直結します！")

    st.markdown("👋 ご参加ありがとうございました！")


