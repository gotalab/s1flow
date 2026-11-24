# box: where one thing is in a picture

The label is a box (`{"top": .., "bottom": .., "left": .., "right": ..}`, each 0..1), or `False` when the target is
not in the picture. An answer is right when its IoU (intersection over union) with the label box is 0.5 or more
(`kind_params=KindParams(iou=0.75)` raises the bar), or when it gives no box where the label is `False`. A model that
always gives a box is wrong on those cases. The hand-off line reads the box's confidence: the model's own (jev), the
agreement of an LLM's repeated boxes, or for an answer of no box, how sure the model is that nothing is there. A model
that returns none has confidence 1 on every answer (※ in the question report, `collect.md`). How an objective acts,
and whose numbers these are: `collect.md`, "Agree on the decision".

## Purposes and their metric

| The person wants... | Standard metric | In `task.py` | Sets |
|---|---|---|---|
| every instance, not one (all the cars) | box F1 | the `boxes` type, which has no playbook yet | — |
| the right thing found, at enough overlap | accuracy at an IoU bar (Acc@0.5) | `Accuracy()` (the default), the bar in `KindParams(iou=)` | nothing |
| tight boxes (a crop, a measurement) | mean IoU | in the question report; not an objective yet: `Accuracy()` at a higher bar | nothing |
| a confidence that ranks hits above misses | AUROC of the confidence | `AUROC()` | nothing |
| act on sure answers only, a person takes the rest | coverage at a target accuracy | `Coverage(target_accuracy=X)` | min probability |
| the same, with a review cost against the overlap lost | mean loss with abstention | an `@per_case` function (`score.md` shows the form) | min probability |

IoU drops for a box that is too large as well as for one that cuts the thing off. When a margin is fine (a crop for
OCR), what counts is that the box holds the whole thing. Containment, mean IoU as the objective, and accuracy averaged
over IoU bars from 0.5 to 0.95 (as COCO does) are not built in: an `@per_case` or `@on_set` function in `task.py`
(`collect.md`, "Write task.py"). `Loss` does not take a box.

## Ask the person

- Can a picture hold more than one of the thing, and are all of them needed? Then it is the `boxes` type.
- What is the box for: pointing at the thing, counting it, cropping it, measuring it? Pointing needs less overlap than
  a measurement; a crop may need the whole thing inside more than a tight fit.
- How much overlap is enough? 0.5 is the common bar, not a recommendation; the number comes from the person.
- Can the target be missing from the picture? Then label those cases `False`, and say that a model that always gives a
  box is wrong on them.
- Will a person look at the answers the model is unsure of? If so, what accuracy must the automatic ones keep?

## The hand-off line

- `Coverage(target_accuracy=X)` answers the largest share it can while the sure answers are hits X of the time.
- `Accuracy()` and `AUROC()` set nothing: a policy adopted on them acts on every box.
- The line reads the box's confidence. Only a candidate with no ※ in the question report has one; its AUROC says how
  well it ranks hits above misses (0.5 is no better than chance).
