from agent.memory_manager import add_solved_problem,get_solved_problems

add_solved_problem("CPU_HIGH", ["Restart service", "Check logs"])
print(get_solved_problems("CPU_HIGH"))