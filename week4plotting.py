import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

success_string = """
0.82979212
0.19645161
0.2932987
0.24947262
0.15058733
0.29283039
0.27052659
0.19869256
0.41809063
0.5129112
0.14208549
0.43094925
0.12872199
0.05018694
0.14933936
0.54031591
0.42177084
0.26600326
0.28457247
0.23699764
0.34309186
0.86981466
0.23099189
0.39810677
0.90916973
0.27825307
0.42259499
0.38058399
0.13115613
1.0408997
0.02923584
0.72276217
0.23658223
0.45860505
0.22900213
0.01130275
0.36317806
0.19054801
0.32718698
0.2893753
0.04709701
0.2742501
0.35121273
0.06190559
0.21834235
0.78725222
0.28048041
0.24679788
0.95756843
0.40505829
0.24483405
0.04809197
0.24015377
0.00278233
0.21075369
0.37762915
0.32718698
0.01130275
0.36283477
0.1514081
0.28457247
0.01130275
0.14123126
0.17848087
0.19645161
0.2471835
0.21844382
0.06572381
0.05806364
"""
failure_string = """
0.13979679
0.34956851
0.39760298
0.25224568
0.18565343
0.16088654
0.18828622
0.53647832
0.19721238
0.58917457
0.86118901
0.18544103
0.13384477
0.28983871
0.25224568
0.14251213
0.06470221
0.03078543
0.21352143
0.40447661
0.2398476
0.21834235
0.03078543
0.34326297
0.21834235
0.03228126
0.19959471
0.6622971
0.23630017
0.32687157
0.87606612
0.36516341
0.25934622
0.14087584
0.58857402
"""
success_scores = np.fromstring(success_string, sep='\n')
failure_scores = np.fromstring(failure_string, sep='\n')

# Create DataFrames from each
success_df = pd.DataFrame({'score': success_scores, 'label': 'success'})
failure_df = pd.DataFrame({'score': failure_scores, 'label': 'failure'})

# Combine into one DataFrame
df = pd.concat([success_df, failure_df], ignore_index=True)

# Streamlit UI
st.title("Filter Successes and Failures by Score")
cutoff = st.slider("Minimum Score Threshold", min_value=0.0, max_value=2.0, value=0.5, step=0.01)

filtered_success = success_scores[success_scores >= cutoff]
filtered_failure = failure_scores[failure_scores >= cutoff]

# Filter based on the threshold
filtered_df = df[df['score'] >= cutoff]

# Plot using Plotly
fig = px.scatter(
    filtered_df,
    x='score',
    y='label',
    color='label',
    color_discrete_map={'success': 'green', 'failure': 'red'},
    title=f"Scores ≥ {cutoff}",
    labels={'score': 'Score', 'label': 'Category'}
)
st.write(f"✅ Successes: {len(filtered_success)} / {len(success_scores)}")
st.write(f"❌ Failures: {len(filtered_failure)} / {len(failure_scores)}")
st.plotly_chart(fig)

# ---- Ratio vs. Threshold Line Graph ----
thresholds = np.linspace(0, 1, 100)
ratios = []
for t in thresholds:
    succ = np.sum(success_scores >= t)
    fail = np.sum(failure_scores >= t)
    ratio = (succ/len(success_scores)) / (fail/len(failure_scores)) if fail != 0 else np.nan
    ratios.append(ratio)

# Plot ratio line
fig1, ax1 = plt.subplots()
ax1.plot(thresholds, ratios, label='Success/Failure Ratio', color='purple')
ax1.axvline(cutoff, color='blue', linestyle='dashed', linewidth=1, label='Selected Threshold')
ax1.set_xlabel("Threshold")
ax1.set_ylabel("Success / Failure Ratio")
ax1.set_title("Success-to-Failure Ratio vs. Threshold")
ax1.legend()
st.pyplot(fig1)

# ---- Histogram for visual reference ----
fig2, ax2 = plt.subplots()
ax2.hist(filtered_success, bins=20, alpha=0.7, label='Successes', color='green')
ax2.hist(filtered_failure, bins=20, alpha=0.7, label='Failures', color='red')
ax2.axvline(cutoff, color='blue', linestyle='dashed', linewidth=2)
ax2.set_title("Histogram of Scores Above Threshold")
ax2.set_xlabel("Score")
ax2.set_ylabel("Count")
ax2.legend()
st.pyplot(fig2)

# Table of filtered scores above the threshold

st.subheader("Filtered Scores")
st.dataframe(filtered_df)