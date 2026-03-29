import streamlit as st
from openai import OpenAI
import json
import plotly.graph_objects as go

# 一、 页面全局配置
st.set_page_config(page_title="AI 品牌文案策略诊断罗盘", layout="wide")
st.title("🎯 AI 品牌文案策略诊断罗盘")
st.markdown("### 将感性的文字，转化为理性的数据可视化资产 (Powered by DeepSeek)")
st.divider()

# 二、 侧边栏配置区
st.sidebar.header("系统安全配置")
api_key = st.sidebar.text_input("请输入 DeepSeek API Key", type="password")
st.sidebar.markdown("---")
st.sidebar.info("💡 **本系统评估维度说明：**\n\n1. **传播记忆度**：好不好记\n2. **情感共鸣力**：能不能打动人\n3. **商业转化力**：能不能带货\n4. **品牌契合度**：符不符合品牌调性\n5. **差异化竞争**：有没有自身特色")

# 三、 主操作区：输入待诊断的文案
st.subheader("第一步：输入待诊断的品牌内容")

col1, col2 = st.columns([1, 2])
with col1:
    brand_name = st.text_input("品牌/产品名称", value="遂宁姜糕")
    brand_tone = st.text_input("设定的品牌调性", value="国潮非遗、养生治愈、年轻化")
with col2:
    copy_text = st.text_area("粘贴需要诊断的营销文案（或广告语）", height=130,
                             value="一口甜，百年轻。遂宁姜糕，非遗手工揉捏。早 C 晚 A 不如带包姜糕回家，暖胃更暖心，国潮新青年的养生口袋包。")

st.divider()

# 四、 核心逻辑与可视化呈现区
if st.button("🚀 启动策略诊断引擎", use_container_width=True):
    if not api_key:
        st.error("请先在左侧输入 API Key！")
    elif not copy_text:
        st.warning("请输入需要诊断的文案！")
    else:
        try:
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
            
            # 这是一个非常硬核的 Prompt，强制 AI 返回标准的 JSON 数据，而不是普通文本
            prompt = f"""
            你是一位顶级的国际 4A 广告公司策略总监。
            请评估以下文案：
            品牌：{brand_name}
            设定调性：{brand_tone}
            待评估文案："{copy_text}"
            
            请严格从以下 5 个维度对文案进行打分（0-100分）：
            1. 传播记忆度 (memory)
            2. 情感共鸣力 (emotion)
            3. 商业转化力 (conversion)
            4. 品牌契合度 (brand_fit)
            5. 差异化竞争 (differentiation)
            
            你必须以 JSON 格式返回结果。不要有任何多余的解释，不要带 Markdown 格式的 ```json ```，只输出纯 JSON 字符串！
            格式如下：
            {{
                "scores": {{
                    "传播记忆度": 85,
                    "情感共鸣力": 70,
                    "商业转化力": 80,
                    "品牌契合度": 90,
                    "差异化竞争": 75
                }},
                "total_score": 80,
                "expert_review": "一段 100 字左右的犀利总评，指出核心问题。",
                "improvement_suggestion": "一段 100 字左右的修改建议。"
            }}
            """

            with st.spinner("系统正在进行多维度语义拆解与策略评估，生成可视化罗盘中..."):
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一个只输出标准 JSON 格式数据的策略评估机器。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3 # 降低发散性，保证数据格式精准
                )
                
                # 获取 AI 结果并清理可能的 Markdown 格式干扰
                raw_result = response.choices[0].message.content
                raw_result = raw_result.replace("```json", "").replace("```", "").strip()
                
                # 将文本转化为 Python 可以读取的数据字典
                data = json.loads(raw_result)
                
                # --- 开始绘制雷达图 ---
                categories = list(data["scores"].keys())
                values = list(data["scores"].values())
                
                # Plotly 图表配置
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=values + [values[0]], # 闭合雷达图
                    theta=categories + [categories[0]],
                    fill='toself',
                    fillcolor='rgba(255, 90, 90, 0.4)',
                    line=dict(color='rgb(255, 90, 90)', width=2),
                    name=brand_name
                ))
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0, 100])
                    ),
                    showlegend=False,
                    margin=dict(l=40, r=40, t=40, b=40) # 调整边距
                )

                # --- 界面排版展示 ---
                st.subheader("📊 诊断结果看板")
                
                # 使用三个栏位展示分数和图表
                res_col1, res_col2 = st.columns([1.5, 1])
                
                with res_col1:
                    # 在网页上渲染互动图表
                    st.plotly_chart(fig, use_container_width=True)
                
                with res_col2:
                    st.metric(label="综合策略得分", value=f"{data['total_score']} 分")
                    st.markdown("### 💡 总监点评")
                    st.info(data['expert_review'])
                    st.markdown("### 🛠️ 优化建议")
                    st.success(data['improvement_suggestion'])

        except Exception as e:
            st.error(f"分析失败，可能是数据格式解析异常或网络问题。错误信息：{e}")