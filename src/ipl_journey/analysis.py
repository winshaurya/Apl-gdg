def summarize(values):
    """Very small summary function that will be expanded across commits."""
    if not values:
        return {"count":0, "mean":None}
    return {"count": len(values), "mean": sum(values)/len(values)}
\n# tiny tweak 2 - Tiny Triumph
\ndef median(values): return sorted(values)[len(values)//2]
\n# fixed edgecases 8 - Magic Smoke
\n# oops fix 11 - Oops Again
\n# bug buffet cleanup 13 - Bug Buffet
\n# polish glitter 15 - Polish Glitter
\n# refactor rave 16 - Refactor Rave
