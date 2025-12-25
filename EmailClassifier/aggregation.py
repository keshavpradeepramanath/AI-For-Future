from collections import defaultdict

def aggregate_by_company(emails):
    """
    Output:
    {
      company: {
        label: count
      }
    }
    """
    stats = defaultdict(lambda: defaultdict(int))

    for e in emails:
        stats[e["company"]][e["label"]] += 1

    return stats
