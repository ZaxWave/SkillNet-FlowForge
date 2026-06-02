# ALFWorld 复杂任务数据说明

## 数据来源

任务数据来自 ALFWorld（Shridhar et al., ICLR 2021），从 ALFRED 数据集（json_2.1.1）的 3,553 局训练集中筛选。ALFWorld 将 ALFRED 的具身任务转为纯文本交互，agent 通过自然语言观察和 9 种原子操作与环境交互。

- 论文：arXiv:2010.03768
- 仓库：https://github.com/alfworld/alfworld
- 数据下载：`pip install alfworld && alfworld-download`（数据存于 `$ALFWORLD_DATA/json_2.1.1/`）

## JSON 字段说明

每个任务对象包含以下字段：

| 字段 | 说明 |
|------|------|
| `task_id` | 任务标识，格式为 `{task_type}-{object}-{targetReceptacle}` |
| `task_type` | 任务类型代码（6 种，对应数据集目录名） |
| `task_desc` | 自然语言任务指令，来自数据集 `turk_annotations.anns[].task_desc` |
| `pddl_params` | 结构化任务参数：`object_target`（目标物品）、`parent_target`（目标容器）、`mrecep`（加工设备，仅 Heat/Cool/Clean/Examine 有）、`quantity`（仅 Pick Two 有） |
| `expert_plan` | 专家高层动作序列（来自 `traj_data.json` 的 `plan.high_pddl`），每步包含 `action` 和 `target` |
| `required_skills` | 从 SkillNet 的 37 个 ALFWorld skill 中，完成此任务需要的 skill 列表 |

## 六种任务类型

| 代码 | 说明 | 核心流程 |
|------|------|---------|
| `pick_and_place_simple` | 拾取与放置 | 定位 → 拾取 → 放置 |
| `look_at_obj_in_light` | 灯光下检查 | 定位光源 → toggle → 定位目标 → 移除遮挡 → 检查 |
| `pick_clean_then_place_in_recep` | 清洗与放置 | 定位 → 拾取 → 水槽清洗 → 放置 |
| `pick_heat_then_place_in_recep` | 加热与放置 | 定位 → 拾取 → 微波炉加热 → 放置 |
| `pick_cool_then_place_in_recep` | 冷却与放置 | 定位 → 拾取 → 冰箱冷却 → 放置 |
| `pick_two_obj_and_place` | 拾取两个与放置 | 搜索物1 → 放置 → 搜索物2 → 放置 |

所有任务模式为"找到物品 → [可选：单次状态改变] → 放置到目标容器"，无组合操作。

## 专家动作说明

专家轨迹使用 8 种高层 PDDL 动作（来自 ALFRED 规划器）：

| 动作 | 说明 |
|------|------|
| `GotoLocation` | 导航到指定容器 |
| `PickupObject` | 从当前容器拾取物品到手中 |
| `PutObject` | 将手中物品放入目标容器 |
| `OpenObject` | 打开封闭容器（抽屉、冰箱、微波炉等） |
| `CloseObject` | 关闭容器 |
| `ToggleObject` | 开关设备（台灯等） |
| `HeatObject` | 用设备加热手中物品 |
| `CoolObject` | 用设备冷却手中物品 |
| `CleanObject` | 用水槽清洗手中物品 |

高层动作与原子操作的映射：`GotoLocation` → `go to`，`PickupObject` → `take ... from ...`，`PutObject` → `put ... in/on ...`，等等。

## Skill 映射

每个任务的 `required_skills` 列出了 SkillNet 中 37 个 `alfworld-*` skill 的对应关系。例如 `GotoLocation(Fridge)` → `alfworld-object-locator`（推理物品在哪）+ `alfworld-location-navigator`（执行移动），`HeatObject` → `alfworld-object-heater`，`OpenObject` → `alfworld-receptacle-opener` 或 `alfworld-appliance-preparer`（取决于目标是容器还是设备）。

## 筛选原则

从 6 种类型各选 1-2 个代表性任务，优先选择涉及多步骤、多设备、跨房间或需要搜索回溯的实例。最终 8 个任务覆盖了 ALFWorld 全部操作类型和 SkillNet 中大部分的 skill。
