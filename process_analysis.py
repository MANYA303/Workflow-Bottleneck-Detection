def detect_bottleneck(df):
    stage_stats = (
        df.groupby("stage")["duration_minutes"]
        .mean()
        .reset_index()
    )
    bottleneck_stage = stage_stats.loc[
        stage_stats["duration_minutes"].idxmax()
    ]
    return stage_stats, bottleneck_stage
