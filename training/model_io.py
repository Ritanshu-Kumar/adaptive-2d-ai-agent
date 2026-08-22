import pickle


def save_q_table(q_table, path):
    with open(path, "wb") as file:
        pickle.dump(dict(q_table), file)


def load_q_table(agent, path):
    with open(path, "rb") as file:
        saved_table = pickle.load(file)

    agent.q_table.update(saved_table)