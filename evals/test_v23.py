from minecraft.v23_skill_learner import SkillLearner
from minecraft.v23_episode import EpisodeRecorder
from minecraft.v23_curriculum import CurriculumManager, CurriculumTask
from minecraft.v23_capability import CapabilityEstimator


def test_unverified_data_is_not_learned():
    learner = SkillLearner()
    learner.record("forest", "move", 1, False)
    assert learner.rank("forest", ["move"])[0][1] == 0


def test_verified_skill_gets_ranked():
    learner = SkillLearner()
    learner.record("forest", "move", 1, True)
    learner.record("forest", "stop", -1, True)
    assert learner.rank("forest", ["move", "stop"])[0][0] == "move"


def test_episode_summary_only_counts_verified_reward():
    recorder = EpisodeRecorder()
    recorder.add("a", "x", 1, True, "success")
    recorder.add("b", "y", -1, False, "unknown")
    assert recorder.summary()["verified_steps"] == 1
    assert recorder.summary()["reward"] == 1


def test_curriculum_stays_within_capability():
    manager = CurriculumManager([CurriculumTask("easy", "walk", .1), CurriculumTask("hard", "nether", .9)])
    assert manager.next_task(.2).id == "easy"


def test_capability_changes_only_from_verified_outcomes():
    estimator = CapabilityEstimator(.5)
    assert estimator.update(1, False) == .5
    assert estimator.update(1, True) > .5
