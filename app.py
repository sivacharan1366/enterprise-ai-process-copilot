import streamlit as st
from dotenv import load_dotenv

from src.rag import generate_rag_response
from src.workflow import (
    create_laptop_request,
    get_requests,
    get_pending_requests,
    update_request_status,
)


load_dotenv()


st.set_page_config(
    page_title="Enterprise AI Process Copilot",
    page_icon="🤖",
    layout="centered"
)


st.title("🤖 Enterprise AI Process Copilot")

st.caption(
    "AI assistant powered by enterprise knowledge and business workflows"
)


# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("⚙️ Process Actions")

    if st.button("💻 New Laptop Request"):

        st.session_state.show_laptop_form = True

    st.divider()

    st.subheader("📊 Request Summary")

    requests = get_requests()

    total = len(requests)

    pending = len(
        [
            r for r in requests
            if r["status"] == "Pending Manager Approval"
        ]
    )

    approved = len(
        [
            r for r in requests
            if r["status"] == "Approved"
        ]
    )

    completed = len(
        [
            r for r in requests
            if r["status"] == "Completed"
        ]
    )

    st.metric("Total Requests", total)
    st.metric("Pending Approval", pending)
    st.metric("Approved", approved)
    st.metric("Completed", completed)


# -----------------------------
# Laptop Request Form
# -----------------------------

if st.session_state.get(
    "show_laptop_form",
    False
):

    st.header("💻 Laptop Request")

    st.info(
        "Submit a laptop request according to "
        "the IT Equipment Policy."
    )

    with st.form("laptop_request_form"):

        employee_name = st.text_input(
            "Employee Name"
        )

        department = st.text_input(
            "Department"
        )

        reason = st.text_area(
            "Reason for Request"
        )

        specifications = st.text_area(
            "Required Specifications",
            placeholder="Example: 16GB RAM, 512GB SSD"
        )

        submitted = st.form_submit_button(
            "Submit Request"
        )

        if submitted:

            if not employee_name:
                st.error(
                    "Please enter the employee name."
                )

            elif not department:
                st.error(
                    "Please enter the department."
                )

            elif not reason:
                st.error(
                    "Please provide the reason."
                )

            elif not specifications:
                st.error(
                    "Please provide the required specifications."
                )

            else:

                request = create_laptop_request(
                    employee_name=employee_name,
                    department=department,
                    reason=reason,
                    specifications=specifications
                )

                st.success(
                    "Laptop request created successfully!"
                )

                st.write(
                    f"### Request ID: `{request['request_id']}`"
                )

                st.write(
                    f"**Status:** {request['status']}"
                )

                st.session_state.show_laptop_form = False
# -----------------------------
# Manager Approval Dashboard
# -----------------------------

st.header("👨‍💼 Manager Approval")

pending_requests = get_pending_requests()

if not pending_requests:

    st.success(
        "No requests are currently waiting for approval."
    )

else:

    for request in pending_requests:

        with st.container(border=True):

            st.subheader(
                f"Request {request['request_id']}"
            )

            st.write(
                f"**Employee:** {request['employee_name']}"
            )

            st.write(
                f"**Department:** {request['department']}"
            )

            st.write(
                f"**Reason:** {request['reason']}"
            )

            st.write(
                f"**Specifications:** "
                f"{request['specifications']}"
            )

            st.write(
                f"**Status:** {request['status']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Approve",
                    key=f"approve_{request['request_id']}"
                ):

                    update_request_status(
                        request["request_id"],
                        "Approved"
                    )

                    st.success(
                        f"{request['request_id']} approved!"
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "❌ Reject",
                    key=f"reject_{request['request_id']}"
                ):

                    update_request_status(
                        request["request_id"],
                        "Rejected"
                    )

                    st.warning(
                        f"{request['request_id']} rejected."
                    )

                    st.rerun()
# -----------------------------
# IT Processing Dashboard
# -----------------------------

st.header("🛠️ IT Processing")

requests = get_requests()

approved_requests = [
    request
    for request in requests
    if request["status"] == "Approved"
]

if not approved_requests:

    st.info(
        "No approved requests are waiting for IT processing."
    )

else:

    for request in approved_requests:

        with st.container(border=True):

            st.subheader(
                f"Request {request['request_id']}"
            )

            st.write(
                f"**Employee:** {request['employee_name']}"
            )

            st.write(
                f"**Department:** {request['department']}"
            )

            st.write(
                f"**Specifications:** "
                f"{request['specifications']}"
            )

            st.write(
                f"**Status:** {request['status']}"
            )

            if st.button(
                "🔧 Start IT Processing",
                key=f"process_{request['request_id']}"
            ):

                update_request_status(
                    request["request_id"],
                    "IT Processing"
                )

                st.success(
                    f"{request['request_id']} "
                    "is now being processed by IT."
                )

                st.rerun()
# -----------------------------
# Completed Requests
# -----------------------------

st.header("✅ Completed Requests")

requests = get_requests()

completed_requests = [
    request
    for request in requests
    if request["status"] == "IT Processing"
]

if not completed_requests:

    st.info(
        "No requests are currently in IT processing."
    )

else:

    for request in completed_requests:

        with st.container(border=True):

            st.subheader(
                f"Request {request['request_id']}"
            )

            st.write(
                f"**Employee:** {request['employee_name']}"
            )

            st.write(
                f"**Department:** {request['department']}"
            )

            st.write(
                f"**Specifications:** "
                f"{request['specifications']}"
            )

            st.write(
                f"**Status:** {request['status']}"
            )

            if st.button(
                "✅ Mark as Completed",
                key=f"complete_{request['request_id']}"
            ):

                update_request_status(
                    request["request_id"],
                    "Completed"
                )

                st.success(
                    f"{request['request_id']} "
                    "has been completed!"
                )

                st.rerun()


# -----------------------------
# Existing RAG Chatbot
# -----------------------------

st.header("💬 Enterprise Knowledge Assistant")

if "messages" not in st.session_state:

    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if message.get("sources"):

            with st.expander(
                "📚 Sources"
            ):

                for source in message["sources"]:

                    st.write(
                        f"**{source['source']}** "
                        f"(similarity: "
                        f"{source['score']:.3f})"
                    )


user_input = st.chat_input(
    "Ask about enterprise policies..."
)


if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):

        st.markdown(user_input)


    with st.chat_message("assistant"):

        try:

            with st.spinner(
                "Searching enterprise knowledge..."
            ):

                answer, sources = generate_rag_response(
                    user_input
                )

            st.markdown(answer)

            with st.expander(
                "📚 Sources"
            ):

                for source in sources:

                    st.write(
                        f"**{source['source']}** "
                        f"(similarity: "
                        f"{source['score']:.3f})"
                    )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                }
            )

        except Exception as error:

            st.error(
                f"Something went wrong: {error}"
            )