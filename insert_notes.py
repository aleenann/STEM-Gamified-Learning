import re

FILE_PATH = "c:/Users/DELL/STEM-Gamified-LEarning/STEM-Gamified-Learning/templates/student_dashboard.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

payload = """

                <!-- TOPIC 1 PAGE 1: Intro / Carbs -->
                <div id="bio-t1-carbs">
                    <h2 style="color: #16a34a; margin-bottom: 1.5rem;"><i class="fa-solid fa-leaf"></i> Chapter 1: Mindful Eating: A Path to a Healthy Body</h2>
                    <h3 class="mb-1" style="font-size: 1.8rem;">Topic 1: What are Nutrients?</h3>
                    <p class="text-muted mb-2 text-lg">Nutrients are the useful substances present in food that our body needs to get energy, grow, and stay healthy.</p>

                    <div class="bio-card" style="border-left-color: #f59e0b; background: #fffbeb;">
                        <h4 style="font-size: 1.5rem; color: #d97706; margin-bottom: 1rem;">1️⃣ Carbohydrates (Energy-giving food) ⚡</h4>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-bolt text-warning"></i> <strong>Function:</strong> Main source of energy</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-person-running text-primary"></i> <strong>Why needed?</strong> Helps us do daily activities like walking, playing, studying</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-bowl-rice text-muted"></i> <strong>Sources:</strong> Rice, wheat, bread, potato, sugar</p>
                        <div style="text-align: center; margin-top: 1.5rem;">
                            <img src="/static/games/grade6/biology/carbohydrates_food_1774280618546.png" class="bio-img" style="border-color: #f59e0b;" alt="Carbohydrates">
                        </div>
                    </div>
                    
                    <div style="text-align: right; margin-top: 2rem;">
                        <button class="menu-btn" onclick="document.getElementById('bio-t1-carbs').style.display='none'; document.getElementById('bio-t1-proteins').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;">Next: Proteins <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>

                <!-- TOPIC 1 PAGE 2: Proteins -->
                <div id="bio-t1-proteins" style="display: none;">
                    <h2 style="color: #16a34a; margin-bottom: 1.5rem;"><i class="fa-solid fa-leaf"></i> Chapter 1: Mindful Eating: A Path to a Healthy Body</h2>
                    <h3 class="mb-1" style="font-size: 1.8rem;">Topic 1: What are Nutrients?</h3>
                    
                    <div class="bio-card" style="border-left-color: #ef4444; background: #fef2f2;">
                        <h4 style="font-size: 1.5rem; color: #b91c1c; margin-bottom: 1rem;">2️⃣ Proteins (Body-building food) 🏗️</h4>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-dumbbell text-danger"></i> <strong>Function:</strong> Body building and repair</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-child-reaching text-primary"></i> <strong>Why needed?</strong> Helps in growth and repairing damaged tissues</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-egg text-muted"></i> <strong>Sources:</strong> Eggs, milk, pulses, beans, fish</p>
                        <div style="text-align: center; margin-top: 1.5rem;">
                            <img src="/static/games/grade6/biology/proteins_food_1774280981693.png" class="bio-img" style="border-color: #ef4444;" alt="Proteins">
                        </div>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
                        <button class="btn-logout" onclick="document.getElementById('bio-t1-proteins').style.display='none'; document.getElementById('bio-t1-carbs').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;"><i class="fa-solid fa-arrow-left mr-1"></i> Previous</button>
                        <button class="menu-btn" onclick="document.getElementById('bio-t1-proteins').style.display='none'; document.getElementById('bio-t1-fats').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;">Next: Fats <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>

                <!-- TOPIC 1 PAGE 3: Fats -->
                <div id="bio-t1-fats" style="display: none;">
                    <h2 style="color: #16a34a; margin-bottom: 1.5rem;"><i class="fa-solid fa-leaf"></i> Chapter 1: Mindful Eating: A Path to a Healthy Body</h2>
                    <h3 class="mb-1" style="font-size: 1.8rem;">Topic 1: What are Nutrients?</h3>
                    
                    <div class="bio-card" style="border-left-color: #eab308; background: #fefce8;">
                        <h4 style="font-size: 1.5rem; color: #a16207; margin-bottom: 1rem;">3️⃣ Fats 🔋</h4>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-battery-full text-success"></i> <strong>Function:</strong> Provide and store energy</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-fire text-danger"></i> <strong>Why needed?</strong> Gives more energy than carbohydrates and keeps body warm</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-bottle-droplet text-muted"></i> <strong>Sources:</strong> Butter, oil, ghee, nuts (Eat in small amounts!)</p>
                        <div style="text-align: center; margin-top: 1.5rem;">
                            <img src="/static/games/grade6/biology/fats_food_1774281520205.png" class="bio-img" style="border-color: #eab308;" alt="Fats">
                        </div>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
                        <button class="btn-logout" onclick="document.getElementById('bio-t1-fats').style.display='none'; document.getElementById('bio-t1-proteins').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;"><i class="fa-solid fa-arrow-left mr-1"></i> Previous</button>
                        <button class="menu-btn" onclick="document.getElementById('bio-t1-fats').style.display='none'; document.getElementById('bio-t1-vitamins').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;">Next: Vitamins & Minerals <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>

                <!-- TOPIC 1 PAGE 4: Vitamins & Minerals -->
                <div id="bio-t1-vitamins" style="display: none;">
                    <h2 style="color: #16a34a; margin-bottom: 1.5rem;"><i class="fa-solid fa-leaf"></i> Chapter 1: Mindful Eating: A Path to a Healthy Body</h2>
                    <h3 class="mb-1" style="font-size: 1.8rem;">Topic 1: What are Nutrients?</h3>
                    
                    <div class="bio-card" style="border-left-color: #10b981; background: #ecfdf5; margin-bottom: 1rem;">
                        <h4 style="font-size: 1.5rem; color: #047857; margin-bottom: 1rem;">4️⃣ Vitamins (Protective food) 🛡️</h4>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-shield-halved text-success"></i> <strong>Function:</strong> Protect from diseases</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-heart-pulse text-danger"></i> <strong>Why needed?</strong> Keeps body functions normal and improves immunity</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-apple-whole text-muted"></i> <strong>Sources:</strong> Fruits and vegetables (like orange, carrot, spinach)</p>
                    </div>

                    <div class="bio-card" style="border-left-color: #8b5cf6; background: #f5f3ff;">
                        <h4 style="font-size: 1.5rem; color: #6d28d9; margin-bottom: 1rem;">5️⃣ Minerals 🦴</h4>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-bone text-muted"></i> <strong>Function:</strong> Strong bones, teeth, and body functions</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-arrow-up-right-dots text-primary"></i> <strong>Why needed?</strong> Helps in proper growth and maintaining health</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-flask text-muted"></i> <strong>Examples:</strong> Calcium, Iron</p>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
                        <button class="btn-logout" onclick="document.getElementById('bio-t1-vitamins').style.display='none'; document.getElementById('bio-t1-fats').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;"><i class="fa-solid fa-arrow-left mr-1"></i> Previous</button>
                        <button class="menu-btn" onclick="document.getElementById('bio-t1-vitamins').style.display='none'; document.getElementById('bio-t1-water').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;">Next: Water & Roughage <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>

                <!-- TOPIC 1 PAGE 5: Water and Roughage -->
                <div id="bio-t1-water" style="display: none;">
                    <h2 style="color: #16a34a; margin-bottom: 1.5rem;"><i class="fa-solid fa-leaf"></i> Chapter 1: Mindful Eating: A Path to a Healthy Body</h2>
                    <h3 class="mb-1" style="font-size: 1.8rem;">Other Important Components 💧</h3>
                    
                    <div class="bio-card" style="border-left-color: #3b82f6; background: #eff6ff; margin-bottom: 1rem;">
                        <h4 style="font-size: 1.5rem; color: #1d4ed8; margin-bottom: 1rem;">💦 Water</h4>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-glass-water text-primary"></i> <strong>Benefits:</strong> Helps in digestion, transports nutrients, removes waste from body</p>
                    </div>

                    <div class="bio-card" style="border-left-color: #84cc16; background: #f7fee7;">
                        <h4 style="font-size: 1.5rem; color: #4d7c0f; margin-bottom: 1rem;">🌾 Roughage (Dietary Fibre)</h4>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-wheat-awn text-success"></i> <strong>Benefits:</strong> Helps in easy digestion, prevents constipation</p>
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-apple-whole text-muted"></i> <strong>Found in:</strong> Fruits, vegetables, whole grains</p>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
                        <button class="btn-logout" onclick="document.getElementById('bio-t1-water').style.display='none'; document.getElementById('bio-t1-vitamins').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;"><i class="fa-solid fa-arrow-left mr-1"></i> Previous</button>
                        <button class="menu-btn" onclick="document.getElementById('bio-t1-water').style.display='none'; document.getElementById('bio-t1-balance').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;">Next: Balanced Diet <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>

                <!-- TOPIC 1 PAGE 6: Balanced Diet -->
                <div id="bio-t1-balance" style="display: none;">
                    <h2 style="color: #16a34a; margin-bottom: 1.5rem;"><i class="fa-solid fa-leaf"></i> Chapter 1: Mindful Eating: A Path to a Healthy Body</h2>
                    <h3 class="mb-1" style="font-size: 1.8rem;">Balanced Diet ⚖️</h3>
                    
                    <div class="bio-card" style="border-left-color: #6366f1; background: #eef2ff;">
                        <p style="font-size: 1.2rem; margin-bottom: 0.5rem;"><i class="fa-solid fa-scale-balanced text-primary"></i> <strong>What is it?</strong> A diet that contains all nutrients in the right proportion.</p>
                        <p style="font-size: 1.2rem; margin-bottom: 1rem;"><i class="fa-solid fa-plus text-muted"></i> <strong>Includes:</strong> Carbohydrates + Proteins + Fats + Vitamins + Minerals + Water + Roughage.</p>
                        <div style="background: white; padding: 15px; border-radius: 8px; border: 2px dashed #818cf8; text-align: center;">
                            <p style="font-size: 1.3rem; font-weight: bold; color: #4338ca; margin: 0;">👉 Ensures proper growth and good health!</p>
                        </div>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
                        <button class="btn-logout" onclick="document.getElementById('bio-t1-balance').style.display='none'; document.getElementById('bio-t1-water').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;"><i class="fa-solid fa-arrow-left mr-1"></i> Previous</button>
                        <button class="menu-btn" onclick="document.getElementById('bio-t1-balance').style.display='none'; document.getElementById('bio-vita').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;">Topic 2: Vitamin Deep Dive <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>

                <!-- TOPIC 2 PAGE 1: Vitamin A -->
                <div id="bio-vita" style="display: none;">
"""

if '<div id="bio-vita">' in content:
    content = content.replace('<div id="bio-vita">', payload)

    # We also need to fix the Previous button inside bio-vita so it targets the intro page (bio-t1-balance) instead of just doing nothing!
    # Let's find: `</div>\n                </div>\n\n                <!-- Page 2: Vitamin B1 -->`
    # Wait, in the HTML, bio-vita's block only has a "Next" button because it used to be the first page:
    # `<div style="text-align: right; margin-top: 2rem;">\n                        <button class="menu-btn" onclick="document.getElementById('bio-vita').style.display='none'; document.getElementById('bio-vitb1').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;">Next: Vitamin B₁ <i class="fa-solid fa-arrow-right ml-1"></i></button>\n                    </div>`

replacement_nav = """
                    <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
                        <button class="btn-logout" onclick="document.getElementById('bio-vita').style.display='none'; document.getElementById('bio-t1-balance').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;"><i class="fa-solid fa-arrow-left mr-1"></i> Previous: Balanced Diet</button>
                        <button class="menu-btn" onclick="document.getElementById('bio-vita').style.display='none'; document.getElementById('bio-vitb1').style.display='block'; window.scrollTo(0,0);" style="width: auto; display: inline-block;">Next: Vitamin B₁ <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
"""

# Try replacing the nav in bio-vita
content = re.sub(r'<div style="text-align: right; margin-top: 2rem;">\s*<button class="menu-btn" onclick="document.getElementById\(\'bio-vita\'\)\.style\.display=\'none\'; document.getElementById\(\'bio-vitb1\'\)\.style\.display=\'block\'; window\.scrollTo\(0,0\);"[^>]+>Next: Vitamin B₁ <i class="fa-solid fa-arrow-right ml-1"></i></button>\s*</div>', replacement_nav, content)

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated successfully via python script.")
