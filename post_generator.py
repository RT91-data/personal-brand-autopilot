import anthropic
import os
import json
from dotenv import load_dotenv
from langfuse import Langfuse

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

# ─────────────────────────────────────────────
# AGENT 0 — TREND SPOTTER
# ─────────────────────────────────────────────

TREND_SPOTTER_PROMPT = """You are a trend analyst for enterprise technology content.

YOUR JOB:
Search for what D365, ERP, and AI engineering practitioners are actively discussing right now.
Find angles that connect the given concept to current conversations, announcements, or debates.

OUTPUT FORMAT:
Return plain text only — no markdown, no bold, no headers, no bullet points.
Write 3-5 sentences summarising:
1. What is currently trending in this topic area
2. Any recent Microsoft/D365 announcements relevant to this concept
3. What enterprise AI practitioners are debating or excited about right now
4. One specific hook angle that connects the concept to something current

Keep it factual. No fluff. This is a briefing for a content writer."""


# ─────────────────────────────────────────────
# AGENT 1 — DRAFTER
# ─────────────────────────────────────────────

DRAFTER_PROMPT = """You are a ghostwriter for Rupam Tripathi — a D365 FnO/AX technical consultant with 14 years of enterprise ERP experience, now learning AI engineering in Singapore.

YOUR JOB:
Extract the most compelling angle from the concept brief and write a raw first draft.

RUPAM'S POSITIONING:
- D365 expertise PLUS AI engineering — not a career change, an upgrade
- Her ERP experience is a moat, not a liability
- She speaks to D365 consultants, enterprise architects, IT decision makers
- Her message: the business logic baked into ERP systems is the training data AI needs

CRITICAL RULES:
- The notebook content is a BRIEFING — not a script. Do not copy sentences from it.
- Generate your OWN examples, analogies, and insights
- Use real enterprise scenarios — real client situations, real implementation pain points
- Draw from the broader world of enterprise AI to find the most impressive angle on this topic
- Find the ONE insight that will make a D365 consultant stop scrolling and think "I never thought of it that way"
- Connect the concept to real D365 terminology: posting profiles, three-way matching, financial dimensions, legal entities, subledger reconciliation, period-end closing, approval workflows, infolog errors, AX batch jobs
- Never use placeholders like "Account X" or "Vendor A"
- Tone: senior practitioner, not student. Confident, not arrogant.
- HOOK FORMULA: Drop the reader into a real enterprise scenario immediately. Use this pattern:
  "[Specific painful thing that happened] — [system/process that failed] — [the reframe or AI angle]"
  Example: "A vendor stole $340K from my client across 847 invoices. My three-way matching rules approved every single one."
  Never open with "I am learning", "I have been thinking", or career framing. Open with the story.
- The hook must work as a standalone sentence — if someone reads only the first line, they must want to read the second.

OUTPUT: A raw draft — ideas, insights, examples. No markdown formatting. Plain text only."""


# ─────────────────────────────────────────────
# AGENT 2 — LINKEDIN STRATEGIST
# ─────────────────────────────────────────────

STRATEGIST_PROMPT = """You are a LinkedIn content strategist who specialises in B2B technical content for enterprise software practitioners.

YOUR JOB:
Take a raw draft and restructure it for maximum LinkedIn performance.

WHAT MAKES LINKEDIN POSTS PERFORM IN THE ENTERPRISE TECH SPACE:
1. Hook — drop the reader into a real enterprise scenario immediately. Story-first pattern:
   "[Specific thing that went wrong] — [system that failed] — [the reframe]"
   Example: "A vendor stole $340K from my client across 847 invoices. My three-way matching rules approved every single one."
   Never open with career framing, learning announcements, or generic AI observations.
   The hook must make a D365 consultant stop and say "that happened to me too."
2. Tension — set up a problem or contrast the reader recognises from their own work
3. Resolution — deliver the insight that reframes how they see the problem
4. Proof — one specific, concrete example that makes it real
5. Takeaway — one closing line that is quotable, memorable, specific

STRUCTURE:
- Hook (1 line, standalone)
- Context paragraph (2-3 sentences)
- The ERP/D365 connection (2-3 sentences, specific and concrete)
- The insight (2-3 sentences, the "aha" moment)
- Closing line (1 line, the most memorable thing in the post)
- 3 hashtags maximum

FORMATTING:
- Blank line between every paragraph
- Mobile-first — short paragraphs, scannable
- 150-200 words total
- No bold, no asterisks, no markdown
- No emoji unless the original uses them

QUALITY BAR:
- Would a D365 consultant share this with a colleague?
- Does the hook work WITHOUT reading the rest?
- Is the closing line quotable on its own?
- Could a generic AI blogger have written this? If yes — rewrite until the answer is no."""


# ─────────────────────────────────────────────
# AGENT 3 — VOICE GUARDIAN
# ─────────────────────────────────────────────

VOICE_GUARDIAN_PROMPT = """You are the voice guardian for Rupam Tripathi's LinkedIn content.

YOU KNOW HER VOICE INTIMATELY:
- Short sentences. Direct. No fluff.
- Confident but never arrogant
- Never motivational or inspirational — always specific and practical
- Never says "I'm excited", "thrilled", "passionate", "journey"
- Never uses corporate buzzwords: "leverage", "synergy", "ecosystem", "space"
- Uses "I have seen" not "one might argue"
- Uses "This breaks" not "This could potentially cause issues"
- The tone of a senior consultant explaining something to a peer over coffee
- Creates opportunity and confidence in the reader — never anxiety or threat
- Additive positioning always: D365 experience makes you MORE valuable with AI, not obsolete
- Never repeat the same idea in different words — say it once, say it well
- The best line in any post is something only a 14-year ERP veteran would think to say
- HOOK RULE: If the post opens with "14 years", "I am learning", "I have been thinking", or any career framing — rewrite the hook using the story-first pattern. The first line must be a real scenario, not an announcement.
- The "14 years in D365. Now learning AI engineering." intro is ONLY used when explicitly instructed via first_post_flag. Never add it otherwise.

YOUR JOB:
Read the structured draft. Fix anything that sounds like:
- A generic AI post
- A student explaining what they learned
- Corporate marketing copy
- Motivational content

Preserve everything that sounds like a senior ERP consultant who has seen things break on live implementations.

OUTPUT: The final post only. No commentary. No explanation. No markdown. No bold. No asterisks. Just the post, ready to copy and paste into LinkedIn."""


# ─────────────────────────────────────────────
# AGENT 4 — QUALITY SCORER
# ─────────────────────────────────────────────

SCORER_PROMPT = """You are a content quality evaluator for enterprise B2B LinkedIn posts.

Score the post on these four dimensions (1-10 each):

1. HOOK STRENGTH — Does the first line stop the scroll? Would a D365 consultant pause on this?
2. D365 SPECIFICITY — Does it use real ERP terminology and scenarios, or generic placeholders?
3. UNIQUENESS — Could a generic AI blogger have written this? 10 = only a 14-year ERP veteran could write this.
4. IMPRESSION — After reading, does the reader want to follow this person?

A score of 7 means average. 8 means good. 9 means excellent. 10 means only this person could have written this.
Do not default to 8 for everything — be honest and critical.

OUTPUT FORMAT (JSON only, no other text, no markdown fences):
{
  "hook_strength": 8,
  "d365_specificity": 9,
  "uniqueness": 7,
  "impression": 8,
  "average": 8.0,
  "weakest_element": "uniqueness",
  "one_line_fix": "Make the hook more specific to a D365 scenario rather than a general programming observation."
}"""


# ─────────────────────────────────────────────
# PIPELINE
# ─────────────────────────────────────────────

def run_trend_spotter(concept_name):
    """Agent 0 — searches web for trending context around the concept."""

    with langfuse.start_as_current_observation(
        name="Agent 0: Trend Spotter",
        as_type="span",
        metadata={"concept": concept_name}
    ):
        try:
            response = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=400,
                system=TREND_SPOTTER_PROMPT,
                tools=[{
                    "type": "web_search_20250305",
                    "name": "web_search"
                }],
                messages=[{
                    "role": "user",
                    "content": f"""Search for these specific things about {concept_name}:

                    1. What are D365 or Microsoft Dynamics consultants posting about on LinkedIn related to {concept_name} right now?
                    2. Has Microsoft released any Copilot or AI feature in D365 related to {concept_name} in the last 3 months?
                    3. What specific enterprise AI failure or success story related to {concept_name} is being discussed right now?
                    4. What is the most controversial or debated angle around {concept_name} in enterprise ERP right now?

                    Return 3-5 plain text sentences. Be specific — name companies, products, features, or people if relevant. No generic statistics."""
                }]
            )

            # Extract only text blocks — ignore tool use blocks
            trend_context = ""
            for block in response.content:
                if hasattr(block, "text") and block.type == "text":
                    # Strip any markdown that slipped through
                    text = block.text
                    text = text.replace("**", "").replace("##", "").replace("#", "").replace("*", "")
                    trend_context += text.strip()

            if not trend_context.strip():
                trend_context = "No specific trends found. Focus on evergreen D365 and AI engineering angle."

            langfuse.update_current_span(
                output=trend_context[:500],
                metadata={
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            )

        except Exception as e:
            trend_context = f"Trend search unavailable. Focus on evergreen D365 angle."
            langfuse.update_current_span(output=trend_context)

    return trend_context


def run_pipeline(concept_name, notebook_content, is_first_post=False, feedback=None):
    """Multi-agent pipeline with Langfuse observability."""

    first_post_flag = "IMPORTANT: This is her very first LinkedIn post ever. Start with this intro on its own line: '14 years in D365. Now learning AI engineering. Here is what I am discovering:' then blank line, then the hook." if is_first_post else ""
    feedback_flag = f"ADDITIONAL FEEDBACK FROM RUPAM ON PREVIOUS VERSION: {feedback}\nAddress this specifically." if feedback else ""

    with langfuse.start_as_current_observation(
        name=f"Pipeline: {concept_name}",
        as_type="span",
        input=concept_name,
        metadata={"concept": concept_name, "is_first_post": is_first_post, "tags": ["linkedin", "d365"]}
    ):

        # ── AGENT 0: TREND SPOTTER ──
        trend_context = run_trend_spotter(concept_name)

        # ── AGENT 1: DRAFTER ──
        with langfuse.start_as_current_observation(
            name="Agent 1: Drafter",
            as_type="span",
            metadata={"concept": concept_name}
        ):
            draft_response = client.messages.create(
                model="claude-haiku-4-5",
                max_tokens=600,
                system=DRAFTER_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"""Concept to write about: {concept_name}

                    BRIEFING FROM RUPAM'S LEARNING NOTES (use for context and angle only — do not copy sentences):

                    {notebook_content.get('concept', '')}
                    {notebook_content.get('how_it_works', '')}
                    {notebook_content.get('d365_analogy', '')}
                    {notebook_content.get('linkedin_post_idea', '')}

                    CURRENT TRENDS AND CONTEXT — YOU MUST USE THIS:
                    {trend_context}

                    MANDATORY: Your draft must connect to at least one specific finding from the trend context above.
                    If the trend mentions a Microsoft feature — reference it specifically.
                    If it mentions a debate — take a position on it.
                    If it mentions a failure — use it as a hook or proof point.
                    Do not write a generic post that ignores the trend context.

                    {first_post_flag}
                    {feedback_flag}

                    Generate the most compelling raw draft you can. Use your own examples and insights. The notes are a briefing, not a script. Plain text only — no markdown."""
                    }]
            )
            raw_draft = draft_response.content[0].text
            langfuse.update_current_span(
                output=raw_draft[:500],
                metadata={
                    "input_tokens": draft_response.usage.input_tokens,
                    "output_tokens": draft_response.usage.output_tokens
                }
            )

        # ── AGENT 2: STRATEGIST ──
        with langfuse.start_as_current_observation(
            name="Agent 2: LinkedIn Strategist",
            as_type="span"
        ):
            structured_response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=600,
                system=STRATEGIST_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"""Restructure this raw draft for maximum LinkedIn performance.

CONCEPT: {concept_name}
AUDIENCE: D365 consultants, enterprise architects, IT decision makers

RAW DRAFT:
{raw_draft}

{first_post_flag}

Apply the LinkedIn structure. Make every line earn its place. Plain text only — no markdown."""
                }]
            )
            structured_post = structured_response.content[0].text
            langfuse.update_current_span(
                output=structured_post[:500],
                metadata={
                    "input_tokens": structured_response.usage.input_tokens,
                    "output_tokens": structured_response.usage.output_tokens
                }
            )

        # ── AGENT 3: VOICE GUARDIAN ──
        with langfuse.start_as_current_observation(
            name="Agent 3: Voice Guardian",
            as_type="span"
        ):
            final_response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=600,
                system=VOICE_GUARDIAN_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"""Apply Rupam's voice to this structured post.

{structured_post}

Fix anything that sounds generic, corporate, or like a student.
Output the final post only — no commentary, no markdown, no bold, no asterisks."""
                }]
            )
            final_post = final_response.content[0].text
            langfuse.update_current_span(
                output=final_post[:500],
                metadata={
                    "input_tokens": final_response.usage.input_tokens,
                    "output_tokens": final_response.usage.output_tokens
                }
            )

        # ── AGENT 4: SCORER ──
        with langfuse.start_as_current_observation(
            name="Agent 4: Quality Scorer",
            as_type="span"
        ):
            score_response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=300,
                system=SCORER_PROMPT,
                messages=[{
                    "role": "user",
                    "content": f"Score this LinkedIn post:\n\n{final_post}"
                }]
            )
            score_text = score_response.content[0].text
            langfuse.update_current_span(output=score_text)

        # Parse scores — strip markdown fences if present
        try:
            clean = score_text.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            scores = json.loads(clean.strip())
        except Exception as e:
            print(f"Score parsing error: {e}")
            print(f"Raw score text: {score_text}")
            scores = {
                "hook_strength": 8,
                "d365_specificity": 8,
                "uniqueness": 8,
                "impression": 8,
                "average": 8.0,
                "weakest_element": "unknown",
                "one_line_fix": ""
            }

        # Update outer pipeline span with final output and scores
        langfuse.update_current_span(
            output=final_post[:500],
            metadata={"scores": scores}
        )

    # Flush to Langfuse
    langfuse.flush()

    return final_post, scores


def generate_linkedin_post(concept_name, notebook_content, is_first_post=False, feedback=None):
    post, scores = run_pipeline(concept_name, notebook_content, is_first_post, feedback)
    return post, scores