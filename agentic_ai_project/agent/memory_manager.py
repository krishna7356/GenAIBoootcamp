import os
import json

SOLVED_PROBLEMS_FILE = "C:\\Users\\sreer\\OneDrive\\Desktop\\Interview Prep\\GenAIBoootcamp\\agentic_ai_project\\memory\\solved_memory.json"
REJECTED_PROBLEMS_FILES ="C:\\Users\\sreer\\OneDrive\\Desktop\\Interview Prep\\GenAIBoootcamp\\agentic_ai_project\\memory\\rejected_memory.json"

def load_memory(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        content = f.read().strip()
        if not content:
            return []
        return json.loads(content)
    

def save_memory(file_path,memory):
    with open(file_path,"w") as f:
        json.dump(memory, f, indent=4)
        

def add_solved_problem(alert_type,step):
    solved_memory = load_memory(SOLVED_PROBLEMS_FILE)
    solved_memory.append({"alert_type": alert_type, "step": step})
    save_memory(SOLVED_PROBLEMS_FILE,solved_memory)

def add_rejected_problem(alert_type,step,reason):
    rejected_memory =load_memory(REJECTED_PROBLEMS_FILES)
    rejected_memory.append({"alert_type": alert_type, "step": step, "reason": reason})
    save_memory(REJECTED_PROBLEMS_FILES,rejected_memory)

def get_solved_problems(alert_type=None):
    solved_memory = load_memory(SOLVED_PROBLEMS_FILE)
    for alerts in solved_memory:
        if alerts["alert_type"] == alert_type:
            return alerts["step"]
        return None

def get_rejected_problems(alert_type=None):
    rejected_memory = load_memory(REJECTED_PROBLEMS_FILES)
    for alert in rejected_memory:
        if alert["alert_type"] == alert_type:
            return {"step":alert["step"], "reason": alert["reason"]}
        return None
