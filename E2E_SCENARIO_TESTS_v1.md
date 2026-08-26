# End-to-end scenario tests
## Scenario A — official new report
discover -> candidate -> fetch -> verify -> assign Evidence ID -> snapshot ADDED -> recompute signal -> brief update

## Scenario B — updated official page
fingerprint differs -> compare fields -> verify changed claim -> MODIFIED revision -> preserve old value -> signal refresh if material

## Scenario C — link disappears
link health fails -> flag source URL -> retain verified Evidence -> queue manual source check -> no factual deletion

## Scenario D — contradictory official evidence
verify both records -> retain both -> flag signal for review -> do not force consensus

## Scenario E — no material change
discovery completes -> no verified delta -> preserve current signal/brief -> report NO_CHANGE
