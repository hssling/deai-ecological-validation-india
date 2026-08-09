from __future__ import annotations
import argparse
from src.utils.io import load_config
from src.search.run_search import run as search
from src.dedup.deduplicate import run as dedup
from src.screening.screen_records import run as screen
from src.retrieval.assess_full_text import run as retrieve
from src.extraction.extract_metadata import run as extract
from src.grading.score_evidence import run as grade
from src.mechanisms.map_mechanisms import run as mechanisms
from src.nlp.topic_hype import run as nlp
from src.meta_analysis.synthesize import run as synth
from src.viz.make_figures import run as figures
from src.write_manuscript import run as manuscript

def run(cfg):
    search(cfg); dedup(cfg); screen(cfg); retrieve(cfg); extract(cfg); grade(cfg); mechanisms(cfg); nlp(cfg); synth(cfg); figures(cfg); manuscript(cfg)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config/review_config.yaml")
    run(load_config(ap.parse_args().config))
