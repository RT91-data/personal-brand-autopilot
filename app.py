import streamlit as st
from github_reader import get_notebooks, get_notebook_content
from post_generator import generate_linkedin_post
from notion_saver import save_post_to_notion
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Personal Brand Autopilot",
    page_icon="✍️",
    layout="wide"
)

# Header
st.title("✍️ Personal Brand Autopilot")
st.caption("Turn your learning notes into LinkedIn posts — in your voice.")

st.divider()

# Load notebooks from GitHub
@st.cache_data(ttl=300)
def load_notebooks():
    return get_notebooks()

notebooks = load_notebooks()

if not notebooks:
    st.error("Could not load notebooks from GitHub. Check your .env settings.")
    st.stop()

# Sidebar — Content Calendar
with st.sidebar:
    st.header("📅 Content Calendar")
    st.caption("Your learning notes — pick a topic to generate a post.")
    st.divider()

    for nb in notebooks:
        if st.button(nb["display_name"], use_container_width=True):
            st.session_state["selected"] = nb
            if "generated_post" in st.session_state:
                del st.session_state["generated_post"]
            if "post_scores" in st.session_state:
                del st.session_state["post_scores"]

# Main area
if "selected" not in st.session_state:
    st.info("👈 Select a topic from the content calendar to generate a LinkedIn post.")

    st.subheader("📚 Your Topics")
    cols = st.columns(3)
    for i, nb in enumerate(notebooks):
        with cols[i % 3]:
            st.markdown(f"**{nb['display_name']}**")

else:
    selected = st.session_state["selected"]

    st.subheader(f"Generating post for: **{selected['display_name']}**")
    st.divider()

    col1, col2 = st.columns([1, 1])

    # ── LEFT COLUMN — Source Material ──
    with col1:
        st.markdown("### 📓 Source Material")
        st.caption("Used as briefing only — the AI generates its own examples.")

        with st.spinner("Loading notebook content..."):
            content = get_notebook_content(selected["download_url"])

        if content:
            if content["d365_analogy"]:
                with st.expander("D365 Analogy"):
                    st.markdown(content["d365_analogy"])
            if content["linkedin_post_idea"]:
                with st.expander("Original Post Idea"):
                    st.markdown(content["linkedin_post_idea"])
            if content["how_it_works"]:
                with st.expander("How It Works"):
                    st.markdown(content["how_it_works"])
        else:
            st.error("Could not load notebook content.")

    # ── RIGHT COLUMN — Post Generator ──
    with col2:
        st.markdown("### 🚀 Generated LinkedIn Post")

        # First post toggle
        is_first_post = st.toggle("This is my first post (add intro)", value=False)

        if st.button("✨ Generate Post", type="primary", use_container_width=True):
            if content:
                max_attempts = 3
                attempt = 0
                
                while attempt < max_attempts:
                    attempt += 1
                    
                    progress_placeholder = st.empty()
                    
                    import threading
                    import time
                    
                    result = {"post": None, "scores": None, "done": False}
                    
                    def run_gen():
                        result["post"], result["scores"] = generate_linkedin_post(
                            selected["display_name"],
                            content,
                            is_first_post=is_first_post
                        )
                        result["done"] = True
                    
                    thread = threading.Thread(target=run_gen)
                    thread.start()
                    
                    messages = [
                        (0,  "🔍 Agent 0: Searching what D365 practitioners are discussing this week..."),
                        (6,  "✍️  Agent 1: Drafting raw insights and real D365 scenarios..."),
                        (14, "📐 Agent 2: Structuring for LinkedIn performance..."),
                        (20, "🎯 Agent 3: Applying your voice and senior consultant tone..."),
                        (26, "📊 Agent 4: Scoring post quality across 4 dimensions..."),
                    ]
                    
                    start = time.time()
                    msg_index = 0
                    
                    while not result["done"]:
                        elapsed = time.time() - start
                        while msg_index < len(messages) and elapsed >= messages[msg_index][0]:
                            progress_placeholder.info(messages[msg_index][1])
                            msg_index += 1
                        time.sleep(0.3)
                    
                    thread.join()
                    progress_placeholder.empty()
                    
                    post = result["post"]
                    scores = result["scores"]
                    
                    # Check if any score is below 7
                    weak_scores = {k: v for k, v in scores.items() 
                                   if k in ["hook_strength", "d365_specificity", "uniqueness", "impression"] 
                                   and isinstance(v, (int, float)) and v < 7}
                    
                    if not weak_scores:
                        # All scores 7 or above — accept
                        st.toast(f"✅ Post passed quality check on attempt {attempt}", icon="✅")
                        break
                    elif attempt < max_attempts:
                        # Weak scores found — auto retry with feedback
                        weak_names = ", ".join([k.replace("_", " ") for k in weak_scores.keys()])
                        auto_feedback = scores.get("one_line_fix", f"Improve weak areas: {weak_names}")
                        st.toast(f"⚠️ Weak scores in: {weak_names}. Auto-retrying with scorer feedback...", icon="⚠️")
                        # Pass scorer feedback into next attempt
                        post, scores = generate_linkedin_post(
                            selected["display_name"],
                            content,
                            is_first_post=is_first_post,
                            feedback=auto_feedback
                        )
                        # Check again
                        weak_scores = {k: v for k, v in scores.items()
                                      if k in ["hook_strength", "d365_specificity", "uniqueness", "impression"]
                                      and isinstance(v, (int, float)) and v < 7}
                        if not weak_scores:
                            st.toast(f"✅ Post passed quality check on attempt {attempt + 1}", icon="✅")
                            break
                    else:
                        # Max attempts reached — show best result
                        weak_names = ", ".join([k.replace("_", " ") for k in weak_scores.keys()])
                        st.warning(f"⚠️ Could not achieve all scores above 7 after {max_attempts} attempts. Showing best result. Weak areas: {weak_names}")
                
                st.session_state["generated_post"] = post
                st.session_state["post_scores"] = scores
            else:
                st.error("No content to generate from.")

        if "generated_post" in st.session_state:

            # Post display
            st.text_area(
                "Your post — review and edit before posting:",
                value=st.session_state["generated_post"],
                height=350
            )

            # Copy box
            st.code(st.session_state["generated_post"], language=None)
            st.caption("👆 Click the copy icon in the top-right corner of the box above.")

            st.divider()

            # Quality scores
            if "post_scores" in st.session_state:
                scores = st.session_state["post_scores"]
                st.markdown("**📊 Post Quality Scores:**")
                col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                with col_s1:
                    st.metric("Hook", f"{scores.get('hook_strength', 0)}/10")
                with col_s2:
                    st.metric("D365 Specificity", f"{scores.get('d365_specificity', 0)}/10")
                with col_s3:
                    st.metric("Uniqueness", f"{scores.get('uniqueness', 0)}/10")
                with col_s4:
                    st.metric("Impression", f"{scores.get('impression', 0)}/10")

                avg = scores.get('average', 0)
                if avg >= 8:
                    st.success(f"✅ Strong post — average score {avg}/10. Ready to publish.")
                elif avg >= 6:
                    st.warning(f"⚠️ Decent post — average {avg}/10. Consider regenerating.")
                else:
                    st.error(f"❌ Weak post — average {avg}/10. Regenerate before posting.")

                # Always show weakest element and fix suggestion
                if scores.get('weakest_element') and scores.get('one_line_fix'):
                    st.info(f"💡 Weakest: **{scores.get('weakest_element').replace('_', ' ').title()}** — {scores.get('one_line_fix')}")

            st.divider()

            # Feedback section
            st.markdown("**Not quite right? Give feedback:**")
            
            # Pre-fill with scorer suggestion if available
            scorer_suggestion = ""
            if "post_scores" in st.session_state:
                scorer_suggestion = st.session_state["post_scores"].get("one_line_fix", "")
            
            feedback = st.text_input(
                "Edit or replace the scorer's suggestion, or type your own:",
                value=scorer_suggestion,
                key="feedback_input"
            )

            col_regen, col_feedback = st.columns(2)

            with col_regen:
                if st.button("🔄 Regenerate", use_container_width=True):
                    if content:
                        with st.spinner("Rewriting..."):
                            post, scores = generate_linkedin_post(
                                selected["display_name"],
                                content,
                                is_first_post=is_first_post
                            )
                        st.session_state["generated_post"] = post
                        st.session_state["post_scores"] = scores
                        st.rerun()

            with col_feedback:
                if st.button("✨ Apply Feedback", use_container_width=True, type="primary"):
                    if content and feedback:
                        with st.spinner("Applying your feedback..."):
                            post, scores = generate_linkedin_post(
                                selected["display_name"],
                                content,
                                is_first_post=is_first_post,
                                feedback=feedback
                            )
                        st.session_state["generated_post"] = post
                        st.session_state["post_scores"] = scores
                        st.rerun()
                    elif not feedback:
                        st.warning("Enter feedback first.")

            st.divider()

            # Image suggestion
            st.markdown("**📸 Image suggestion for this post:**")
            image_suggestions = {
                "What Is Machine Learning": "Simple before/after diagram: 'Traditional: Rules → Output' vs 'ML: Data → Rules'. Clean, minimal, dark background.",
                "Supervised Vs Unsupervised": "Two columns visual: labelled data examples vs unlabelled clusters. Use D365 invoice examples.",
                "Parameters Vs Hyperparameters": "A dial/knob graphic labelled 'You set this' vs a brain icon labelled 'Model learns this'.",
                "Cost Function And Gradient Descent": "A simple hill/valley diagram showing gradient descent steps going downward.",
                "Overfitting And Underfitting": "Three curves: underfit (too simple), just right, overfit (too wiggly). Classic ML diagram.",
                "Precision And Recall": "A Venn diagram showing flagged vs actual fraud with the overlap highlighted.",
            }

            image_hint = image_suggestions.get(
                selected["display_name"],
                "Clean graphic: concept name as heading, one key insight as subtext, your name/handle at bottom. Dark background, white text. 1200x627px."
            )
            st.info(f"💡 {image_hint}")
            st.caption("Create this in Canva — use a 1200x627px template for LinkedIn.")

            st.divider()

            # Save to Notion
            st.markdown("**💾 Save to Notion Content Calendar:**")

            col_date, col_save = st.columns(2)

            with col_date:
                scheduled_date = st.date_input(
                    "Schedule for:",
                    value=datetime.today() + timedelta(days=1),
                    min_value=datetime.today()
                )

            with col_save:
                st.write("")
                st.write("")
                if st.button("💾 Save to Notion", use_container_width=True, type="primary"):
                    try:
                        notion_url = save_post_to_notion(
                            title=f"{selected['display_name']} — LinkedIn Post",
                            content=st.session_state["generated_post"],
                            topic=selected["display_name"],
                            image_suggestion=image_hint,
                            scheduled_date=scheduled_date
                        )
                        st.success("✅ Saved to Notion!")
                        st.markdown(f"[Open in Notion]({notion_url})")
                    except Exception as e:
                        st.error(f"Failed to save: {str(e)}")

    # Reset button
    st.divider()
    if st.button("← Back to Calendar"):
        for key in ["selected", "generated_post", "post_scores"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()