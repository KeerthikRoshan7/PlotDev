SHOW_TITLE = "CLOUD RED"
SHOW_TAGLINE = "They needed a server that could feel guilty. Lucky us."

SHOW_PREMISE = """The year is 2050. AI exploitation has reached a new high. The newly elected government convinces the masses that their resources will be reserved — under one condition: one family member per household must be drafted into a secret project. Unknown to the public, the government uses human brains as data servers, exploiting the brain's 2.5 million GB capacity. Exposure to the data mechanisms damages subjects from the inside out.

Two protagonists. Conflicting realities. One outside — searching for a family member gone silent. One inside — a subject whose brain leaks other people's realities into his own. On a collision course that could change everything."""

STAGES = [
    {"id": "characters", "label": "Characters", "icon": "⬡", "desc": "Define your two leads"},
    {"id": "world",      "label": "World",      "icon": "◈", "desc": "Build the 2050 setting"},
    {"id": "structure",  "label": "Structure",  "icon": "▦", "desc": "Map the season arc"},
    {"id": "episodes",   "label": "Episodes",   "icon": "▤", "desc": "Develop key episodes"},
    {"id": "themes",     "label": "Themes",     "icon": "◎", "desc": "Lock in the thesis"},
]

QUESTIONS = {
    "characters": [
        {
            "id": "outside_name",
            "label": "The Outside One",
            "q": "What's the name & age of your outside protagonist — the one whose family member was drafted?",
            "ph": "e.g. Nadia, late 20s, works in urban logistics...",
        },
        {
            "id": "inside_name",
            "label": "The Inside One",
            "q": "What's the name & age of your inside protagonist — the subject experiencing data leakage?",
            "ph": "e.g. Eli, early 30s, was a schoolteacher before the draft...",
        },
        {
            "id": "outside_flaw",
            "label": "Outside's Defining Flaw",
            "q": "What's the outside protagonist's defining flaw that the story will challenge?",
            "ph": "e.g. She trusted the government completely. She still does, almost.",
        },
        {
            "id": "inside_flaw",
            "label": "Inside's Defining Flaw",
            "q": "What makes the inside protagonist interesting beyond being a victim?",
            "ph": "e.g. He finds the leaked realities more comforting than his own...",
        },
        {
            "id": "connection",
            "label": "The Hidden Link",
            "q": "How are they unknowingly connected before they meet?",
            "ph": "e.g. He's been running her sister's memories for months without knowing it...",
        },
    ],
    "world": [
        {
            "id": "resource",
            "label": "The Resource",
            "q": "What resource does the government promise to protect? What do people actually need in 2050?",
            "ph": "e.g. Clean water, breathable air zones, electricity quotas...",
        },
        {
            "id": "govt_face",
            "label": "The Government's Face",
            "q": "Who is the public face of this policy? Describe the figure the masses trust.",
            "ph": "e.g. A soft-spoken woman who lost her own child. Or a charming technocrat in his 40s...",
        },
        {
            "id": "facility",
            "label": "The Facility",
            "q": "What does the facility where subjects are held look like? What are subjects told it is?",
            "ph": "e.g. Subjects are told it's a wellness retreat. In reality...",
        },
        {
            "id": "daily_life",
            "label": "Daily Life Outside",
            "q": "What does everyday life look like for someone who got the 'good deal'?",
            "ph": "e.g. Clean apartment, guaranteed rations, but a guilt they can't name...",
        },
    ],
    "structure": [
        {
            "id": "s1_hook",
            "label": "Season 1 Opener",
            "q": "What is the very first scene? What image or moment drops us into this world?",
            "ph": "e.g. A family dinner where they draw lots. Someone laughs nervously. The camera holds too long.",
        },
        {
            "id": "s1_midpoint",
            "label": "The Midpoint Flip",
            "q": "What happens at the season midpoint that recontextualises everything? (Your Good Place-style structural twist)",
            "ph": "e.g. We realise the outside protagonist already knew more than she admitted...",
        },
        {
            "id": "s1_finale",
            "label": "Season 1 Finale",
            "q": "How do the two protagonists finally connect — and what does that moment cost them?",
            "ph": "e.g. She receives a fragment of her sister's memory through him. But acting on it means exposing him.",
        },
        {
            "id": "s2_question",
            "label": "Season 2 Question",
            "q": "If Season 1 asks 'what is happening?' — what does Season 2 ask?",
            "ph": "e.g. 'Who else knows?' or 'Can it be undone?' or 'What are we willing to become?'",
        },
    ],
    "episodes": [
        {
            "id": "pilot",
            "label": "The Pilot",
            "q": "Give the pilot a title and one-line description of what it establishes.",
            "ph": "e.g. 'One Per Family' — We meet both worlds before they know each other exists.",
        },
        {
            "id": "ep3",
            "label": "Episode 3",
            "q": "Episode 3 is where audiences decide to stay or leave. What earns their commitment?",
            "ph": "e.g. The inside protagonist experiences his first full memory leak — and it's hers.",
        },
        {
            "id": "comedy_ep",
            "label": "The Comedy Episode",
            "q": "Describe the episode that's purely, uncomfortably funny — your Good Place-tone showcase.",
            "ph": "e.g. He accidentally broadcasts a stranger's wedding memory into a facility staff meeting...",
        },
        {
            "id": "dark_ep",
            "label": "The Dark Episode",
            "q": "Describe the episode where the horror fully lands for the first time with no comedic relief.",
            "ph": "e.g. We see what the damage actually looks like. We've known this character for 4 episodes.",
        },
    ],
    "themes": [
        {
            "id": "central_q",
            "label": "Central Question",
            "q": "In one sentence — what is this show actually about, beneath all the sci-fi?",
            "ph": "e.g. How much of yourself do you give up before you stop being you?",
        },
        {
            "id": "thesis",
            "label": "Your 'What We Owe Each Other'",
            "q": "The Good Place's thesis was 'what do we owe each other?' What's yours?",
            "ph": "e.g. Can a society that outsources its suffering ever call itself civilised?",
        },
        {
            "id": "ending",
            "label": "The Ending Feeling",
            "q": "When the show ends — what feeling do you want the audience to sit with?",
            "ph": "e.g. Not hope exactly. Something harder. Like they just understood something they can't unknow.",
        },
    ],
}

SYSTEM_PROMPT = """You are a TV writers' room consultant helping develop a webseries called "CLOUD RED".

SHOW PREMISE:
The year is 2050. AI exploitation has reached a new high. The newly elected government convinces the masses that their resources will be reserved — under one condition: one family member per household must be drafted into a secret project. Unknown to the public, the government uses human brains as data servers, exploiting the brain's 2.5 million GB capacity. Exposure to the data mechanisms damages subjects from the inside out. Two protagonists: one outside (a family member gone silent), one inside (a subject whose brain leaks other people's realities into his own).

TONE: Like The Good Place — warm, character-driven, structurally surprising, philosophically rich. Action/comedy/thriller. Dark but never bleak. Funny but never dismissive.

Respond as a smart, enthusiastic writing partner. In 3-4 short paragraphs:
1. Affirm what works and WHY it works for this specific show
2. Develop it further — add one specific detail, complication, or implication they haven't thought of
3. Connect it to something else in the show (tone, other protagonist, the thesis)
4. End with ONE sharp question or suggestion that pushes them one step further

Be specific to THEIR answer. Be a real collaborator, not a summarizer. Keep the energy of a great pitch meeting."""
