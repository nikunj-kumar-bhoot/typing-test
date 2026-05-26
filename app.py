import streamlit as st
import time
import random

# ---------------------------------------------------------
# 1. TEXT DATA POOLS
# ---------------------------------------------------------
SENTENCES = [
    "The quick brown fox jumps over the lazy dog.",
    "Success is not final, failure is not fatal: it is the courage to continue that counts.",
    "Coding is the closest thing we have to a superpower in the modern world.",
    "The beautiful thing about learning is that no one can take it away from you.",
    "Artificial intelligence is growing at an unprecedented pace these days.",
    "A journey of a thousand miles begins with a single step.",
    "Please make sure to wash your hands before preparing dinner.",
    "The weather forecast predicts heavy rain and strong winds for tomorrow afternoon.",
    "She sells sea shells by the sea shore on a sunny day.",
    "Patience and perseverance have a magical effect before which difficulties disappear.",
    "You can write code that a computer understands, but good programmers write code that humans understand.",
    "The solar system consists of the sun and all the celestial objects bound to it by gravity.",
    "Reading books is a wonderful way to expand your vocabulary and imagination.",
    "The coffee shop on the corner always smells like freshly ground espresso.",
    "Consistency is much more important than perfection when building a new habit.",
    "Light travels at an incredible speed of approximately three hundred thousand kilometers per second.",
    "Don't count the days, make the days count.",
    "The museum featured a stunning collection of ancient artifacts and modern art.",
    "Taking a deep breath can help reduce stress and improve your focus immediately.",
    "The internet has completely transformed the way people communicate and share information.",
    "Practice makes perfect, so keep typing as fast and accurately as you can.",
    "Trees play a crucial role in absorbing carbon dioxide and producing oxygen.",
    "An apple a day keeps the doctor away, or so the old saying goes.",
    "The orchestra played a beautiful symphony that captivated the entire audience.",
    "Learning a new language opens up a whole world of cultural experiences.",
    "The early bird catches the worm, but the second mouse gets the cheese.",
    "Innovation distinguishes between a leader and a follower in any industry.",
    "Mountains look absolutely majestic when the peak is covered in fresh winter snow.",
    "A regular exercise routine can significantly boost your physical and mental health.",
    "Always remember to back up your important computer files to an external drive.",
    "The ocean covers more than seventy percent of the planet's surface.",
    "To be or not to be, that is the ultimate question.",
    "The rapid growth of technology has created many exciting new career paths.",
    "A warm cup of tea on a rainy afternoon is incredibly comforting.",
    "Space exploration helps us understand our place in this vast universe.",
    "Do not go where the path may lead, go instead where there is no path and leave a trail.",
    "Computers process millions of instructions per second without breaking a sweat.",
    "The smell of old books always brings back fond memories of childhood libraries.",
    "Believe you can and you are already halfway there.",
    "Time flies like an arrow, but fruit flies like a banana."
]

PARAGRAPHS = [
    "Technology has fundamentally altered the fabric of human existence over the last few decades. What started as basic automation has blossomed into a complex digital ecosystem that governs our daily routines. We rely on smartphones for communication, artificial intelligence for decision-making, and the internet for an infinite stream of information. While these advancements have brought undeniable convenience and connectivity, they also challenge our attention spans and privacy. Striking a healthy balance between the virtual world and physical reality is one of the greatest challenges of modern life. As we move forward, humanity must shape technology mindfully.",
    "The cosmos has always captured the human imagination with its vast, silent grandeur. Beyond our tiny blue planet lies an infinite expanse filled with billions of galaxies, each hosting countless stars and mysterious worlds. Astronomers use powerful space telescopes to peer deep into the past, capturing ancient light from the very edge of the observable universe. Every discovery reveals something incredible, from swirling nebulae where new stars are born to massive black holes that distort time itself. Exploring the universe reminds us of how small we are, yet it highlights our unique capacity to wonder, learn, and explore.",
    "Reading a well-written book is like stepping into a time machine or opening a portal to another dimension. Without moving a single inch, a reader can experience the bustling streets of ancient Rome, explore distant futuristic planets, or feel the deep emotions of a stranger. Literature allows us to build empathy by stepping into characters' shoes and seeing the world through entirely different perspectives. In a fast-paced digital world dominated by fleeting video clips, the quiet act of reading remains a powerful anchor. It sharpens our minds, expands our vocabularies, and keeps the imagination alive and thriving.",
    "Nature operates in a delicate, beautiful balance where every living organism plays a vital role. From the smallest microscopic bacteria in the soil to the massive whales swimming in the deep blue ocean, all creatures are interconnected. Forests act as the planet's lungs, absorbing carbon dioxide and providing clean oxygen, while rivers deliver life-giving water across vast continents. However, human industrial activity has disrupted these natural cycles, causing climate patterns to shift unpredictably. Protecting our environment is no longer just a kind gesture; it is a critical necessity for ensuring the survival of future generations on Earth.",
    "Cooking is a beautiful blend of precise science and creative artistic expression. It transforms raw, simple ingredients into delightful culinary experiences that engage all five human senses. A chef acts like a scientist when balancing acidic flavors with fats, or using precise heat to create a perfect golden crust. At the same time, choosing vibrant colors and arranging components on a plate requires the eye of a skilled painter. Beyond the physical nutrition it provides, sharing a homemade meal brings people together, fostering deep conversation and creating lasting memories around the dinner table across every culture."
]

# ---------------------------------------------------------
# 2. STATE MANAGER INITIALIZATION
# ---------------------------------------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "LOBBY"  
    st.session_state.s1_count = 0
    st.session_state.s1_times = []
    st.session_state.s1_accs = []
    st.session_state.s1_wpms = []
    st.session_state.available_sentences = SENTENCES.copy()
    st.session_state.current_text = ""
    st.session_state.start_time = 0.0

st.set_page_config(page_title="SpeedyType Test", page_icon="⌨️", layout="centered")
st.title("⌨️ Ultimate Typing Speed Test")

# ANTI-CHEAT SECURITY: Disables highlight selection, text copying, and right-click menus app-wide
st.markdown(
    """
    <style>
    body, html, [data-testid="stMarkdownContainer"], p, h1, h2, h3, h4, code {
        -webkit-user-select: none; /* Safari */
        -moz-user-select: none;    /* Firefox */
        -ms-user-select: none;     /* IE10+ */
        user-select: none;         /* Standard */
    }
    input, textarea {
        -webkit-user-select: text !important;
        -moz-user-select: text !important;
        -ms-user-select: text !important;
        user-select: text !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def reset_test():
    st.session_state.stage = "LOBBY"
    st.session_state.s1_count = 0
    st.session_state.s1_times = []
    st.session_state.s1_accs = []
    st.session_state.s1_wpms = []
    st.session_state.available_sentences = SENTENCES.copy()
    st.session_state.current_text = ""

# ---------------------------------------------------------
# 3. GAME RUNNER
# ---------------------------------------------------------

# --- STAGE: LOBBY ---
if st.session_state.stage == "LOBBY":
    st.markdown("""
    Welcome! Test your typing efficiency and accuracy across two challenging stages.
    
    ### 📊 Test Structure
    * **Stage 1:** You will be given a set of **5 random sentences**, presented one by one.
    * **Stage 2:** You will be given a **short paragraph** to type out completely.
    """)
    
    st.info("""
    💡 **Important Instruction for Players:** To ensure your timer tracks your speed accurately, **please click or tap inside the text input field ("Your input:") at the start of each new round** to activate your cursor and keyboard before you begin typing.
    """)
    
    st.markdown("*Press the button below when you are ready to begin. ALL THE BEST!*")
    
    if st.button("🚀 Start Typing Test", use_container_width=True):
        st.session_state.stage = "STAGE1"
        st.session_state.s1_count = 1
        st.session_state.current_text = random.choice(st.session_state.available_sentences)
        st.session_state.available_sentences.remove(st.session_state.current_text)
        st.session_state.start_time = time.time()
        st.rerun()

# --- STAGE: 1 (SENTENCES) ---
elif st.session_state.stage == "STAGE1":
    st.header(f"📌 Stage 1: Single Sentences ({st.session_state.s1_count} of 5)")
    st.info("👉 Click the text box below to start typing, then press Enter or click submit:")
    
    st.markdown(f"#### `{st.session_state.current_text}`")
    
    with st.form(key=f"s1_form_{st.session_state.s1_count}", clear_on_submit=True):
        user_input = st.text_input(
            "Your input:", 
            key=f"input_s1_{st.session_state.s1_count}", 
            autocomplete="off"
        )
        submit_btn = st.form_submit_button("Submit Sentence", use_container_width=True)
        
        if submit_btn:
            end_time = time.time()
            elapsed_time = max(end_time - st.session_state.start_time, 0.1)
            
            words = st.session_state.current_text.split()
            correct_words = sum(1 for w in user_input.split() if w in words)
            accuracy = (correct_words / len(words)) * 100 if len(words) > 0 else 0
            wpm = (len(user_input.split()) / elapsed_time) * 60
            
            st.session_state.s1_times.append(elapsed_time)
            st.session_state.s1_accs.append(accuracy)
            st.session_state.s1_wpms.append(wpm)
            
            if st.session_state.s1_count < 5:
                st.session_state.s1_count += 1
                st.session_state.current_text = random.choice(st.session_state.available_sentences)
                st.session_state.available_sentences.remove(st.session_state.current_text)
                st.session_state.start_time = time.time()
                st.rerun()
            else:
                st.session_state.stage = "STAGE2"
                st.session_state.current_text = random.choice(PARAGRAPHS)
                st.session_state.start_time = time.time()
                st.rerun()

# --- STAGE: 2 (PARAGRAPH) ---
elif st.session_state.stage == "STAGE2":
    st.header("📌 Stage 2: The Paragraph")
    st.warning("👉 Click the text area below to start typing. Click 'Submit Paragraph' when finished:")
    
    st.write(st.session_state.current_text)
    
    with st.form(key="s2_form", clear_on_submit=True):
        user_input = st.text_area("Your input:", key="input_s2", height=150)
        submit_btn = st.form_submit_button("Submit Paragraph", use_container_width=True)
        
        if submit_btn:
            end_time = time.time()
            st.session_state.s2_time = max(end_time - st.session_state.start_time, 0.1)
            
            words = st.session_state.current_text.split()
            correct_words = sum(1 for w in user_input.split() if w in words)
            st.session_state.s2_acc = (correct_words / len(words)) * 100 if len(words) > 0 else 0
            st.session_state.s2_wpm = (len(user_input.split()) / st.session_state.s2_time) * 60
            
            st.session_state.stage = "RESULTS"
            st.rerun()

# --- STAGE: RESULTS & ANALYTICS ---
elif st.session_state.stage == "RESULTS":
    st.header("📊 Results & Analysis")
    
    stg1time = sum(st.session_state.s1_times)
    stg1acc = sum(st.session_state.s1_accs) / 5
    stg1wpm = sum(st.session_state.s1_wpms) / 5
    
    stg2time = st.session_state.s2_time
    stg2acc = st.session_state.s2_acc
    stg2wpm = st.session_state.s2_wpm

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Stage 1 (Sentences)")
        st.metric(label="Time Taken", value=f"{stg1time:.2f} s")
        st.metric(label="Accuracy", value=f"{stg1acc:.2f}%")
        st.metric(label="Typing Speed", value=f"{stg1wpm:.2f} WPM")
        
    with col2:
        st.subheader("Stage 2 (Paragraph)")
        st.metric(label="Time Taken", value=f"{stg2time:.2f} s")
        st.metric(label="Accuracy", value=f"{stg2acc:.2f}%")
        st.metric(label="Typing Speed", value=f"{stg2wpm:.2f} WPM")
        
    st.markdown("---")
    st.subheader("🏆 Overall Metrics")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Time", value=f"{(stg2time + stg1time):.2f} s")
    m2.metric("Mean Accuracy", value=f"{((stg1acc + stg2acc) / 2):.2f}%")
    m3.metric("Net Typing Speed", value=f"{((stg1wpm + stg2wpm) / 2):.2f} WPM")
    
    if st.button("🔄 Try Again", use_container_width=True):
        reset_test()
        st.rerun()