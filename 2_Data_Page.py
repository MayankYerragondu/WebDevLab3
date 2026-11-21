# Lab 3: API data page
# TODO: Rename this file to fit your page. Keep the number at the front, since it sets the
#       page's order in the sidebar (for example, 2_Pokedex.py).
#
# This page shows data from your API, processed with your own Python code. No AI on this page.
# It should have:
#   - at least 2 meaningful user inputs (for example st.selectbox, st.text_input, st.slider)
#   - at least 2 dynamic visuals that change based on the user's input: charts, displays of
#     images, or other visualizations (see the example website for examples!)
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Undergraduate Research Lab Finder", page_icon="🔬", layout="wide")
st.header("🔬NIH Research Explorer🔬", divider="violet")
st.write("""
Discover biomedical research, explore faculty investigators,
and compare NIH-funded projects across universities.
""")
st.badge("NIH Database", color="violet")
st.badge("Biomedical Research", color="blue")
st.badge("Pre-Med", color="green")
st.divider()
validTopics = ["neuroscience","genetics","cancer","cancer biology","immunology","biomedical engineering","cardiology","neurology","microbiology","biochemistry","molecular biology","cell biology","pharmacology","epidemiology","infectious diseases","public health","stem cells","diabetes","mental health","regenerative medicine"]
# USER INPUTS
st.header("🔎 Find Research Projects", divider="blue")
st.write("Research Projects Are Available In The Following Areas")
for i in range(len(validTopics)):
    st.markdown(f"- {validTopics[i].title()}")
st.write("Choose a topic from the list above")
col1, col2 = st.columns(2)
with col1:
    researchTopic=st.text_input("Research Topic", value="", placeholder="e.g., neuroscience, genetics, cancer")
    universityList = ["All institutions", "Emory University", "Georgia Institute of Technology", "University of Georgia"]
    selectedUniversity = st.selectbox("Choose a university", universityList, index=None, placeholder="Select a university")
with col2:
    fiscalYear = st.selectbox("Fiscal year", [2025, 2024, 2023], index=None, placeholder="Select a fiscal year")
    st.info("💡 Tip: Try searching for neuroscience, "
        "cancer biology, or genetics!")
st.divider()

# NIH API Request code:
@st.cache_data(ttl=3600)
def getProjects(topic, university, year):
    criteria = {"fiscal_years": [year]}
    if topic.strip() != "":
        criteria["advanced_text_search"] = {
            "operator": "and",
            "search_field": "all",
            "search_text": topic.strip()
        }
    if university != "All institutions":
        criteria["org_names"] = [university]
    payload = {"criteria": criteria, "offset": 0, "limit": 500}
    response = requests.post(
        "https://api.reporter.nih.gov/v2/projects/search",
        json=payload,
        timeout=25
    )
    response.raise_for_status()
    return response.json().get("results", [])

if selectedUniversity is None or fiscalYear is None:
    st.info("Please select a university and fiscal year.")
    st.stop()
if researchTopic.strip() != "" and researchTopic.lower().strip() not in validTopics:
    st.warning("Please enter a valid biomedical research topic.")
    st.stop()
if researchTopic.strip() == "" and selectedUniversity == "All institutions":
    st.info("Enter a research topic or select a university to narrow your search.")
    st.stop()
else:
    try:
        apiProjects = getProjects(researchTopic, selectedUniversity, fiscalYear)
    except requests.RequestException as error:
        st.error("Could not load NIH project data. Check your internet connection or search criteria.")
        st.caption(str(error))
        st.stop()
    # PROCESS API JSON USING OUR OWN PYTHON CODE
    projectList = []
    for project in apiProjects:
        investigatorNames = []
        for investigator in (project.get("principal_investigators") or []):
            investigatorNames.append(investigator.get("full_name") or "Unknown")
        organization = project.get("organization") or {}
        funding = project.get("award_amount") or 0
        projectList.append({
            "Project Title": project.get("project_title") or "Untitled",
            "Principal Investigator": ", ".join(investigatorNames) or "Not listed",
            "Institution": organization.get("org_name") or "Not listed",
            "Funding ($)": funding,
            "Fiscal Year": project.get("fiscal_year") or fiscalYear,
            "Abstract": project.get("abstract_text") or "No abstract available"
        })
    st.metric("Projects returned", len(projectList))
    if len(projectList) == 0:
        st.warning("No projects found. Try a broader topic or another university.")
        st.stop()
    # PROJECT DETAILS
    st.subheader("Research Project Details")
    projectNames = []
    for i in range(len(projectList)):
        projectNames.append(str(i + 1) + ". " + projectList[i]["Project Title"])
    selectedProject = st.selectbox("Select a research project", projectNames)
    selectedIndex = projectNames.index(selectedProject)
    chosen = projectList[selectedIndex]
    st.write("**Principal Investigator:**", chosen["Principal Investigator"])
    st.write("**Institution:**", chosen["Institution"])
    st.write("**NIH Funding:**", "${:,.0f}".format(chosen["Funding ($)"]))
    st.write("**Fiscal Year:**", chosen["Fiscal Year"])
    st.write("**Abstract:**", chosen["Abstract"])
    
    # DYNAMIC VISUAL 1: NIH funding for selected projects
    st.subheader("NIH Funding by Project")
    numberToShow = st.slider("Number of projects to compare", 1, min(len(projectList), len(projectList)), min(len(projectList), len(projectList)))
    fundingData = []
    for i in range(numberToShow):
        fundingData.append({"Project": projectList[i]["Project Title"], "Funding ($)": projectList[i]["Funding ($)"]})
    fundingDF = pd.DataFrame(fundingData)
    st.bar_chart(fundingDF, x="Project", y="Funding ($)")
    st.caption("Project numbers correspond to the first projects returned by NIH. A missing funding amount is displayed as zero.")
    
    # DYNAMIC VISUAL 2: Count projects per institution
    st.subheader("Research Projects by Institution")
    institutionCounts = {}
    for project in projectList:
        institution = project["Institution"]
        if institution not in institutionCounts:
            institutionCounts[institution] = 0
        institutionCounts[institution] += 1
    institutionData = []
    for institution in institutionCounts:
        institutionData.append({"Institution": institution, "Number of Projects": institutionCounts[institution]})
    institutionDF = pd.DataFrame(institutionData)
    institutionDF = institutionDF.sort_values("Number of Projects", ascending=False).head(15)
    st.bar_chart(institutionDF, x="Institution", y="Number of Projects")
    st.caption("Counts are based on the first 100 matching API records, not all NIH projects.")
    st.subheader("Compare Research Projects")
    comparisonNames = st.multiselect("Choose projects to compare", projectNames, default=[], placeholder="Select projects to compare")
    comparisonList = []
    for name in comparisonNames:
        index = projectNames.index(name)
        comparisonList.append(projectList[index])
    if len(comparisonList) > 0:
        comparisonDF = pd.DataFrame(comparisonList)
        st.dataframe(comparisonDF.drop(columns=["Abstract"]), use_container_width=True)