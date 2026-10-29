"""Bounding boxes: IoU between two `BoxEdges`."""

from __future__ import annotations

from .answers import BoxEdges


def iou(a: BoxEdges, b: BoxEdges) -> float:
    """Intersection over union of two boxes; 0 when they do not overlap."""
    w = min(a.right, b.right) - max(a.left, b.left)
    h = min(a.bottom, b.bottom) - max(a.top, b.top)
    inter = max(0.0, w) * max(0.0, h)
    union = (a.right - a.left) * (a.bottom - a.top) + (b.right - b.left) * (b.bottom - b.top) - inter
    return inter / union if union > 0 else 0.0
