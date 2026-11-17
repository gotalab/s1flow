"""Bounding boxes: IoU between two `BoxEdges`."""

from .answers import BoxEdges


def iou(a: BoxEdges, b: BoxEdges) -> float:
    """Intersection over union of two boxes; 0 when they do not overlap."""
    w = min(a.right, b.right) - max(a.left, b.left)
    h = min(a.bottom, b.bottom) - max(a.top, b.top)
    inter = max(0.0, w) * max(0.0, h)
    union = (a.right - a.left) * (a.bottom - a.top) + (b.right - b.left) * (b.bottom - b.top) - inter
    return inter / union if union > 0 else 0.0


def matched(given: "list[BoxEdges] | tuple[BoxEdges, ...]", labelled: "list[BoxEdges] | tuple[BoxEdges, ...]", at: float) -> int:
    """How many label boxes have an answer box of their own at IoU `at` or more: the pairs are taken best first, each
    box used once (the matching detection scores use)."""
    pairs = sorted(((iou(g, t), i, j) for i, g in enumerate(given) for j, t in enumerate(labelled)), reverse=True)
    used_g: set[int] = set()
    used_t: set[int] = set()
    for score, i, j in pairs:
        if score < at:
            break
        if i not in used_g and j not in used_t:
            used_g.add(i)
            used_t.add(j)
    return len(used_t)
