# ALFWorld 数据集调研报告

## 一、数据集概览

ALFWorld（Aligning Text and Embodied Environments for Interactive Learning）由 Mohit Shridhar 等人于 2021 年 ICLR 发表。数据集从 ALFRED 衍生而来，将具身任务转化为纯文本交互环境，共 **3,553 局训练 + 274 局验证**。

### 获取方式

| 方式 | 说明 |
|------|------|
| 官方下载 | `pip install alfworld` → `alfworld-download` → 数据存于 `$ALFWORLD_DATA/json_2.1.1/` |
| HuggingFace | `mteb/Proced_mem_bench`（54 条样本，含完整 state-action 序列） |
| GitHub | https://github.com/alfworld/alfworld |

### 数据目录结构

每局任务是一个独立目录，命名编码了任务信息：

```
json_2.1.1/
├── train/           (3,553 局)
├── valid_seen/      (140 局，训练见过的房间布局)
└── valid_unseen/    (134 局，训练没见过的房间布局)

单局目录: {task_type}-{object}-{movableReceptacle}-{targetReceptacle}-{sceneNum}/
  └── trial_ID/
      ├── traj_data.json       ← 核心：专家轨迹 + 自然语言标注
      ├── initial_state.pddl   ← PDDL 初始状态
      └── game.tw-pddl         ← TextWorld 游戏文件
```

---

## 二、六种任务类型

数据集**仅包含 6 种任务类型**。每种任务的模式是：

```
找到物品 → [可选: 单次状态改变] → 放置到目标容器
```

**关键发现：没有任何任务需要 2 次或以上的状态改变。** 不存在"先洗再加热"或"先加热再冷却"的组合任务。

### 类型总览

| ID | 类型 | 代码标识 | 训练/局 | 验证已见/局 | 验证未见/局 |
|----|------|---------|---------|------------|------------|
| 1 | Pick & Place | `pick_and_place_simple` | 790 | 35 | 24 |
| 2 | Examine in Light | `look_at_obj_in_light` | 308 | 13 | 18 |
| 3 | Clean & Place | `pick_clean_then_place_in_recep` | 650 | 27 | 31 |
| 4 | Heat & Place | `pick_heat_then_place_in_recep` | 459 | 16 | 23 |
| 5 | Cool & Place | `pick_cool_then_place_in_recep` | 533 | 25 | 21 |
| 6 | Pick Two & Place | `pick_two_obj_and_place` | 813 | 24 | 17 |
| **合计** | | | **3,553** | **140** | **134** |

### 每种类型的操作逻辑

#### 类型 1：Pick & Place（拾取与放置）— 最简单

仅需定位、拾取、放置。无状态改变，无设备交互。

```
流程: 定位物体 → 拾取 → 移动到目标容器 → 放置
平均步数: 7-10 步
```

示例任务：
- `put a pencil in desk`
- `put some keychain on sofa`
- `put a spraybottle in cabinet`
- `put some newspaper on garbagecan`

#### 类型 2：Examine in Light（灯光下检查）— 最特殊

不改变物体状态，但需要**先找到并操作光源设备**（台灯），再在光源下检查目标物体。经常涉及遮挡关系（物体在台灯"下面"）。

```
流程: 定位台灯 → 打开台灯(toggle) → 定位目标物体 → 可能在遮挡物下 → 移除遮挡 → 检查
平均步数: 8-12 步
```

示例任务：
- `look at pillow under the desklamp` — 枕头被台灯遮挡
- `look at box under the desklamp`
- `examine the cellphone with the desklamp`
- `look at alarmclock under the desklamp`

#### 类型 3：Clean & Place（清洗与放置）

需要对物体执行清洗操作（用水槽），然后放置。

```
流程: 定位物体 → 拾取 → 移动到水槽 → 清洗 → 移动到目标容器 → 放置
平均步数: 10-15 步
```

示例任务：
- `put a clean lettuce in diningtable`
- `clean some apple and put it in microwave`
- `put a clean soapbar in cabinet`
- `put a clean fork in drawer`
- `clean some potato and put it in microwave`

#### 类型 4：Heat & Place（加热与放置）

需要用微波炉或灶台加热物体，然后放置。涉及与加热设备的交互（可能需要开门）。

```
流程: 定位物体 → 拾取 → 移动到微波炉/灶台 → 打开设备 → 加热 → 取出 → 移动到目标容器 → 放置
平均步数: 10-15 步
```

示例任务：
- `heat some egg and put it in diningtable`
- `put a hot potato in sidetable`
- `put a hot tomato in garbagecan`
- `heat some mug and put it in coffeemachine`

#### 类型 5：Cool & Place（冷却与放置）

需要用冰箱冷却物体，然后放置。

```
流程: 定位物体 → 拾取 → 移动到冰箱 → 打开冰箱 → 冷却 → 移动到目标容器 → 放置
平均步数: 10-15 步
```

示例任务：
- `cool some lettuce and put it in garbagecan`
- `put a cool cup in shelf`
- `cool some tomato and put it in microwave`
- `put a cool pan in stoveburner`

#### 类型 6：Pick Two & Place（拾取两个与放置）— 最复杂

需要找到**两个同类物体**并放到目标容器。两次搜索可能走完全不同的路径。

```
流程: 搜索物体1 → 拾取 → 放置 → 搜索物体2 → 拾取 → 放置 → 验证数量
平均步数: 14-20 步（全类型最多）
```

示例任务：
- `find two pen and put them in garbagecan`
- `find two laptop and put them in bed`
- `find two cd and put them in sidetable`
- `find two book and put them in bed`
- `find two remotecontrols and put them in sofa`

---

## 三、复杂度分析

### 3.1 按所需操作步数

| 排名 | 类型 | 平均步数 | 复杂度来源 |
|------|------|---------|-----------|
| 🥇 | Pick Two & Place | 14-20 | 双倍搜索 + 数量追踪 + 可能回溯 |
| 🥈 | Clean / Heat / Cool & Place | 10-15 | 设备交互 + 状态改变 + 开关容器 |
| 🥉 | Examine in Light | 8-12 | 设备操作 + 遮挡推理 |
| 4 | Pick & Place | 7-10 | 仅搬运，无额外环节 |

### 3.2 按需要的 Skill 数量

基于 SkillNet 的 37 个 ALFWorld skill 来评估每种类型需要调用的 skill 数量：

#### Pick Two & Place — 约 9-11 个 skill

```
alfworld-goal-interpreter      ← 解析任务：数量=2，类型=pen，目标=garbagecan
alfworld-environment-scanner   ← 构建全屋容器地图
alfworld-inventory-management  ← 初始化计数 collected=0, needed=2
alfworld-object-locator        ← 优先级排序：笔 → 搜索抽屉/笔筒/桌面
alfworld-search-pattern-executor ← 按候选列表逐容器穷举
alfworld-receptacle-opener     ← 候选容器可能关着（抽屉）
alfworld-object-retriever      ← 找到后拾取
alfworld-location-navigator    ← 去目标容器
alfworld-object-placer         ← 放置
alfworld-search-verifier       ← 第一轮没凑够 → 回溯已搜容器
alfworld-task-verifier         ← 最终验证数量
```

#### Heat / Cool / Clean & Place — 约 7-9 个 skill

```
alfworld-goal-interpreter      ← 解析：加热 egg → 放 diningtable
alfworld-environment-scanner   ← 扫描
alfworld-object-locator        ← egg 在哪？→ 常识推理：冰箱
alfworld-receptacle-opener     ← 开冰箱
alfworld-object-picker         ← 拾取 egg
alfworld-appliance-navigator   ← 去微波炉（heat）或冰箱（cool）或水槽（clean）
alfworld-appliance-preparer    ← 开设备门
alfworld-object-heater         ← 执行 heat/cool/clean（或 object-cooler / clean-object）
alfworld-object-retriever      ← 从设备中取出（clean 不需要，物品在手中）
alfworld-location-navigator    ← 去目标容器
alfworld-object-placer         ← 放置
alfworld-task-verifier         ← 验证
```

#### Examine in Light — 约 6-8 个 skill

```
alfworld-goal-interpreter      ← 解析空间关系 "under the desklamp"
alfworld-environment-scanner   ← 扫描
alfworld-tool-locator          ← 定位台灯
alfworld-device-operator       ← toggle 台灯
alfworld-object-locator        ← pillow 在哪？→ 可能在台灯下面（被遮挡）
alfworld-object-picker         ← 移除遮挡物（台灯）
alfworld-object-state-inspector ← 确认看到目标物体
alfworld-task-verifier         ← 验证
```

#### Pick & Place — 约 4-5 个 skill

```
alfworld-goal-interpreter      ← 解析
alfworld-object-locator        ← 定位
alfworld-object-picker         ← 拾取
alfworld-location-navigator    ← 去目标
alfworld-object-placer         ← 放置
alfworld-task-verifier         ← 验证
```

### 3.3 复杂度对比总表

| 类型 | 步数 | Skill 数 | 状态改变 | 设备交互 | 数量追踪 | 空间推理 | 回溯搜索 |
|------|------|---------|---------|---------|---------|---------|---------|
| Pick Two | 14-20 | 9-11 | 无 | 无 | ✅ | 无 | ✅ |
| Heat | 10-15 | 7-9 | ✅ | ✅ | 无 | 无 | 无 |
| Cool | 10-15 | 7-9 | ✅ | ✅ | 无 | 无 | 无 |
| Clean | 10-15 | 7-9 | ✅ | ✅ | 无 | 无 | 无 |
| Examine | 8-12 | 6-8 | 无 | ✅ | 无 | ✅ | 无 |
| Pick | 7-10 | 4-5 | 无 | 无 | 无 | 无 | 无 |

---

## 四、六种类型之间的具体差异

### 4.1 "局"是什么意思？为什么有三千多局？

**"局"（episode）= 一次完整的任务执行。** 每一局是一个独立的 TextWorld 游戏实例，有自己随机生成的房间布局、物品位置、容器状态。

一局包含：初始环境描述 + 自然语言任务指令 + 专家动作轨迹（约 7-20 步）。

三千多局不是三千多种**不同的任务逻辑**——核心逻辑只有 6 种。多局的原因是**排列组合**：

```
一局的目录名 = {任务类型} + {物品} + {设备} + {目标容器} + {场景编号}

例如: pick_heat_then_place_in_recep-Potato-Microwave-SinkBasin-14
       ↑ 类型:加热       ↑ 物品:土豆  ↑ 设备:微波炉  ↑ 终点:水槽  ↑ 14号场景
```

变化维度：
- **物品**（~30+ 种）：pen, pencil, book, apple, potato, egg, mug, cup, bowl, plate, pan, lettuce, tomato, soapbar, soapbottle, spraybottle, ladle, fork, cellphone, laptop, cd, remotecontrol, alarmclock, keychain, newspaper, pillow, box, handtowel, toiletpaper...
- **目标容器**（~15+ 种）：diningtable, sidetable, coffeetable, desk, shelf, drawer, cabinet, fridge, garbagecan, bed, sofa, dresser, countertop, sinkbasin, toilet, stoveburner, microwave...
- **场景编号**（1-30 号 FloorPlan，来自 ALFRED）：每个编号代表不同的房间布局
- **专家轨迹随机种子**：同一个任务配置下，专家示范的路径也有随机扰动

所以 **3,553 局 ≈ 6 种逻辑 × 几十种物品 × 十几种容器 × 30 个场景 × 多次随机采样**。同类型下的不同局，对 skill 编排来说是完全等价的——skill 链不变，只是 `object = "pen"` 换成 `object = "book"`。

**训练/验证的分布逻辑：**
- `valid_seen`（140局）：场景编号在训练中出现过，但物品-容器组合是新的 → 测**泛化到新任务**
- `valid_unseen`（134局）：场景编号在训练中从未出现 → 测**泛化到新环境**

### 4.2 六种类型的核心差异

每种类型在操作链的**环节数量**和**环节性质**上有本质区别：

```
                   定位    拾取   设备交互   状态改变   二次搜索   放置    验证
Pick & Place        ✅     ✅       —         —         —       ✅     ✅
Examine in Light   ✅✅     ✅      ✅         —         —       —      ✅
                        (找台灯+找目标)   (toggle)
Clean & Place       ✅     ✅      ✅         ✅         —       ✅     ✅
                                  (水槽)    (clean)
Heat & Place        ✅     ✅      ✅         ✅         —       ✅     ✅
                                 (微波炉)    (heat)
Cool & Place        ✅     ✅      ✅         ✅         —       ✅     ✅
                                  (冰箱)    (cool)
Pick Two & Place   ✅✅    ✅✅     —         —         ✅       ✅     ✅
                   (找物1+找物2) (取1+取2)           (回溯搜物2)
```

具体差异拆解：

**① Pick & Place vs 其他：多了一个"加工环节"**

Heat/Cool/Clean 三种比 Pick 多了整整一个阶段——设备交互 + 状态改变。这个阶段的 skill 链是：`appliance-navigator`（去设备）→ `appliance-preparer`（开门）→ `object-heater/cooler/clean-object`（执行）→ `object-retriever`（取出）。多出 4 个 skill，多出 3-5 步。

**② Heat/Cool/Clean 三者之间：设备不同，前置条件不同**

三者操作结构完全一样，但实际执行有细微差别：

| | Heat | Cool | Clean |
|------|------|------|------|
| 设备 | microwave / stoveburner | fridge | sinkbasin |
| 设备需要开门？ | microwave 要开，stoveburner 不需要 | 需要开冰箱门 | 不需要开水槽 |
| 加工后物品在哪？ | 在设备里，需取出 | 物品留在冰箱内或手中 | 物品在手中 |
| 典型终点 | diningtable, sidetable | cabinet, shelf, microwave | cabinet, shelf, diningtable |
| 特殊场景 | 物品原本在冰箱 → 加热 → 可能放回冰箱 | 物品可能在冰箱里已冷却 → 跳过热操作 | 物品可能已经干净 → 跳过热操作 |

**③ Examine vs Heat/Cool/Clean：设备交互方式不同**

Examine 不需要改变物品状态，但需要：
- 找两个东西（台灯 + 目标），而不是找一个 → 多一次定位
- `toggle`（开关灯）vs `heat/cool/clean`（加工物品）→ 操作目标不同
- 经常涉及**遮挡**：物品在台灯"下面"（under），不拿走台灯就看不到

**④ Pick Two vs 其他所有：唯一需要循环的类型**

其他 5 种都是**单次线性流程**：找→（加工）→放→结束。Pick Two 是**循环流程**：找→放→找→放→验证。这带来了两个独有需求：
- `inventory-management`（追踪已收集数量、控制循环终止）
- `search-verifier`（第一轮没凑够时回溯已搜容器）

### 4.3 Examine in Light 为什么局数最少（308局）？

因为能作为光源的设备只有 **desklamp** 一种，覆盖场景有限。不像 Heat（微波炉、灶台都在大多数厨房场景中）或 Pick（任何物品+任何容器都能配对）。物品×容器的组合空间小，自然局数少。

### 4.4 Pick Two 为什么局数最多（813局）？

因为需要 2 个同类物品同时存在于环境中。生成约束更松——只要有 2 个 pen（可能在 2 个不同容器里）就能构成一局，物品×容器×场景的组合空间比单物品任务更大。

---

## 五、推荐研究的任务（补齐 6 种全覆盖）

| # | 任务 | 类型 | 核心竞争力 | 需要 skill 数 |
|---|------|------|-----------|--------------|
| 1 | `find two pen and put them in garbagecan` | Pick Two | 循环搜搜 + 数量追踪 + 失败回溯 | ~10 个 |
| 2 | `heat some egg and put it in diningtable` | Heat & Place | 封闭容器拆包 + 设备开门 + 三段式流水线 | ~8 个 |
| 3 | `cool some lettuce and put it in garbagecan` | Cool & Place | 冰箱交互 + 冷却状态改变 | ~8 个 |
| 4 | `clean some apple and put it in microwave` | Clean & Place | 水槽清洗 + 状态改变 + 设备交互 | ~8 个 |
| 5 | `look at pillow under the desklamp` | Examine in Light | 空间关系推理 + 遮挡消除 + 设备 toggle | ~7 个 |
| 6 | `put a pencil in desk` | Pick & Place | 纯搬运（基线对比） | ~5 个 |

其中 Heat/Cool/Clean 三种虽然 skill 链相同，但选三者的原因是**设备交互的细节不同**（微波炉要开门取物、冰箱要开关门、水槽不需要开门），对 skill 编排中的 `appliance-preparer` 和 `object-retriever` 的使用有不同要求。

---

## 六、数据集局限

1. **无组合操作**：标准 ALFWorld 每个任务只含至多一次状态改变（clean / heat / cool 任选一）。不存在 "先洗再加热" 或 "先加热再冷却" 的组合任务。ALFRED 原始数据集中存在切片+加热等组合（如 `SliceObject` + `HeatObject`），但 ALFWorld 为了简化将其排除。

2. **物品一次只能拿一个**：agent 无法同时搬运多个物品，每次只能手持一件。Pick Two 任务必须分两次搬运。

3. **环境动作有限**：仅支持 9 种原子操作（`go to`、`take`、`put`、`open`、`close`、`toggle`、`clean`、`heat`、`cool`），无法执行更细粒度的操作（如切片、倒水、搅拌）。

4. **任务模板化**：同一类型下的不同任务只是替换了物品名和容器名，操作结构完全一样。3,553 局训练数据本质上是几十个模板 × 不同实例的排列组合。

---

## 七、数据来源

- ALFWorld 论文: arXiv:2010.03768 (ICLR 2021)
- GitHub 仓库: https://github.com/alfworld/alfworld
- HuggingFace 样本: https://huggingface.co/datasets/mteb/Proced_mem_bench
- ReAct base_config: https://raw.githubusercontent.com/ysymyth/ReAct/refs/heads/master/base_config.yaml
- SkillNet ALFWorld Skills: `E:/Desktop/SkillNet/Skills/skills/skill-collections/alfworld/`
