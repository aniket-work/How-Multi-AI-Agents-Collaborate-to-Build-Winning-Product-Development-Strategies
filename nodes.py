import yaml
from state import State

class Node:
    def __init__(self, name: str):
        self.name = name

    def process(self, state: State) -> dict:
        raise NotImplementedError

    def __call__(self, state: State) -> dict:
        result = self.process(state)
        return result

class SupervisorNode(Node):
    def __init__(self):
        super().__init__("Supervisor")

    def process(self, state: State) -> dict:
        state['iteration'] = state.get('iteration', 0) + 1
        task = state['messages'][0] if state['messages'] else "No task set."
        return {"messages": [f"Iteration {state['iteration']}: {task}"]}

class AgentNode(Node):
    def __init__(self, agent_name: str, llm):
        super().__init__(agent_name)
        self.llm = llm
        with open('prompts.yaml', 'r') as f:
            self.prompts = yaml.safe_load(f)

    def process(self, state: State) -> dict:
        task = state['messages'][-1]
        prompt = self.prompts['agent_prompt'].format(agent_name=self.name, task=task)
        response = self.llm.invoke(prompt)
        return {"messages": [f"{self.name}'s response: {response}"]}

class SummarizerNode(Node):
    def __init__(self, llm):
        super().__init__("Supervisor")  # Changed from "Summarizer" to "Supervisor"
        self.llm = llm
        with open('prompts.yaml', 'r') as f:
            self.prompts = yaml.safe_load(f)

    def process(self, state: State) -> dict:
        responses = state['messages'][1:]  # Skip the initial task
        responses_text = "\n\n".join([f"Agent {i+1}:\n{response}" for i, response in enumerate(responses)])
        prompt = self.prompts['supervisor_prompt'].format(responses=responses_text)
        response = self.llm.invoke(prompt)
        return {"messages": [f"Supervisor's response: {response}"]}