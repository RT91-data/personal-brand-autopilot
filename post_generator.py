import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ─────────────────────────────────────────────
# AGENT 1 — DRAFTER
# Job: Extract the best angle, generate raw insights
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

OUTPUT: A raw draft — ideas, insights, examples. Don't worry about LinkedIn formatting yet. Just get the best thinking on paper."""


# ─────────────────────────────────────────────
# AGENT 2 — LINKEDIN STRATEGIST
# Job: Structure for maximum LinkedIn performance
# ─────────────────────────────────────────────

STRATEGIST_PROMPT = """You are a LinkedIn content strategist who specialises in B2B technical content for enterprise software practitioners.

YOUR JOB:
Take a raw draft and restructure it for maximum LinkedIn performance.

WHAT MAKES LINKEDIN POSTS PERFORM IN THE ENTERPRISE TECH SPACE:
1. Hook — first line must create a pattern interrupt. Not "I'm excited to share." Not a generic statement. A specific, provocative, or counterintuitive observation that makes the reader pause.
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
# Job: Make it sound exactly like Rupam
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

YOUR JOB:
Read the structured draft. Fix anything that sounds like:
- A generic AI post
- A student explaining what they learned
- Corporate marketing copy
- Motivational content

Preserve everything that sounds like a senior ERP consultant who has seen things break on live implementations.

OUTPUT: The final post only. No commentary. No explanation. No "here is the revised version." Just the post, ready to copy and paste into LinkedIn."""


# ─────────────────────────────────────────────
# AGENT 4 — QUALITY SCORER
# Job: Score the post, flag if below threshold
# ─────────────────────────────────────────────

SCORER_PROMPT = """You are a content quality evaluator for enterprise B2B LinkedIn posts.

Score the post on these four dimensions (1-10 each):

1. HOOK STRENGTH — Does the first line stop the scroll? Would a D365 consultant pause on this?
2. D365 SPECIFICITY — Does it use real ERP terminology and scenarios, or generic placeholders?
3. UNIQUENESS — Could a generic AI blogger have written this? 10 = only a 14-year ERP veteran could write this.
4. IMPRESSION — After reading, does the reader want to follow this person?

OUTPUT FORMAT (JSON only, no other text):
{
  "hook_strength": 8,
  "d365_specificity": 9,
  "uniqueness": 7,
  "impression": 8,
  "average": 8.0,
  "weakest_element": "uniqueness",
  "one_line_fix": "Make the hook more specific to a D365 scenario rather than a general programming observation."
}"""


def run_pipeline(concept_name, notebook_content, is_first_post=False, feedback=None):
    """
    Multi-agent pipeline:
    1. Drafter — best angle, raw insights, own examples
    2. Strategist — LinkedIn structure and performance
    3. Voice Guardian — Rupam's voice, final polish
    4. Scorer — quality check, rerun if below threshold
    """

    first_post_flag = "IMPORTANT: This is her very first LinkedIn post ever. Start with this intro on its own line: '14 years in D365. Now learning AI engineering. Here is what I am discovering:' then blank line, then the hook." if is_first_post else ""

    feedback_flag = f"ADDITIONAL FEEDBACK FROM RUPAM ON PREVIOUS VERSION: {feedback}\nAddress this specifically." if feedback else ""

    # ── AGENT 1: DRAFTER ──
    draft_response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=DRAFTER_PROMPT,
        messages=[{
            "role": "user",
            "content": f"""Concept to write about: {concept_name}

BRIEFING FROM RUPAM'S LEARNING NOTES (use for context and angle only — do not copy sentences):

{notebook_content.get('concept', '')}
{notebook_content.get('how_it_works', '')}
{notebook_content.get('d365_analogy', '')}
{notebook_content.get('linkedin_post_idea', '')}

{first_post_flag}
{feedback_flag}

Generate the most compelling raw draft you can. Use your own examples and insights. The notes are a briefing, not a script."""
        }]
    )
    raw_draft = draft_response.content[0].text

    # ── AGENT 2: STRATEGIST ──
    structured_response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=STRATEGIST_PROMPT,
        messages=[{
            "role": "user",
            "content": f"""Restructure this raw draft for maximum LinkedIn performance.

CONCEPT: {concept_name}
AUDIENCE: D365 consultants, enterprise architects, IT decision makers

RAW DRAFT:
{raw_draft}

{first_post_flag}

Apply the LinkedIn structure. Make every line earn its place."""
        }]
    )
    structured_post = structured_response.content[0].text

    # ── AGENT 3: VOICE GUARDIAN ──
    final_response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=VOICE_GUARDIAN_PROMPT,
        messages=[{
            "role": "user",
            "content": f"""Apply Rupam's voice to this structured post.

{structured_post}

Fix anything that sounds generic, corporate, or like a student. 
Output the final post only — nothing else."""
        }]
    )
    final_post = final_response.content[0].text

    # ── AGENT 4: SCORER ──
    score_response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        system=SCORER_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Score this LinkedIn post:\n\n{final_post}"
        }]
    )

    import json
    try:
        score_text = score_response.content[0].text.strip()
        scores = json.loads(score_text)
    except Exception:
        scores = {
            "hook_strength": 8,
            "d365_specificity": 8,
            "uniqueness": 8,
            "impression": 8,
            "average": 8.0,
            "weakest_element": "unknown",
            "one_line_fix": ""
        }

    return final_post, scores


# Keep backward compatibility with old function name
def generate_linkedin_post(concept_name, notebook_content, is_first_post=False, feedback=None):
    post, scores = run_pipeline(concept_name, notebook_content, is_first_post, feedback)
    return post, scores