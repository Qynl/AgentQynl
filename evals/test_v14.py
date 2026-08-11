from minecraft.v14_memory import SkillMemory, SkillEpisode
from minecraft.v14_tasks import TaskPlan, Subtask


def test_skill_memory_retrieves_related_success():
    memory = SkillMemory()
    memory.add(SkillEpisode("get wood", "forest near tree", "key", "got logs", 1.0, "approach tree then interact"))
    results = memory.retrieve("collect wood", "forest with tree")
    assert results
    assert results[0].reward > 0


def test_task_plan_advances():
    plan = TaskPlan("build shelter", [Subtask("1", "collect logs", "logs visible in inventory")])
    assert not plan.complete
    assert plan.active.description == "collect logs"
    plan.advance()
    assert plan.complete
