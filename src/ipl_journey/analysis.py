def summarize(values):
    """Very small summary function that will be expanded across commits."""
    if not values:
        return {"count":0, "mean":None}
    return {"count": len(values), "mean": sum(values)/len(values)}
