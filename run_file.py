
import streamlit as st
import pandas as pd
from sklearn.decomposition import FactorAnalysis
import matplotlib.pyplot as plt
import plotly.graph_objects as go

df = pd.read_csv("./data.csv")
df = df.iloc[:,:31]

questions = [
    "Q1. I usually don't laugh or joke around much with other people.",
    "Q2. If I am feeling depressed, I can usually cheer myself up with humor.",
    "Q3. If someone makes a mistake, I will often tease them about it.",
    "Q4. I let people laugh at me or make fun at my expense more than I should.",
    "Q5. I don't have to work very hard at making other people laugh—I seem to be a naturally humorous person.",
    "Q6. Even when I'm by myself, I'm often amused by the absurdities of life.",
    "Q7. People are never offended or hurt by my sense of humor.",
    "Q8. I will often get carried away in putting myself down if it makes my family or friends laugh.",
    "Q9. I rarely make other people laugh by telling funny stories about myself.",
    "Q10. If I am feeling upset or unhappy I usually try to think of something funny about the situation to make myself feel better.",
    "Q11. When telling jokes or saying funny things, I am usually not very concerned about how other people are taking it.",
    "Q12. I often try to make people like or accept me more by saying something funny about my own weaknesses, blunders, or faults.",
    "Q13. I laugh and joke a lot with my closest friends.",
    "Q14. My humorous outlook on life keeps me from getting overly upset or depressed about things.",
    "Q15. I do not like it when people use humor as a way of criticizing or putting someone down.",
    "Q16. I don't often say funny things to put myself down.",
    "Q17. I usually don't like to tell jokes or amuse people.",
    "Q18. If I'm by myself and I'm feeling unhappy, I make an effort to think of something funny to cheer myself up.",
    "Q19. Sometimes I think of something that is so funny that I can't stop myself from saying it, even if it is not appropriate for the situation.",
    "Q20. I often go overboard in putting myself down when I am making jokes or trying to be funny.",
    "Q21. I enjoy making people laugh.",
    "Q22. If I am feeling sad or upset, I usually lose my sense of humor.",
    "Q23. I never participate in laughing at others even if all my friends are doing it.",
    "Q24. When I am with friends or family, I often seem to be the one that other people make fun of or joke about.",
    "Q25. I don't often joke around with my friends.",
    "Q26. It is my experience that thinking about some amusing aspect of a situation is often a very effective way of coping with problems.",
    "Q27. If I don't like someone, I often use humor or teasing to put them down.",
    "Q28. If I am having problems or feeling unhappy, I often cover it up by joking around, so that even my closest friends don't know how I really feel.",
    "Q29. I usually can't think of witty things to say when I'm with other people.",
    "Q30. I don't need to be with other people to feel amused—I can usually find things to laugh about even when I'm by myself.",
    "Q31. Even if something is really funny to me, I will not laugh or joke about it if someone will be offended.",
]
fact_names = ["Pragmatic","self-Remedial Humorist","Self-Deprecating Humor Enthusiast","Respectful Comedian","Humor Impaired"]

def analyze():
    answer = {}
    grade = "\n1:当てはまらない\n2:あまり当てはまらない\n3:時々当てはまる,\n4:当てはまる\n5:とても当てはまる"
    for q in range(0,31):
        a = st.number_input(questions[q]+grade, min_value=1, max_value=5, step=1)
        answer[f"Q{q+1}"] = [a]

    answer = pd.DataFrame(answer)
    fa = FactorAnalysis(n_components=5, rotation="varimax")
    fa.fit(df)
    score = fa.transform(answer)
    score = pd.DataFrame(score)
    score.columns = fact_names

    return score

# Streamlit UI
st.title("Humour Characteristics Analysis App")
st.text("次の問題に答えてください")

# Function call
score = analyze()

# Streamlit UI
st.title("This is Your Humour Characteristics ")
st.write(score)


st.subheader("Scores:")
for idx, col in enumerate(score.columns):
    st.write(
        f"**{col}:** {score.iloc[0, idx]}"
    )
# # Run the analysis when the button is clicked
# if st.button("Run Analysis",key="Analysis"):
#     score = analyze()
#     # st.write("Factor Scores:")
#     # st.write(score)


st.write("## Radar Chart for Scores")
fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      r=score.iloc[0].tolist(),
      theta=score.columns.tolist(),
      fill='toself'
))

fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
st.plotly_chart(fig, use_container_width=True)

