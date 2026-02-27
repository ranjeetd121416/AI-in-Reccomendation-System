import numpy as np


def precision_at_k(recommended, relevant, k):
    if k == 0:
        return 0.0

    recommended_k = recommended[:k]
    relevant_set = set(relevant)

    if not recommended_k:
        return 0.0

    return len(set(recommended_k) & relevant_set) / k


def recall_at_k(recommended, relevant, k):
    if not relevant:
        return 0.0

    recommended_k = recommended[:k]
    relevant_set = set(relevant)

    return len(set(recommended_k) & relevant_set) / len(relevant_set)


def f1_at_k(recommended, relevant, k):
    precision = precision_at_k(recommended, relevant, k)
    recall = recall_at_k(recommended, relevant, k)

    if precision + recall == 0:
        return 0.0

    return 2 * (precision * recall) / (precision + recall)


def ndcg_at_k(recommended, relevant, k):

    recommended_k = recommended[:k]
    relevant_set = set(relevant)

    # DCG
    dcg = 0.0
    for i, item in enumerate(recommended_k):
        if item in relevant_set:
            dcg += 1 / np.log2(i + 2)

    # IDCG (ideal DCG)
    ideal_hits = min(len(relevant_set), k)
    idcg = sum(1 / np.log2(i + 2) for i in range(ideal_hits))

    if idcg == 0:
        return 0.0

    return dcg / idcg