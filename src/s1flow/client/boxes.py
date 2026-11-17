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
    """How many label boxes have an answer box of their own at IoU `at` or more, each box used once: the most
    there can be (a maximum matching), so the order the boxes come in never changes the count."""
    near = [[i for i, g in enumerate(given) if iou(g, t) >= at] for t in labelled]
    owner: dict[int, int] = {}  # answer box -> the label box it is matched to

    def claim(j: int, tried: set[int]) -> bool:  # an augmenting path from label box j
        for i in near[j]:
            if i not in tried:
                tried.add(i)
                if i not in owner or claim(owner[i], tried):
                    owner[i] = j
                    return True
        return False

    return sum(claim(j, set()) for j in range(len(labelled)))
