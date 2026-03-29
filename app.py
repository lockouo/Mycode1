import streamlit as st
from openai import OpenAI

# 一、 页面全局配置与UI排版
st.set_page_config(page_title="AI 品牌营销文案生成引擎", layout="centered")
st.title("AI 品牌营销文案生成引擎")
st.markdown("### 专为广告策划与品牌营销设计的提效辅助系统 (Powered by DeepSeek)")
st.divider()

# 二、 侧边栏配置区
st.sidebar.header("系统配置")
st.sidebar.markdown("请在此输入您的 DeepSeek API Key 以激活引擎。")
api_key = st.sidebar.text_input("DeepSeek API Key", type="password")

# 三、 主操作区：输入产品营销参数
st.subheader("一、 输入营销策略参数")
# 这里的 value="遂宁姜糕" 只是默认显示文本，网页运行后可随意修改
product_name = st.text_input("产品/项目名称", value="遂宁姜糕")
selling_points = st.text_area("核心品牌卖点", value="百年非遗工艺，全新国潮包装设计，便携式独立小包装，口感软糯养生")
target_audience = st.selectbox("核心目标受众群", ["年轻世代国潮爱好者", "注重健康养生的中老年群体", "具有伴手礼/节庆送礼需求的人群"])
copy_style = st.selectbox("预设文案输出风格", ["小红书平台种草风（强网感/带Emoji）", "电商详情页转化风（重理性诉求与功能介绍）", "品牌公关新闻稿（严肃/企业视角）"])

st.divider()

# 四、 核心逻辑区：调用 DeepSeek 大模型
st.subheader("二、 智能生成结果")
if st.button("启动引擎，生成营销文案"):
    if not api_key:
        st.error("操作受阻：系统未检测到有效的 API Key，请先在左侧边栏完成配置。")
    else:
        try:
            # 配置 DeepSeek 客户端
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
            
            # 构建专业级提示词 (Prompt)
            prompt = f"""
            产品名称：{product_name}
            核心卖点：{selling_points}
            目标受众：{target_audience}
            文案风格：{copy_style}
            
            请严格按照上述设定的风格，撰写一段高质量的营销文案。字数控制在 300 - 400 字之间，要求排版清晰，具备直接落地的商业价值。
            """

            with st.spinner("DeepSeek 引擎正在进行语义构建与策略推演，请稍候..."):
                # 调用 DeepSeek-Chat 模型
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "你是一位资深广告文案与营销策划师。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )
                
                st.success("文案生成完毕：")
                # 提取并展示最终文本
                st.write(response.choices[0].message.content)
                
        except Exception as e:
            st.error(f"引擎运行异常，请检查网络或 API Key 的有效性。系统报错信息：{e}")