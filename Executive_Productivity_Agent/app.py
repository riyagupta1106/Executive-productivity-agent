import streamlit as st
import pandas as pd
st.title("Executive AI Dashboard")

#LOADING THE DATAFRAMES AND CSV FILES REQUIRED
df = pd.read_csv("data/task.csv")
emails_df = pd.read_csv("data/emails.csv")
meetings_df = pd.read_csv("data/meetings.csv")
calendar_df = pd.read_csv("data/calendar.csv")
voice_df = pd.read_csv("data/voice_notes.csv")
people_df = pd.read_csv("data/people.csv")
threads_df = pd.read_csv("data/threads.csv")
st.set_page_config(page_title="Executive Productivity Agent", layout="wide")
open_tasks = len(df[df["Status"] == "Open"])
waiting_tasks = len(df[df["Status"] == "Waiting"])
risk_tasks = len(df[df["Status"] == "Risk"])


# STREAMLIT APPLICATION


st.markdown("""
<style>
.metric-card{
    background:#FFFFFF;
    padding:10px 14px;
    border-radius:12px;
    border:1px solid #E5E7EB;
    box-shadow:0 1px 4px rgba(0,0,0,0.04);
    margin:4px 0px;
}

.metric-title{
    color:#6B7280;
    font-size:12px;
    font-weight:600;
    margin-bottom:2px;
}

.metric-value{
    color:#2563EB;
    font-size:24px;
    font-weight:700;
    line-height:1;
}

</style>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title"> Open Tasks</div>
        <div class="metric-value">{open_tasks}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title"> Waiting</div>
        <div class="metric-value">{waiting_tasks}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title"> Risks</div>
        <div class="metric-value">{risk_tasks}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Meetings</div>
        <div class="metric-value">{len(meetings_df)}</div>
    </div>
    """, unsafe_allow_html=True)



menu = st.sidebar.selectbox(
    "Choose Section",
[
"Daily Brief",
"All Tasks",
"My Actions",
"Waiting On Others",
"Risks",
"Ask Agent",
"People",
"Emails",
"Meetings",
"Calendar",
"Threads",
"Voice Notes"
] )

if menu == "Ask Agent":

    st.header("Ask the Agent")

    question = st.text_input("Ask a question")

    if question:

        q = question.lower()

        if "raghav" in q:
            raghav_tasks = df[df["Task"].str.contains("vendor", case=False)]
            st.success("Related task:")
            st.dataframe(raghav_tasks)
        elif "waiting" in q or "wait" in q:
             waiting = df[df["Status"] == "Waiting"]
             st.success("Waiting on:")
             for task in waiting["Task"]:
                st.write("•", task)
        elif "meeting" in q:
            st.dataframe(meetings_df)
            
        elif "calendar" in q:
            st.dataframe(calendar_df)
        elif "voice" in q:
            st.dataframe(voice_df)
            
        elif "people" in q or "contact" in q:
             st.dataframe(people_df)

        elif "risk" in q:
             risks = df[df["Status"] == "Risk"]
             st.success("Current Risks:")
             st.dataframe(risks)

        elif "action" in q:
             actions = df[df["Owner"] == "Arjun"]
             st.success("Your actions:")
             st.dataframe(actions)

        elif "email" in q:
             person = people_df[
             people_df["Name"].str.lower().isin(q.split())]

             if not person.empty:
                 st.dataframe(person)
             else:
                st.warning("Person not found.")

        else:
            st.warning("No information found.")
elif menu == "Threads":

    st.subheader("🧵 Communication Threads")

    display_threads = threads_df.copy()

    display_threads["Status"] = display_threads["Status"].replace({
        "Open": "🟢 Open",
        "Waiting": "🟡 Waiting",
        "Risk": "🔴 Risk"
    })

    st.dataframe(
        display_threads,
        width="stretch",
        hide_index=True
    )
elif menu == "People":

    st.subheader("People & Contacts")

    for _, row in people_df.iterrows():

        with st.container(border=True):

            name = row.get("Name", "Unknown")
            role = row.get("Role", "N/A")

            st.markdown(
                f"""
                <div style="
                background:#F8FAFC;
                padding:15px;
                border-radius:12px;
                border-left:6px solid #8B5CF6;">
                <h3>{name}</h3>
                <p>{role}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if "Email" in people_df.columns:
                st.write(f"📧 {row['Email']}")

            if "Phone" in people_df.columns:
                st.write(f"📱 {row['Phone']}")

            if "Company" in people_df.columns:
                st.write(f"🏢 {row['Company']}")

            st.divider()
elif menu == "Emails":

    st.subheader("Emails")

    for _, row in emails_df.iterrows():

        with st.container(border=True):

            subject = row.get("Subject", "No Subject")
            sender = row.get("Sender", "Unknown")

            st.markdown(
                f"""
                <div style="
                background:#F8FAFC;
                padding:15px;
                border-radius:12px;
                border-left:6px solid #2563EB;
                ">
                <h4>📧 {subject}</h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(f"👤 From: {sender}")

            if "Priority" in emails_df.columns:
                st.write(f"⚡ Priority: {row['Priority']}")

            if "Summary" in emails_df.columns:
                st.write(f"📝 Summary: {row['Summary']}")

            if "Body" in emails_df.columns:
                st.write(f"📄 {row['Body']}")

            st.divider()
elif menu == "Meetings":

    st.subheader("Meetings")

    for _, row in meetings_df.iterrows():

        with st.container(border=True):

            meeting = row.get("Meeting", "Meeting")
            date = row.get("Date", "N/A")
            time = row.get("Time", "N/A")

            st.markdown(
                f"""
                <div style="
                    background-color:#EEF4FF;
                    padding:15px;
                    border-radius:12px;
                    border-left:6px solid #2563EB;">
                    <h2>{meeting}</h2>
                    <p><b>Date:</b> {date}</p>
                    <p><b>Time:</b> {time}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            if "Attendees" in meetings_df.columns:

                st.markdown("### Attendees")

                for person in str(row["Attendees"]).split(";"):
                    st.info(person.strip())

            if "Action_Items" in meetings_df.columns:

                st.markdown("### Action Items")

                for action in str(row["Action_Items"]).split(";"):
                    st.checkbox(action.strip())

            if "Risks" in meetings_df.columns:

                st.markdown("### Risks")

                for risk in str(row["Risks"]).split(";"):
                    st.warning(risk.strip())

            st.divider()

elif menu == "Calendar":

    st.subheader("Calendar")

    st.dataframe(
        calendar_df,
        width="stretch"
    )
elif menu == "Voice Notes":

    st.subheader("Voice Notes")

    st.dataframe(
        voice_df,
        width="stretch"
    )
elif menu== "All Tasks":

    st.subheader("All Tasks")

    display_df = df.copy()
    search = st.text_input("Search Tasks")
    if search:
        display_df = display_df[
        display_df["Task"].str.contains(search, case=False)
    ]

    display_df["Status"] = display_df["Status"].replace({
        "Open":"🔵 Open",
        "Waiting":"🟡 Waiting",
        "Risk":"🔴 Risk",
        "Done":"🟢 Done"
    })

    st.dataframe(
        display_df.sort_values("DueDate"),
        width="stretch"
    )
elif menu == "Daily Brief":
    st.markdown("""
<div style="
background:linear-gradient(135deg,#2563EB,#3B82F6);
padding:10px 16px;
border-radius:12px;
margin:10px 0 15px 0;
color:white;
box-shadow:0 2px 6px rgba(37,99,235,0.15);
">
<h3 style="margin:0;"> Daily Executive Brief</h3>
<p style="margin:2px 0 0 0;font-size:13px;">
Today's executive priorities and risks
</p>
</div>
""", unsafe_allow_html=True)

    actions = df[df["Owner"] == "Arjun"]
    waiting = df[df["Status"] == "Waiting"]
    risks = df[df["Status"] == "Risk"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title"> Open Actions</div>
            <div class="metric-value">{len(actions)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title"> Waiting Items</div>
            <div class="metric-value">{len(waiting)}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Risks</div>
            <div class="metric-value">{len(risks)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("Today's Priorities")

    for _, row in actions.iterrows():
        st.info(f"{row['Task']} | Due: {row['DueDate']}")

    st.subheader("Waiting On Others")

    st.dataframe(
        waiting[["Task","Owner","Waiting_For","DueDate"]],
        width="stretch"
    )

    st.subheader("Risks")

    for _, row in risks.iterrows():
        st.error(row["Task"])

elif menu == "My Actions":
    st.subheader("My Actions")
    st.dataframe(df[df["Owner"] == "Arjun"])

elif menu == "Waiting On Others":
    st.subheader("Waiting On Others")
    st.dataframe(df[df["Status"] == "Waiting"])

elif menu == "Risks":
    st.subheader("Risks")
    st.dataframe(df[df["Status"] == "Risk"])