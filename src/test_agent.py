from agent import AndroidWorldAgent, OpenAIProvider
from prompts import render_prompt, DEFAULT_PROMPT_TEMPLATE
from agent import load_episode_from_json

# Load a sample episode
episode = load_episode_from_json("episodes/sample_episode.json")

# Print goal and first observation
print("Goal:", episode.goal)
print("First observation:", episode.observations[0])
print("Ground truth action:", episode.ground_truth_actions[0])

# Render prompt for first step
prompt = render_prompt(episode.goal, episode.observations[0])
print("Prompt to LLM:\n", prompt)