SHOW_TITLE = "CLOUD RED"
SHOW_TAGLINE = "They needed a server that could feel guilty. Lucky us."

PLOT_PREMISE = """The year is 2050. AI exploitation has reached a new high. The newly elected government convinces the masses that their resources will be reserved — under one condition: one family member per household must be drafted into a secret government project. Unknown to the public, the project uses human brains as data servers, exploiting the brain's 2.5 million GB capacity. Exposure to the data mechanisms damages subjects from the inside out.

Two protagonists. Conflicting realities. One outside, one inside — on a collision course that could change everything."""

STAGES = [
  {"id": "characters", "label": "Characters", "icon": "⬡", "description": "Define your two leads"},
  {"id": "world", "label": "World", "icon": "◈", "description": "Build the 2050 setting"},
  {"id": "structure", "label": "Structure", "icon": "▦", "description": "Map the season arc"},
  {"id": "episodes", "label": "Episodes", "icon": "▤", "description": "Develop key episodes"},
  {"id": "themes", "label": "Themes", "icon": "◎", "description": "Lock in the thesis"},
]

QUESTIONS = {
  "characters": [
    {"id": "outside_name", "label": "The Outside One", "question": "What's the name & gender of your outside protagonist — the one whose family member was drafted?", "placeholder": "e.g. Nadia, late 20s, works in urban logistics..."},
    {"id": "inside_name", "label": "The Inside One", "question": "What's the name & gender of your inside protagonist — the subject experiencing data leakage?", "placeholder": "e.g. Eli, early 30s, was a schoolteacher before the draft..."},
    {"id": "outside_trait", "label": "Outside's defining flaw", "question": "What's the outside protagonist's defining flaw or blind spot that the story will challenge?", "placeholder": "e.g. She trusted the government completely. She still does, almost."},
    {"id": "inside_trait", "label": "Inside's defining flaw", "question": "What's the inside protagonist's defining flaw that makes him interesting beyond just being a victim?", "placeholder": "e.g. He finds the leaked realities more comforting than his own..."},
    {"id": "connection", "label": "The Link", "question": "How are they unknowingly connected before they meet? (Beyond the obvious — the drafted family member)", "placeholder": "e.g. He's been running her sister's memories for months without knowing it..."},
  ],
  "world": [
    {"id": "resource", "label": "The Resource", "question": "What resource is the government promising to protect? What do people actually need in 2050?", "placeholder": "e.g. Clean water, breathable air zones, electricity quotas..."},
    {"id": "govt_face", "label": "The Government's Face", "question": "Who is the public face of this policy? Describe the politician or figure the masses trust.", "placeholder": "e.g. A soft-spoken woman who lost her own child. Or a charming technocrat in his 40s..."},
    {"id": "facility", "label": "The Facility", "question": "What does the facility where subjects are held actually look like? What are they told it is?", "placeholder": "e.g. Subjects are told it's a wellness retreat. In reality..."},
    {"id": "outside_world", "label": "Daily Life Outside", "question": "What does everyday life look like for someone on the outside who got the 'good deal'?", "placeholder": "e.g. Clean apartment, guaranteed rations, but a weird guilt they can't name..."},
  ],
  "structure": [
    {"id": "s1_hook", "label": "Season 1 Hook", "question": "What is the very first scene of the show? What image or moment drops us into this world?", "placeholder": "e.g. A family dinner where they draw lots. Someone laughs nervously. The camera holds too long."},
    {"id": "s1_midpoint", "label": "The Midpoint Flip", "question": "What happens at the season midpoint that recontextualizes everything we've seen? (Your Good Place-style structural twist)", "placeholder": "e.g. We realize the outside protagonist already knew more than she admitted..."},
    {"id": "s1_finale", "label": "Season 1 Finale", "question": "How do the two protagonists finally connect, and what does that moment cost them?", "placeholder": "e.g. She receives a fragment of her sister's memory through him. But acting on it means exposing him."},
    {"id": "s2_question", "label": "Season 2 Question", "question": "If Season 1 asks 'what is happening?' — what does Season 2 ask?", "placeholder": "e.g. 'Who else knows?' or 'Can it be undone?' or 'What are we willing to become?'"},
  ],
  "episodes": [
    {"id": "pilot_title", "label": "Pilot", "question": "Give the pilot episode a title and a one-line description of what it establishes.", "placeholder": "e.g. 'One Per Family' — We meet both worlds before they know each other exists."},
    {"id": "ep3_title", "label": "Episode 3", "question": "Episode 3 is where audiences decide to stay or leave. What happens that earns their commitment?", "placeholder": "e.g. The inside protagonist experiences his first full memory leak — and it's hers."},
    {"id": "comedy_ep", "label": "The Comedy Episode", "question": "Describe the episode that's purely, uncomfortably funny — your Good Place-tone showcase.", "placeholder": "e.g. He accidentally broadcasts a stranger's memory of a wedding into a facility staff meeting..."},
    {"id": "dark_ep", "label": "The Dark Episode", "question": "Describe the episode where the horror fully lands for the first time with no comedic relief.", "placeholder": "e.g. We see what the damage actually looks like. We've known a character for 4 episodes by now."},
  ],
  "themes": [
    {"id": "central_question", "label": "The Central Question", "question": "In one sentence — what is this show actually about, beneath all the sci-fi?", "placeholder": "e.g. How much of yourself do you give up before you stop being you?"},
    {"id": "good_place_equivalent", "label": "Your 'What We Owe Each Other'", "question": "The Good Place's thesis was 'what do we owe each other?' What's yours?", "placeholder": "e.g. Can a society that outsources its suffering ever call itself civilized?"},
    {"id": "ending_feeling", "label": "The Ending Feeling", "question": "When the show ends — however many seasons in — what feeling do you want the audience to sit with?", "placeholder": "e.g. Not hope exactly. Something harder. Like they just understood something they can't unknow."},
  ],
}

LOADING_LINES = [
  "Running your data through the neural grid...",
  "Accessing memory fragment...",
  "Cross-referencing leaked realities...",
  "Syncing parallel consciousness...",
  "Decrypting story architecture...",
]
