def hesitation_index(pause_analysis,Filler_stats,normal_pitch):
    pause_factor=pause_analysis["pause_count"]
    filler_factor=Filler_stats["total fillers used"]
    pitch_factor=normal_pitch

    hesitation=(0.4*pause_factor
                +0.4*filler_factor
                +0.2*pitch_factor)
    hesitation=max(0.0,min(1.0,hesitation))
    return round(float(hesitation),3)


def confidence_score(hesitation,stable,normal_pitch):
    confidence = (
    0.5 * stable +
    0.3 * (1 - hesitation) +
    0.2 * (1 - normal_pitch)
)
    confidence=max(0.0,min(1.0,confidence))
    return round(float(confidence),3)