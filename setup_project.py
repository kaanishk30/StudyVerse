"""
Auto-setup script for AI Study Pal
Run this to create all necessary folders and files
"""
import os

def create_folders():
    """Create necessary folders"""
    folders = ['templates', 'models', 'uploads', 'static']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✓ Created folder: {folder}")
        else:
            print(f"• Folder exists: {folder}")

def create_index_template():
    """Create index_modern.html template"""
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Study Pal - Smart Learning Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #1a202c;
        }
        
        .glass-nav {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 1.5rem;
            font-weight: 800;
            color: white;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .streak-badge {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-weight: 600;
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
        
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .hero-section {
            text-align: center;
            color: white;
            margin-bottom: 3rem;
            animation: fadeInDown 0.6s ease-out;
        }
        
        .hero-section h1 {
            font-size: 3rem;
            font-weight: 900;
            margin-bottom: 1rem;
            text-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
        }
        
        .hero-section p {
            font-size: 1.2rem;
            opacity: 0.95;
            max-width: 600px;
            margin: 0 auto;
        }
        
        .card {
            background: white;
            border-radius: 24px;
            padding: 2.5rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem;
            animation: fadeInUp 0.6s ease-out;
        }
        
        .input-group {
            margin-bottom: 1.5rem;
        }
        
        .input-group label {
            display: block;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #2d3748;
            font-size: 0.95rem;
        }
        
        input[type="text"], textarea {
            width: 100%;
            padding: 1rem;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s;
            font-family: inherit;
        }
        
        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        .file-upload {
            border: 2px dashed #cbd5e0;
            border-radius: 12px;
            padding: 2rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
            background: #f7fafc;
        }
        
        .file-upload:hover {
            border-color: #667eea;
            background: #edf2f7;
        }
        
        .file-upload input {
            display: none;
        }
        
        .btn-primary {
            width: 100%;
            padding: 1.2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
        }
        
        .btn-primary:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 2rem;
        }
        
        .spinner {
            border: 4px solid #f3f4f6;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        
        .results {
            display: none;
        }
        
        .summary-section {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 2rem;
            transition: filter 0.3s;
        }
        
        .summary-section.blurred {
            filter: blur(10px);
            pointer-events: none;
            user-select: none;
        }
        
        .quiz-section {
            background: #f7fafc;
            padding: 2rem;
            border-radius: 16px;
        }
        
        .question-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }
        
        .question-text {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #2d3748;
        }
        
        .options {
            display: grid;
            gap: 0.75rem;
        }
        
        .option {
            padding: 1rem;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            background: white;
        }
        
        .option:hover {
            border-color: #667eea;
            background: #edf2f7;
        }
        
        .option.selected {
            border-color: #667eea;
            background: #e6f0ff;
            font-weight: 600;
        }
        
        .btn-submit-quiz {
            width: 100%;
            padding: 1rem;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 1rem;
        }
        
        .btn-submit-quiz:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(245, 87, 108, 0.4);
        }
        
        .achievement-popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
            z-index: 1000;
            text-align: center;
            transition: transform 0.3s;
            max-width: 400px;
        }
        
        .achievement-popup.show {
            transform: translate(-50%, -50%) scale(1);
        }
        
        .overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            z-index: 999;
        }
        
        .overlay.show {
            display: block;
        }
        
        .profile-link {
            color: white;
            text-decoration: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            transition: all 0.3s;
        }
        
        .profile-link:hover {
            background: rgba(255, 255, 255, 0.3);
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @media (max-width: 768px) {
            .hero-section h1 {
                font-size: 2rem;
            }
            
            .card {
                padding: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <nav class="glass-nav">
        <div class="logo">
            <span>🎓</span> AI Study Pal
        </div>
        <div style="display: flex; gap: 1rem; align-items: center;">
            <div class="streak-badge">
                <span>🔥</span> {{ user.streak }} Day Streak
            </div>
            <a href="/profile" class="profile-link">Profile</a>
        </div>
    </nav>

    <div class="container">
        <div class="hero-section">
            <h1>Learn Smarter, Not Harder</h1>
            <p>AI-powered study assistant with RAG technology. Ask questions, compare concepts, upload your materials, and master any subject.</p>
        </div>

        <div class="card">
            <form id="studyForm">
                <div class="input-group">
                    <label>🔍 What do you want to learn?</label>
                    <input type="text" 
                           name="query" 
                           placeholder="e.g., Machine learning vs Deep learning, Photosynthesis process..."
                           required>
                    <p style="font-size: 0.85rem; color: #718096; margin-top: 0.5rem;">
                        💡 You can ask comparative questions like "difference between X and Y"
                    </p>
                </div>

                <div class="input-group">
                    <label>📝 Your Notes (Optional)</label>
                    <textarea name="user_notes" 
                              placeholder="Paste your class notes, lecture transcripts, or any study material here..."></textarea>
                </div>

                <div class="input-group">
                    <label>📎 Upload Study Materials (Optional)</label>
                    <div class="file-upload" onclick="document.getElementById('fileInput').click()">
                        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📁</div>
                        <p><strong>Click to upload</strong> or drag files here</p>
                        <p style="font-size: 0.85rem; color: #718096; margin-top: 0.5rem;">
                            PDF, PPT, PPTX, TXT • Max 16MB
                        </p>
                        <input type="file" 
                               id="fileInput" 
                               name="files" 
                               multiple 
                               accept=".pdf,.ppt,.pptx,.txt">
                        <div id="fileList" style="margin-top: 1rem; font-size: 0.9rem;"></div>
                    </div>
                </div>

                <button type="submit" class="btn-primary">
                    ✨ Generate Smart Study Plan
                </button>
            </form>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>🧠 AI is analyzing and generating personalized content...</p>
        </div>

        <div class="results" id="results">
            <div class="summary-section" id="summarySection">
                <h2 style="margin-bottom: 1rem;">📚 Summary & Context</h2>
                <div id="summaryContent"></div>
                <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                    <strong>Sources:</strong> <span id="sources"></span>
                </p>
            </div>

            <div class="quiz-section">
                <h2 style="margin-bottom: 1.5rem;">🎯 Interactive Quiz</h2>
                <p style="margin-bottom: 2rem; color: #718096;">
                    Complete the quiz to unlock the full summary above!
                </p>
                <div id="quizContainer"></div>
                <button class="btn-submit-quiz" onclick="submitQuiz()">
                    Submit Answers
                </button>
            </div>
        </div>
    </div>

    <div class="overlay" id="overlay"></div>
    <div class="achievement-popup" id="achievementPopup">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
        <h2 id="achievementTitle"></h2>
        <p id="achievementDesc" style="color: #718096; margin-top: 0.5rem;"></p>
        <button class="btn-primary" onclick="closeAchievement()" style="margin-top: 1.5rem; padding: 0.75rem;">
            Awesome!
        </button>
    </div>

    <script>
        let currentQuestions = [];
        let userAnswers = {};

        document.getElementById('fileInput').addEventListener('change', function(e) {
            const fileList = document.getElementById('fileList');
            const files = Array.from(e.target.files);
            
            if (files.length > 0) {
                fileList.innerHTML = '<strong>Selected files:</strong><br>' + 
                    files.map(f => '• ' + f.name).join('<br>');
            }
        });

        document.getElementById('studyForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.error) {
                    alert(data.error);
                    return;
                }
                
                displayResults(data);
                
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });

        function displayResults(data) {
            document.getElementById('summaryContent').innerHTML = `
                <div style="background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                    <p style="line-height: 1.7;">${data.summary}</p>
                </div>
                <div style="background: white; padding: 1.5rem; border-radius: 12px;">
                    <strong>Preview:</strong>
                    <p style="color: #718096; margin-top: 0.5rem; line-height: 1.6;">${data.content_preview}</p>
                </div>
            `;
            
            document.getElementById('sources').textContent = data.sources.join(', ');
            document.getElementById('summarySection').classList.add('blurred');
            
            currentQuestions = data.questions;
            userAnswers = {};
            
            const quizHTML = data.questions.map((q, index) => `
                <div class="question-card">
                    <div class="question-text">
                        ${index + 1}. ${q.question}
                    </div>
                    <div class="options">
                        ${q.options.map((opt, optIndex) => `
                            <div class="option" onclick="selectOption(${index}, '${opt.replace(/'/g, "\\'")}')">
                                <input type="radio" name="q${index}" value="${opt}" style="margin-right: 0.5rem;">
                                ${opt}
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('');
            
            document.getElementById('quizContainer').innerHTML = quizHTML;
            document.getElementById('results').style.display = 'block';
            document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
        }

        function selectOption(questionIndex, answer) {
            userAnswers[questionIndex] = answer;
            
            const options = document.querySelectorAll(`input[name="q${questionIndex}"]`);
            options.forEach(input => {
                input.parentElement.classList.remove('selected');
                if (input.value === answer) {
                    input.checked = true;
                    input.parentElement.classList.add('selected');
                }
            });
        }

        async function submitQuiz() {
            if (Object.keys(userAnswers).length < currentQuestions.length) {
                alert('Please answer all questions before submitting!');
                return;
            }
            
            try {
                const response = await fetch('/submit_quiz', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ answers: userAnswers })
                });
                
                const data = await response.json();
                
                document.getElementById('summarySection').classList.remove('blurred');
                
                const percentage = data.percentage;
                let message = percentage >= 90 ? 'Outstanding! 🌟' :
                              percentage >= 70 ? 'Great job! 👏' :
                              percentage >= 50 ? 'Good effort! 💪' : 'Keep practicing! 📚';
                
                alert(`${message}\n\nYour Score: ${data.score}/${data.total} (${percentage}%)`);
                
                if (data.new_achievements && data.new_achievements.length > 0) {
                    showAchievement(data.new_achievements[0]);
                }
                
            } catch (error) {
                alert('Error submitting quiz: ' + error.message);
            }
        }

        function showAchievement(achievement) {
            document.getElementById('achievementTitle').textContent = achievement.name;
            document.getElementById('achievementDesc').textContent = achievement.desc;
            document.getElementById('overlay').classList.add('show');
            document.getElementById('achievementPopup').classList.add('show');
        }

        function closeAchievement() {
            document.getElementById('overlay').classList.remove('show');
            document.getElementById('achievementPopup').classList.remove('show');
        }
    </script>
</body>
</html>'''
    
    with open('templates/index_modern.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("✓ Created: templates/index_modern.html")

def create_profile_template():
    """Create profile.html template"""
    profile_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Profile - AI Study Pal</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #1a202c;
        }
        .glass-nav {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .logo { font-size: 1.5rem; font-weight: 800; color: white; }
        .back-link {
            color: white;
            text-decoration: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 20px;
        }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        .stat-card {
            background: white;
            border-radius: 20px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        .stat-icon { font-size: 3rem; margin-bottom: 1rem; }
        .stat-value {
            font-size: 2.5rem;
            font-weight: 900;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stat-label { color: #718096; font-weight: 600; margin-top: 0.5rem; }
        .card {
            background: white;
            border-radius: 24px;
            padding: 2.5rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem;
        }
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.5rem;
            margin-top: 1.5rem;
        }
        .calendar-day {
            aspect-ratio: 1;
            border-radius: 8px;
            background: #f7fafc;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
        }
        .calendar-day.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .achievements-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }
        .achievement {
            background: #f7fafc;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
        }
        .achievement.unlocked {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        }
        .achievement.locked { opacity: 0.5; }
        .achievement-icon { font-size: 3rem; margin-bottom: 0.5rem; }
    </style>
</head>
<body>
    <nav class="glass-nav">
        <div class="logo">🎓 AI Study Pal</div>
        <a href="/" class="back-link">← Back to Study</a>
    </nav>
    <div class="container">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">🔥</div>
                <div class="stat-value">{{ user.streak }}</div>
                <div class="stat-label">Day Streak</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📝</div>
                <div class="stat-value">{{ user.total_quizzes }}</div>
                <div class="stat-label">Quizzes Completed</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-value">
                    {% if user.total_quizzes > 0 %}
                        {{ ((user.correct_answers / user.total_quizzes) * 100) | round(1) }}%
                    {% else %}
                        0%
                    {% endif %}
                </div>
                <div class="stat-label">Accuracy</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🏆</div>
                <div class="stat-value">{{ user.achievements | length }}</div>
                <div class="stat-label">Achievements</div>
            </div>
        </div>
        
        <div class="card">
            <h2>📅 Study Calendar</h2>
            <div class="calendar-grid">
                {% for day in calendar %}
                    <div class="calendar-day {% if day.has_activity %}active{% endif %}">
                        {{ day.date.split('-')[2] }}
                    </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="card">
            <h2>🏆 Achievements</h2>
            <div class="achievements-grid">
                {% for achievement in achievements %}
                    <div class="achievement {% if achievement.unlocked %}unlocked{% else %}locked{% endif %}">
                        <div class="achievement-icon">{{ achievement.name.split()[0] }}</div>
                        <div><strong>{{ achievement.name.split(' ', 1)[1] if ' ' in achievement.name else achievement.name }}</strong></div>
                        <div style="font-size: 0.85rem; color: #718096;">{{ achievement.desc }}</div>
                    </div>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open('templates/profile.html', 'w', encoding='utf-8') as f:
        f.write(profile_html)
    print("✓ Created: templates/profile.html")

if __name__ == "__main__":
    print("🚀 Setting up AI Study Pal project...\n")
    create_folders()
    print()
    create_index_template()
    create_profile_template()
    print("\n✅ Setup complete!")
    print("\n📋 Next steps:")
    print("1. Run: python train_models.py")
    print("2. Run: python app.py")
    print("3. Open: http://127.0.0.1:5000")