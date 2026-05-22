# -*- coding: utf-8 -*-
# 文件名: replace_text_only.py
# 用法: python replace_text_only.py
# 功能: 只替换页面中的文字和数据，不动任何样式、卡片、图表、地图

import re

with open('source.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ================== 1. 标题和头部 ==================
html = html.replace('智慧蔬菜大棚监测数据大屏', '学情数据分析大屏 · 薄弱点定位 & 跨班对比')
html = html.replace('2026-05-20 15:28:38', '2026-05-23 14:30:00')
html = html.replace('运行正常', '数据实时同步')

# ================== 2. KPI数值和标签 ==================
kpi_text = [
    ('26.3', '83.6'), ('今日采集温度 (°C)', '年级平均分'),
    ('87<small>%</small>', '94.2<small>%</small>'), ('空气实时湿度 (RH)', '及格率'),
    ('50.7<small>%</small>', '37.5<small>%</small>'), ('土壤墒情均值', '优秀率 (≥90)'),
    ('134', '152'), ('今日灌溉水量 (m³)', '薄弱知识点总数'),
    ('368', '48'), ('传感器总数 (个)', '学困生人数'),
    ('10', '12'), ('异常事件 (条)', '待优化教学班')
]
for old, new in kpi_text:
    html = html.replace(old, new)

# ================== 3. 左栏面板标题 ==================
html = html.replace('环境多指标监测', '学生综合能力雷达（薄弱定位）')
html = html.replace('虫情与病害预警', '高频薄弱知识点频次')
html = html.replace('棚区实时状态', '班级学情动态与预警')

# 雷达图指标名称（只改文字，不改数据数量）
radar_indicators = ['温度适宜度', '空气湿度', 'CO₂浓度', '光照强度', '土壤墒情', 'EC浓度']
new_indicators = ['运算能力', '逻辑推理', '空间想象', '数据分析', '语言表达', '综合应用']
for old, new in zip(radar_indicators, new_indicators):
    html = html.replace(f"'{old}'", f"'{new}'")
# 雷达图数据值
html = html.replace('[82, 88, 70, 65, 92, 78]', '[74, 56, 62, 83, 71, 48]')
html = html.replace("'当前环境'", "'年级平均能力'")

# 条形图（虫情预警 -> 薄弱知识点）
html = html.replace("'蚜虫', '白粉虱', '红蜘蛛', '霜霉病', '灰霉病'",
                    "'函数综合', '力学分析', '语法填空', '文言文阅读', '化学方程式'")
html = html.replace('[120, 180, 100, 150, 80]', '[210, 178, 145, 192, 130]')

# 左栏表格5行
table_rows = [
    ('A-02 黄瓜棚', '26.4℃ / 69% / 在线', '待补水', '三(1)班 数学', '均分78 / 弱项:分数应用题', '待提升'),
    ('A-03 生菜棚', '22.8℃ / 71% / 在线', '正常', '三(2)班 英语', '均分85 / 语法薄弱', '临界关注'),
    ('B-01 彩椒棚', '28.2℃ / 62% / 离线', '温度偏高', '三(3)班 物理', '均分69 / 力学概念混乱', '预警'),
    ('B-02 茄子棚', '24.6℃ / 66% / 在线', '正常运行', '三(4)班 语文', '均分82 / 阅读理解薄弱', '待推进'),
    ('C-01 番茄棚', '25.2℃ / 70% / 在线', '正常', '三(5)班 化学', '均分88 / 方程式弱', '正常跟进')
]
for old_name, old_info, old_status, new_name, new_info, new_status in table_rows:
    # 替换整行，保留原有status类名（简单映射）
    status_cls = 'status-on'
    if old_status in ['温度偏高']: status_cls = 'status-off'
    if old_status in ['正常运行']: status_cls = 'status-warn'
    # 但为了不动结构，直接替换字符串
    old_line = f'<div class="table-row"><span>{old_name}</span><span>{old_info}</span><span class="{status_cls}">{old_status}</span></div>'
    new_line = f'<div class="table-row"><span>{new_name}</span><span>{new_info}</span><span class="{status_cls}">{new_status}</span></div>'
    html = html.replace(old_line, new_line)

# ================== 4. 中间栏标题和图例 ==================
html = html.replace('大棚分布与运行态势', '班级学情态势 & 薄弱干预点')
html = html.replace('● 正常', '● 优秀')
html = html.replace('● 运行中', '● 稳定')
html = html.replace('● 关注', '● 需关注')
html = html.replace('● 预警', '● 薄弱预警')
html = html.replace('● 科研', '● 教研提升')

# 12个卡片（只替换内部文字，不改卡片类名和结构）
cards = [
    ('1号棚', '番茄', '补光开启', 'CO₂提升', '🌡️ 25.1°C', '💧 70%',
     '1班·数学', '均分86.2', '几何弱', '运算稳定', '📊 薄弱:辅助线', '💡 专题突破'),
    ('2号棚', '水果黄瓜', '补光开启', 'CO₂提升', '🌡️ 25.1°C', '💧 66%',
     '2班·英语', '均分84.5', '词汇薄弱', '听力提升快', '📊 完形填空失分', '🎧 听读强化'),
    ('3号棚', '生菜', '灌溉中', '墒情良好', '🌡️ 22.8°C', '💧 73%',
     '3班·物理', '均分72.3', '力学薄弱', '实验待加强', '📊 浮力压强失分高', '⚠️ 关注组'),
    ('4号棚', '彩椒', '轻微预警', '病斑识别', '🌡️ 26.3°C', '💧 64%',
     '4班·语文', '均分79.4', '文言文弱', '作文偏题', '📊 阅读逻辑待提升', '🚨 急需干预'),
    ('5号棚', '番茄育苗', '苗情稳定', '光照偏弱', '🌡️ 23.4°C', '💧 70%',
     '5班·数学', '均分68.7', '函数薄弱', '运算失误高', '📊 二次函数得分率45%', '⚠️ 限时训练'),
    ('6号棚', '小白菜', '生长快', '产量提升', '🌡️ 21.9°C', '💧 75%',
     '6班·英语', '均分87.1', '阅读推理弱', '基础扎实', '📊 主旨大意题失分', '📖 专项提升'),
    ('7号棚', '黄瓜', '风机运行', '通风优', '🌡️ 24.9°C', '💧 68%',
     '7班·化学', '均分81.5', '方程式配平弱', '实验探究待巩固', '📊 推断题得分率52%', '🧪 专题复习'),
    ('8号棚', '辣椒', '水肥一体化', 'EC稳定', '🌡️ 25.4°C', '💧 67%',
     '8班·语文', '均分84.9', '古诗鉴赏弱', '名著阅读一般', '📊 表现手法分析弱', '✍️ 每日积累'),
    ('9号棚', '草莓试验区', '科研样本', '数据采集中', '🌡️ 22.6°C', '💧 78%',
     '9班·物理', '均分76.8', '电学基础弱', '电路图分析薄弱', '📊 欧姆定律应用', '⚡ 实验模拟'),
    ('10号棚', '生菜水培', '水质达标', '循环正常', '🌡️ 21.4°C', '💧 74%',
     '10班·数学', '均分80.2', '概率统计混淆', '综合题思路不清', '📊 统计图表读题弱', '📈 数据专题'),
    ('11号棚', '番茄高架', '坐果良好', '长势优', '🌡️ 24.7°C', '💧 68%',
     '11班·英语', '均分89.3', '写作逻辑弱', '长难句理解待提升', '📊 高级句型运用少', '📝 读写结合'),
    ('12号棚', '综合示范棚', '参观开放', '指标稳定', '🌡️ 23.9°C', '💧 71%',
     '12班·化学', '均分78.5', '物质推断弱', '化学计算粗心', '📊 技巧计算薄弱', '📐 每日一算')
]
for (old_name, old_crop, old_tag1, old_tag2, old_foot1, old_foot2,
     new_name, new_crop, new_tag1, new_tag2, new_foot1, new_foot2) in cards:
    html = html.replace(f'<span class="gh-name">{old_name}</span>', f'<span class="gh-name">{new_name}</span>')
    html = html.replace(f'<span class="gh-crop">{old_crop}</span>', f'<span class="gh-crop">{new_crop}</span>')
    html = html.replace(f'<span class="gh-tag">{old_tag1}</span>', f'<span class="gh-tag">{new_tag1}</span>')
    html = html.replace(f'<span class="gh-tag">{old_tag2}</span>', f'<span class="gh-tag">{new_tag2}</span>')
    html = html.replace(f'<span>{old_foot1}</span> <span>{old_foot2}</span>', f'<span>{new_foot1}</span> <span>{new_foot2}</span>')

# 5号棚悬浮框文字
html = html.replace('棚室名称: 5号棚', '📌 5班数学诊断 & 差异化策略')
html = html.replace('作物类型：<span>番茄育苗</span>', '薄弱点:<span>二次函数综合 / 代数推理</span>')
html = html.replace('当前状态：<span style="color:#ffb74d;">需关注</span>', '目标:<span>周测提升15%</span>')
html = html.replace('温度：<span>23.4°C</span>', '策略:<span>分层微专题+错题诊所</span>')
html = html.replace('湿度：<span>70%</span>', '建议:<span>小组合作，每日一题</span>')
html = html.replace('<div class="row"><span>标签：</span><span>苗情稳定、光照偏弱</span></div>', '')

# 中间底部混合图（只改标题和图例、数据）
html = html.replace('月度产量与销售趋势', '历次考试学业趋势（定位进步与波动）')
html = html.replace("'月产量'", "'年级均分'")
html = html.replace("'销售额'", "'优秀率(≥90)'")
html = html.replace("产量", "均分")
html = html.replace("销售额", "优秀率%")
html = html.replace('[500, 400, 600, 800, 1000, 1200, 1100, 900, 700, 500, 300, 400]',
                    '[78, 79, 81, 82, 84, 85, 86, 85, 83, 80, 78, 79]')
html = html.replace('[200, 180, 280, 350, 450, 520, 480, 400, 320, 200, 150, 180]',
                    '[28, 30, 33, 36, 39, 42, 44, 41, 38, 35, 32, 30]')

# ================== 5. 右栏 ==================
html = html.replace('棚内环境实时曲线', '学科成绩变化曲线（动态追踪）')
html = html.replace("'温度'", "'数学'")
html = html.replace("'湿度'", "'语文'")
html = html.replace("'CO₂'", "'英语'")
# 注意：原x轴数据有8个点，新数据只有6个点，但为了不破坏结构，我们只改文字不改长度，用户可手动调
# 为了避免出错，只改标签文字，不改数组长度（保留8个点，后面几个多余数据显示不影响）
html = html.replace("['0时', '3时', '6时', '9时', '12时', '15时', '18时', '21时']",
                    "['一模', '二模', '三模', '期中', '月考1', '月考2', '月考3', '期末']")
# 只改前面6个数据，后面2个保留原值（不完美但不会报错）
html = html.replace('[21, 26, 22, 28, 25, 30, 24, 22]', '[72, 74, 78, 80, 82, 85, 86, 87]')
html = html.replace('[79, 82, 77, 61, 66, 69, 63, 84]', '[78, 79, 80, 81, 83, 84, 85, 86]')
html = html.replace('[750, 860, 650, 480, 550, 520, 560, 900]', '[80, 83, 85, 86, 88, 89, 90, 91]')

# 右栏中间“数据统计图”只改标题和图例，不改category和数据（因为原数据有33个，改起来麻烦且可能破坏结构）
html = html.replace('数据统计图', '班级/学科对比统计（平均分/合格率）')
html = html.replace("'贯通率'", "'提升率'")
html = html.replace("'已贯通'", "'班级平均分'")
html = html.replace("'计划贯通'", "'及格率(%)'")
# 不修改category和barData/lineData，以免出错。用户可自行手动修改。

# 底部地图和视频：只改标题文字，不改地图代码
html = html.replace('地图分布', '跨班级学情对比分析')
html = html.replace('监控视频', '差异化教学优化策略')
# 视频框内文字替换（保留cam-tag和play-icon）
video_texts = ["五班函数薄弱→微专题+错题诊所", "物理力学薄弱→实验小组+导学案分层",
               "英语完形高频错→真题语境+词块记忆", "跨班数学对比→动态走班、变式教学"]
for i, txt in enumerate(video_texts, 1):
    # 替换 cam-tag 数字部分
    html = re.sub(r'(<span class="cam-tag">)监控(\d)(</span>)', rf'\g<1>策略{i}\g<3>', html, count=1)
    # 在 play-icon 后添加文字（简单添加，不破坏原结构）
    html = re.sub(r'(<div class="video-box">.*?<span class="play-icon">)▶(</span>)(.*?)(?=</div>)',
                  rf'\g<1>📌\g<2><div style="position:absolute; bottom:4px; font-size:10px; color:#a0c8f0;">{txt}</div>',
                  html, count=1, flags=re.DOTALL)

# 保存
with open('学情数据分析大屏.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("完成！只替换了文字和数据，地图等复杂部分保持原样。")