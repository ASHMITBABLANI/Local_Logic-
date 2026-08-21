# AirGuard AI — Air Pollution Predictive Chatbot
### CODEMANIA 2026 • Round 02 • Sample Submission

---

## 2. PROBLEM STATEMENT

Air pollution is one of the most pressing public health and environmental challenges faced by urban populations today, particularly in cities where seasonal factors — such as post-monsoon stubble burning, vehicular emissions, construction dust, and temperature inversions — cause sharp spikes in pollutant concentration (PM2.5, PM10, NO₂, SO₂, CO, O₃).

A specific and recurring pattern is the **sharp deterioration in air quality that follows the autumnal equinox** (roughly late September through winter), when cooler surface temperatures trap pollutants closer to the ground (a phenomenon known as **temperature inversion**), combined with reduced wind speed and increased crop-residue burning. Citizens — especially children, the elderly, outdoor workers, and people with respiratory conditions — are exposed to hazardous air quality without timely, personalized, and actionable guidance on what to do.

**Who faces it:** General urban residents, vulnerable groups (asthma/COPD patients, elderly, children, pregnant women), outdoor workers, schools, and local health/civic authorities.

**Why it matters:** Prolonged exposure to poor air quality is linked to respiratory illness, cardiovascular disease, reduced life expectancy, and increased healthcare burden. Most existing tools report *current* AQI but do not explain *why* the pollution is rising after seasonal transitions like the equinox, nor do they give **clear, personalized preventive action** in real time.

---

## 3. PROBLEM UNDERSTANDING

**Context:**
As seasons shift post-equinox, meteorological conditions (lower temperatures, calmer winds, temperature inversion layers) trap pollutants near the surface. Combined with human activity (crop burning, festival fireworks, heating), AQI levels can spike suddenly and stay elevated for days or weeks.

**Target Users / Stakeholders:**
- General public seeking daily guidance on outdoor activity, commuting, and exercise
- Vulnerable groups needing tailored health precautions
- Schools and offices deciding on outdoor activity/closures
- Local municipal and health authorities monitoring public advisories

**Existing Pain Points:**
- AQI apps show numbers (e.g., "AQI: 320") without explaining causes or practical next steps
- Generic advisories aren't personalized to age, health condition, or activity type
- No conversational, on-demand interface — users must interpret raw data themselves
- Poor awareness of *why* pollution worsens after seasonal transitions (equinox effect), reducing preparedness
- Delayed or infrequent government advisories compared to real-time pollution changes

**Key Assumptions:**
- Users have access to a smartphone/browser with internet connectivity
- Government/open AQI APIs (e.g., CPCB, IQAir, OpenWeather Air Pollution API) provide reasonably reliable real-time and historical data
- Users are willing to share basic profile info (age group, health condition) for personalized advice

**Gap Addressed:**
A conversational, predictive assistant that not only reports AQI but **forecasts short-term trends**, explains the **underlying seasonal/meteorological cause**, and gives **personalized, actionable preventive measures** — closing the gap between raw data and user understanding/action.

---

## 4. PROPOSED SOLUTION

**AirGuard AI** is a predictive air-quality chatbot that combines real-time pollution data, short-term forecasting, and conversational AI to explain rising pollution trends (e.g., post-equinox spikes) and recommend preventive measures tailored to the user.

**Main Idea:**
The chatbot ingests live AQI/meteorological data for a user's location, runs a predictive model to forecast AQI for the next 24–72 hours, and uses a natural-language layer to explain *why* pollution is expected to rise or fall — then generates a personalized action checklist.

**How It Works:**
1. User shares location (and optionally age/health profile).
2. System fetches current + historical AQI and weather data via API.
3. A forecasting model predicts near-term AQI trend.
4. A rule/NLP layer maps the trend + season + causal factors (e.g., temperature inversion, stubble burning season) into a plain-language explanation.
5. Chatbot responds conversationally with forecast, cause, and preventive measures.

**Key Features:**
- **Conversational interface** — ask "Why is the air bad today?" or "Should I go for a run tomorrow morning?"
- **Short-term AQI forecasting** (next 1–3 days)
- **Cause explanation engine** — links spikes to seasonal/meteorological triggers (e.g., equinox-driven inversion, crop burning windows)
- **Personalized preventive recommendations** — mask usage, activity timing, ventilation tips, medication reminders for at-risk users
- **Proactive alerts** — push notification when AQI crosses unsafe thresholds

**Why It Addresses the Problem:**
It converts a passive, numeric AQI reading into an understandable, personalized, and actionable conversation — directly closing the awareness-to-action gap, especially during high-risk seasonal windows like post-equinox months.

---

## 5. DOMAIN-SPECIFIC APPROACH (AI / ML)

**Data:**
The model uses a structured, user-input pollutant dataset with the following 14 fields:

| Field | Description |
|---|---|
| PM2.5 | Fine particulate matter (≤2.5 µm), µg/m³ |
| PM10 | Coarse particulate matter (≤10 µm), µg/m³ |
| NO | Nitric oxide concentration |
| NO2 | Nitrogen dioxide concentration |
| NOx | Total nitrogen oxides |
| NH3 | Ammonia concentration |
| CO | Carbon monoxide concentration |
| SO2 | Sulphur dioxide concentration |
| O3 | Ground-level ozone concentration |
| Benzene | Benzene concentration (VOC) |
| Toluene | Toluene concentration (VOC) |
| Xylene | Xylene concentration (VOC) |
| AQI | Computed/reported Air Quality Index (target variable) |
| Rank | Severity category/rank derived from AQI (e.g., Good, Moderate, Poor, Severe, Hazardous) |

These values are collected directly as **user input** (either manually entered by the user or auto-filled from a connected AQI monitoring source), rather than fetched live from an external API — making the system usable even in areas with sparse official sensor coverage, as long as the user has access to a local reading (e.g., from a personal air-quality monitor or a nearby station report).

- **Features (inputs):** PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene
- **Targets:** AQI (regression) and Rank (classification/severity band)
- Historical records of these same fields (past days/months) are used to train the forecasting model and detect seasonal trend shifts (e.g., post-equinox spikes)
- Optional supplementary data: meteorological data (temperature, humidity, wind speed) and calendar/season context, to strengthen the cause-explanation module if available

**AI/ML Task:**
- **Regression** — predict AQI value from the 12 pollutant-concentration inputs (PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene)
- **Classification** — predict the severity **Rank**/band (e.g., Good/Moderate/Poor/Severe/Hazardous) from the same inputs, either directly or derived from the predicted AQI
- **(Optional) Time-series extension** — if historical user-entered readings are logged over time, a secondary forecasting task can predict next-day AQI/Rank trend
- **NLP (intent recognition + response generation)** for the chatbot conversational layer

**Proposed Model / Approach:**
- Regression: models such as Random Forest Regressor, XGBoost/LightGBM, or a simple feed-forward neural network trained on the 12 pollutant fields to predict AQI
- Classification: a classifier (Random Forest / Logistic Regression / Gradient Boosting) trained on the same features to predict Rank, or a rule-based mapping applied to the predicted AQI using standard CPCB/AQI breakpoints
- Preprocessing: handling missing pollutant readings (imputation), scaling/normalizing concentration units, and correlation analysis to identify which pollutants dominate the AQI/Rank prediction
- Conversational layer: an LLM (e.g., via Claude/GPT API) that receives the user's entered pollutant values + predicted AQI/Rank and generates a natural-language explanation of which pollutants are driving the reading, plus personalized preventive measures
- Personalization: rule-based layer that adjusts recommendations based on user profile (age, respiratory condition, outdoor activity plans)

**Workflow:**
```
User Inputs Pollutant Readings (PM2.5, PM10, NO, NO2, NOx, NH3, CO, SO2, O3, Benzene, Toluene, Xylene)
   → Preprocessing (validation, scaling, missing-value handling)
   → Regression Model → Predicted AQI
   → Classification Model → Predicted Rank/Severity Band
   → Cause-Tagging Module (identifies dominant contributing pollutants + seasonal context, e.g. post-equinox inversion)
   → LLM Response Generator (AQI + Rank + cause + personalized preventive measures)
   → Chatbot Reply to User
```

**Expected Output:**
A conversational reply such as:
> "Based on the values you entered, your predicted AQI is 312 (Rank: Very Poor), driven mainly by high PM2.5 and NOx levels — consistent with the post-equinox temperature inversion trapping pollutants near the ground. Avoid outdoor exercise after 6 PM, wear an N95 mask outdoors, and keep windows closed during early morning hours."

**Limitations:**
- Prediction accuracy depends on the correctness and completeness of the user-entered pollutant values (manual entry can introduce errors)
- No live/continuous sensor feed by default — readings reflect only the moment the user inputs them, not a continuous stream
- Cause-attribution (which pollutant + which seasonal factor) is heuristic, not a certified causal analysis
- Model needs a reasonably sized, representative historical dataset (with these same 14 fields) for good regression/classification accuracy
- Requires periodic retraining as pollution patterns and standards evolve

---

## 6. IMPLEMENTATION / DEMONSTRATION

*(Include the following, labelled clearly, as applicable to your actual build):*
- Chatbot UI screenshots (chat interface showing a sample conversation and AQI forecast)
- Architecture diagram (data pipeline → model → chatbot)
- Sample forecast chart (predicted vs. actual AQI over a week)
- Code snippet of the forecasting model training/inference
- Notebook output showing model evaluation metrics (RMSE/MAE)

**Supporting Links (include only what is applicable, ensure access is enabled):**
- GitHub Repository: `<insert link>`
- Google Colab Notebook (model training): `<insert link>`
- Live Demo / Dashboard: `<insert link>`
- Demo Video: `<insert link>`

---

## 7. EXPECTED IMPACT

**Who Benefits:**
- General citizens get clear, timely, personalized guidance instead of confusing raw numbers
- Vulnerable groups (asthma/COPD patients, elderly, children) receive tailored preventive alerts, reducing health risk
- Schools/offices can make informed decisions about outdoor activities
- Local authorities gain a citizen-facing tool that complements official advisories

**What Improves:**
- Faster, clearer understanding of *why* pollution is rising, especially during seasonal high-risk windows
- Increased adoption of preventive behavior (mask usage, activity rescheduling, ventilation practices)
- Reduced short-term health incidents linked to acute pollution exposure

**Measurable Impact:**
- Potential reduction in AQI-related hospital/ER visits during high-pollution weeks (trackable via public health data correlation)
- Increased user engagement with preventive actions (measurable via in-app action completion/acknowledgment rates)
- Improved public awareness scores (via periodic user surveys on understanding of pollution causes)

---

## 8. LIMITATIONS & FUTURE SCOPE

**Current Limitations:**
- Dependent on third-party AQI/weather API accuracy, coverage, and update frequency
- Forecasting model needs a substantial historical dataset for reliable multi-day predictions
- Cause-explanation relies on heuristic tagging rather than deep causal modeling
- No hyperlocal sensor network yet — city/region-level granularity only
- Chatbot cannot yet account for indoor air quality (which also matters for exposure)

**Future Scope:**
- Integrate low-cost IoT air-quality sensors for hyperlocal, street-level predictions
- Expand forecasting horizon (up to 7 days) using more advanced spatiotemporal models (e.g., Graph Neural Networks across monitoring stations)
- Add indoor AQI monitoring and HVAC/purifier recommendations
- Partner with health systems to correlate pollution spikes with real-time hospital admission data for validated impact measurement
- Multilingual voice-based chatbot support for wider accessibility
- Push proactive, geofenced alerts integrated with wearables (e.g., notify asthma patients before they step outdoors into poor air)

---
