from flask import Flask, request, render_template_string
from openai import OpenAI
import os
import csv
import json

app = Flask(__name__)

# =========================================================
# CONFIG
# =========================================================
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# =========================================================
# ANALYSIS LOGIC (using OpenAI API)
# =========================================================
def analyze_transcript(transcript, openai_api_key, model_name="gpt-4o-mini"):
    """
    Analyzes a given transcript using the OpenAI API to get a summary and sentiment.
    """
    client = OpenAI(api_key=openai_api_key)
    
    system_prompt = (
        "You are an expert at analyzing customer transcripts. "
        "Your task is to provide a concise summary (in 2-3 sentences) "
        "and determine the sentiment (Positive, Neutral, or Negative). "
        "Provide your response in a JSON object with 'summary' and 'sentiment' keys."
    )
    
    user_prompt = f"Analyze the following customer transcript: '{transcript}'"
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
        )
        
        response_text = response.choices[0].message.content
        
        # Parse JSON response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            response_data = json.loads(json_str)
            summary = response_data.get('summary', 'Unable to generate summary')
            sentiment = response_data.get('sentiment', 'Unknown')
        else:
            summary = response_text
            sentiment = "Unknown"
            
        return summary, sentiment
    except Exception as e:
        return f"Analysis failed: {str(e)}", "Unknown"


def save_analysis_to_csv(filename, transcript, summary, sentiment):
    """
    Save analysis results to a CSV file.
    """
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Transcript", "Summary", "Sentiment"])
        writer.writerow([transcript, summary, sentiment])


# =========================================================
# FLASK ROUTES
# =========================================================
PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>CUSTOMER'S INTEL • NeonSentience</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        h1 {
            color: #333;
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .subtitle {
            color: #666;
            font-size: 1em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-family: inherit;
            font-size: 1em;
            resize: vertical;
            min-height: 150px;
            transition: border-color 0.3s;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        button {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1.1em;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        button:active {
            transform: translateY(0);
        }
        .result {
            margin-top: 30px;
            padding: 20px;
            background: #f5f5f5;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .result h3 {
            color: #333;
            margin-bottom: 10px;
        }
        .result p {
            color: #555;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        .sentiment-badge {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            margin-top: 10px;
        }
        .sentiment-positive {
            background-color: #d4edda;
            color: #155724;
        }
        .sentiment-neutral {
            background-color: #fff3cd;
            color: #856404;
        }
        .sentiment-negative {
            background-color: #f8d7da;
            color: #721c24;
        }
        .error {
            color: #721c24;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            padding: 12px;
            border-radius: 8px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 CUSTOMER'S INTEL</h1>
            <p class="subtitle">NeonSentience - AI-Powered Transcript Analysis</p>
        </div>
        
        <form method="POST" action="/analyze">
            <div class="form-group">
                <label for="transcript">Paste Customer Transcript:</label>
                <textarea id="transcript" name="transcript" placeholder="Paste the customer transcript here..." required></textarea>
            </div>
            <button type="submit">Analyze Transcript</button>
        </form>
        
        {% if summary and sentiment %}
        <div class="result">
            <h3>Analysis Result:</h3>
            <p><strong>Summary:</strong> {{ summary }}</p>
            <p>
                <strong>Sentiment:</strong>
                <span class="sentiment-badge sentiment-{{ sentiment.lower() }}">{{ sentiment }}</span>
            </p>
        </div>
        {% endif %}
        
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(PAGE_TEMPLATE, summary=None, sentiment=None, error=None)


@app.route("/analyze", methods=["POST"])
def analyze():
    transcript = request.form.get("transcript", "").strip()
    
    if not transcript:
        return render_template_string(PAGE_TEMPLATE, summary=None, sentiment=None, error="Please provide a transcript.")
    
    if not OPENAI_API_KEY:
        return render_template_string(PAGE_TEMPLATE, summary=None, sentiment=None, error="OpenAI API key not configured.")
    
    summary, sentiment = analyze_transcript(transcript, OPENAI_API_KEY, model_name="gpt-4o-mini")
    
    # Save to CSV
    save_analysis_to_csv("analysis_results.csv", transcript, summary, sentiment)
    
    return render_template_string(PAGE_TEMPLATE, summary=summary, sentiment=sentiment, error=None)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
