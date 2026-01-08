from flask import Flask, request, render_template_string
from groq import Groq
import os
import csv
import json

app = Flask(__name__)

# =========================================================
# CONFIG
# =========================================================
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

os.environ['GROQ_API_KEY'] = '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'
# =========================================================
# ANALYSIS LOGIC (same as your code)
# =========================================================

def analyze_transcript(transcript, groq_api_key, model_name="llama-3.1-8b-instant"):
    """
    Analyzes a given transcript using the Groq API to get a summary and sentiment.
    """
    client = Groq(api_key=groq_api_key)

    system_prompt = (
        "You are an expert at analyzing customer transcripts. "
        "Your task is to provide a concise summary (in 2-3 sentences) "
        "and determine the sentiment (Positive, Neutral, or Negative). "
        "Provide your response in a JSON object with 'summary' and 'sentiment' keys."
    )

    user_prompt = f"Analyze the following customer transcript: '{transcript}'"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            model=model_name,
            temperature=0.5,
            response_format={"type": "json_object"}
        )

        response_data = chat_completion.choices[0].message.content
        analysis = json.loads(response_data)

        return analysis.get('summary', 'Analysis failed.'), analysis.get('sentiment', 'Unknown')

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Analysis failed.", "Unknown"


def save_analysis_to_csv(data, filename="call_analysis.csv"):
    """
    Saves the analysis data to a CSV file.
    """
    fieldnames = ['Transcript', 'Summary', 'Sentiment']
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


# =========================================================
# FUTURISTIC CYBERPUNK / PORTFOLIO LANDING PAGE TEMPLATE
# =========================================================

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NEERAJ'S PORTFOLIO • NeonSentience</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>
        /* Reset-ish */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: radial-gradient(circle at top, #1b2550 0, #050614 40%, #020308 100%);
            color: #e6f3ff;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: stretch;
            padding: 0;
            overflow-x: hidden;
        }

        .scanline {
            position: fixed;
            inset: 0;
            background: repeating-linear-gradient(
                to bottom,
                rgba(255, 255, 255, 0.03),
                rgba(255, 255, 255, 0.03) 1px,
                transparent 1px,
                transparent 3px
            );
            pointer-events: none;
            mix-blend-mode: soft-light;
            opacity: 0.4;
        }

        .grid-overlay {
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(0, 255, 255, 0.12) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 255, 0.12) 1px, transparent 1px);
            background-size: 40px 40px;
            opacity: 0.15;
            pointer-events: none;
        }

        .neon-orb {
            position: fixed;
            width: 420px;
            height: 420px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(0, 255, 255, 0.35), transparent 60%);
            filter: blur(4px);
            top: -80px;
            right: -80px;
            opacity: 0.8;
            pointer-events: none;
        }

        .neon-orb-2 {
            position: fixed;
            width: 380px;
            height: 380px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255, 0, 153, 0.28), transparent 60%);
            filter: blur(4px);
            bottom: -80px;
            left: -60px;
            opacity: 0.8;
            pointer-events: none;
        }

        .wrapper {
            position: relative;
            z-index: 1;
            width: 100%;
            max-width: 1200px;
            margin: 16px auto 32px;
            padding: 12px 12px 24px;
        }

        @media (min-width: 768px) {
            .wrapper {
                margin: 32px auto;
                padding: 24px;
            }
        }

        .hud-frame {
            border-radius: 24px;
            padding: 18px 16px;
            border: 1px solid rgba(0, 255, 255, 0.4);
            background: radial-gradient(circle at top left, rgba(0, 255, 255, 0.08), transparent 55%),
                        radial-gradient(circle at bottom right, rgba(255, 0, 153, 0.13), transparent 55%),
                        rgba(2, 5, 20, 0.85);
            backdrop-filter: blur(18px);
            box-shadow:
                0 0 35px rgba(0, 255, 255, 0.25),
                0 0 60px rgba(255, 0, 153, 0.35);
            border-image: linear-gradient(120deg, #00f5ff, #ff00ae) 1;
        }

        @media (min-width: 768px) {
            .hud-frame {
                padding: 28px 32px;
            }
        }

        header.hud-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
            gap: 12px;
            flex-wrap: wrap;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo-orb {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: conic-gradient(from 220deg, #00f5ff, #ff00ae, #00f5ff);
            box-shadow: 0 0 18px rgba(0, 255, 255, 0.85);
            position: relative;
        }

        .logo-orb::after {
            content: "";
            position: absolute;
            inset: 7px;
            border-radius: 50%;
            background: radial-gradient(circle, #020612, #050615);
        }

        .logo-text-main {
            font-size: 1.1rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #e9f7ff;
        }

        .logo-text-sub {
            font-size: 0.7rem;
            letter-spacing: 0.24em;
            text-transform: uppercase;
            color: #6ee6ff;
            opacity: 0.8;
        }

        .hud-pill {
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid rgba(0, 255, 255, 0.45);
            color: #8cf3ff;
            background: linear-gradient(90deg, rgba(0, 255, 255, 0.18), transparent);
            text-align: center;
            flex-shrink: 0;
        }

        @media (max-width: 480px) {
            .hud-pill {
                width: 100%;
            }
        }

        main {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
        }

        @media (min-width: 900px) {
            main {
                grid-template-columns: minmax(0, 1.4fr) minmax(0, 1.1fr);
                gap: 28px;
            }
        }

        .hero-copy {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .hero-eyebrow {
            font-size: 0.8rem;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            color: #7de5ff;
        }

        .hero-title {
            font-size: clamp(1.9rem, 4vw + 0.5rem, 3rem);
            line-height: 1.1;
            font-weight: 700;
        }

        .hero-title span.neon {
            background: linear-gradient(120deg, #00f5ff, #4de0ff, #ff00ae);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            text-shadow: 0 0 18px rgba(0, 255, 255, 0.75);
        }

        .hero-subtitle {
            font-size: 0.95rem;
            max-width: 32rem;
            color: #b3c8ff;
        }

        .cta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
            align-items: center;
        }

        @media (max-width: 600px) {
            .cta-row {
                flex-direction: column;
                align-items: stretch;
            }
        }

        .btn-primary {
            border: none;
            padding: 12px 24px;
            border-radius: 999px;
            font-size: 0.9rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            cursor: pointer;
            background: radial-gradient(circle at 10% 0, #ffffff 0, #00f5ff 10%, #00a5ff 40%, #ff00ae 100%);
            color: #020313;
            box-shadow:
                0 0 12px rgba(0, 255, 255, 0.9),
                0 0 24px rgba(255, 0, 153, 0.7);
            position: relative;
            overflow: hidden;
            width: 100%;
        }

        @media (min-width: 600px) {
            .btn-primary {
                width: auto;
            }
        }

        .btn-primary::after {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transform: translateX(-100%);
            animation: sweep 3s infinite;
        }

        @keyframes sweep {
            0% { transform: translateX(-120%); }
            40% { transform: translateX(120%); }
            100% { transform: translateX(120%); }
        }

        .btn-secondary {
            padding: 11px 22px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            cursor: pointer;
            border: 1px solid rgba(143, 191, 255, 0.7);
            background: transparent;
            color: #c6ddff;
            width: 100%;
            text-align: center;
        }

        @media (min-width: 600px) {
            .btn-secondary {
                width: auto;
            }
        }

        .glow-text {
            font-size: 0.75rem;
            color: #74f0ff;
            opacity: 0.85;
        }

        .hud-metrics {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 14px;
        }

        .metric-pill {
            border-radius: 999px;
            padding: 6px 10px;
            border: 1px solid rgba(0, 255, 255, 0.4);
            font-size: 0.72rem;
            color: #9deeff;
            background: rgba(5, 18, 40, 0.8);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .metric-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: radial-gradient(circle, #00f5ff, transparent 60%);
        }

        .dashboard-shell {
            position: relative;
            padding: 14px;
            border-radius: 20px;
            background: linear-gradient(145deg, rgba(5, 18, 40, 0.9), rgba(14, 6, 40, 0.9));
            border: 1px solid rgba(0, 255, 255, 0.5);
            box-shadow:
                0 0 24px rgba(0, 255, 255, 0.35),
                0 0 32px rgba(255, 0, 153, 0.45);
            overflow: hidden;
        }

        @media (min-width: 768px) {
            .dashboard-shell {
                padding: 18px;
            }
        }

        .dashboard-shell::before {
            content: "";
            position: absolute;
            inset: -40%;
            background: conic-gradient(from 180deg, rgba(0, 255, 255, 0.08), rgba(255, 0, 153, 0.1), rgba(0, 255, 255, 0.08));
            opacity: 0.7;
            filter: blur(32px);
            pointer-events: none;
        }

        .dashboard-inner {
            position: relative;
            z-index: 1;
            display: grid;
            grid-template-rows: auto auto auto auto;
            gap: 10px;
        }

        .floating-icons {
            position: absolute;
            inset: 0;
            pointer-events: none;
            z-index: 0;
        }

        .floating-icon {
            position: absolute;
            font-size: 1.1rem;
            opacity: 0.5;
            filter: drop-shadow(0 0 6px rgba(0, 255, 255, 0.7));
            animation: float 7s ease-in-out infinite alternate;
        }

        .floating-icon:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
        .floating-icon:nth-child(2) { top: 18%; right: 8%; animation-delay: 1.2s; }
        .floating-icon:nth-child(3) { bottom: 16%; left: 16%; animation-delay: 2.1s; }
        .floating-icon:nth-child(4) { bottom: 8%; right: 14%; animation-delay: 3s; }

        @keyframes float {
            from { transform: translateY(0) translateX(0); opacity: 0.4; }
            to { transform: translateY(-10px) translateX(6px); opacity: 0.9; }
        }

        .hud-topbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            color: #a8caff;
            gap: 8px;
            flex-wrap: wrap;
        }

        .hud-topbar span.code {
            font-family: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
            font-size: 0.7rem;
        }

        .star-strip {
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 0.8rem;
        }

        .star {
            filter: drop-shadow(0 0 4px rgba(255, 215, 0, 0.95));
        }

        .mini-panels {
            display: grid;
            grid-template-columns: 1fr;
            gap: 8px;
            margin-top: 4px;
        }

        @media (min-width: 600px) {
            .mini-panels {
                grid-template-columns: repeat(3, minmax(0, 1fr));
            }
        }

        .mini-panel {
            border-radius: 12px;
            padding: 8px 9px;
            background: radial-gradient(circle at top, rgba(0, 255, 255, 0.2), rgba(2, 10, 30, 0.95));
            border: 1px solid rgba(0, 255, 255, 0.4);
            font-size: 0.7rem;
            color: #cbe7ff;
        }

        .mini-label {
            text-transform: uppercase;
            letter-spacing: 0.18em;
            font-size: 0.6rem;
            color: #7eeaff;
        }

        .mini-value {
            font-size: 0.85rem;
            margin-top: 4px;
        }

        .cityline {
            position: relative;
            height: 70px;
            margin: 6px 0 2px;
            border-radius: 10px;
            background:
                linear-gradient(to top, rgba(0, 0, 0, 0.9), rgba(1, 4, 16, 0.9)),
                linear-gradient(120deg, rgba(0, 255, 255, 0.2), rgba(255, 0, 153, 0.3));
            overflow: hidden;
            border: 1px solid rgba(125, 234, 255, 0.45);
        }

        .city-building {
            position: absolute;
            bottom: 0;
            width: 6%;
            background: linear-gradient(to top, rgba(0, 255, 255, 0.7), rgba(0, 0, 0, 0.1));
            border-radius: 3px 3px 0 0;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.7);
            opacity: 0.9;
        }

        .city-building.magenta {
            background: linear-gradient(to top, rgba(255, 0, 153, 0.8), rgba(0, 0, 0, 0.1));
            box-shadow: 0 0 10px rgba(255, 0, 153, 0.7);
        }

        .city-building:nth-child(1) { left: 6%; height: 34px; }
        .city-building:nth-child(2) { left: 16%; height: 50px; }
        .city-building:nth-child(3) { left: 27%; height: 42px; }
        .city-building:nth-child(4) { left: 38%; height: 58px; }
        .city-building:nth-child(5) { left: 52%; height: 40px; }
        .city-building:nth-child(6) { left: 66%; height: 54px; }
        .city-building:nth-child(7) { left: 78%; height: 44px; }
        .city-building:nth-child(8) { left: 88%; height: 32px; }

        .silhouettes-row {
            position: absolute;
            bottom: 4px;
            left: 4%;
            right: 4%;
            height: 22px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            pointer-events: none;
        }

        .silhouette {
            width: 22px;
            height: 22px;
            border-radius: 40% 40% 10% 10%;
            background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(0, 255, 255, 0.6));
            position: relative;
            filter: drop-shadow(0 0 6px rgba(0, 255, 255, 0.7));
        }

        .silhouette::before {
            content: "";
            position: absolute;
            width: 11px;
            height: 11px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(0, 255, 255, 0.85), rgba(0, 0, 0, 0.85));
            top: -8px;
            left: 5px;
        }

        .silhouette.magenta {
            background: linear-gradient(to top, rgba(0, 0, 0, 0.8), rgba(255, 0, 153, 0.7));
            filter: drop-shadow(0 0 6px rgba(255, 0, 153, 0.85));
        }

        .review-flow {
            margin-top: 4px;
            display: flex;
            gap: 6px;
            font-size: 0.7rem;
            color: #a4d1ff;
            opacity: 0.9;
            flex-wrap: wrap;
        }

        .review-chip {
            border-radius: 999px;
            padding: 4px 8px;
            background: rgba(1, 10, 24, 0.9);
            border: 1px solid rgba(0, 255, 255, 0.4);
        }

        .analysis-panel {
            margin-top: 8px;
            border-radius: 14px;
            padding: 10px 12px;
            background: radial-gradient(circle at top left, rgba(0, 255, 255, 0.22), rgba(5, 8, 30, 0.98));
            border: 1px solid rgba(160, 227, 255, 0.85);
            font-size: 0.8rem;
            color: #d6ebff;
            max-height: 200px;
            overflow-y: auto;
        }

        .analysis-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
            gap: 8px;
            flex-wrap: wrap;
        }

        .analysis-header span.label {
            text-transform: uppercase;
            letter-spacing: 0.2em;
            font-size: 0.63rem;
            color: #9cecff;
        }

        .sentiment-tag {
            font-size: 0.7rem;
            padding: 2px 8px;
            border-radius: 999px;
            text-transform: uppercase;
            letter-spacing: 0.16em;
        }

        .sentiment-positive {
            border: 1px solid rgba(0, 255, 170, 0.8);
            color: #7bffdf;
            background: rgba(0, 210, 140, 0.16);
        }

        .sentiment-negative {
            border: 1px solid rgba(255, 60, 120, 0.9);
            color: #ff9cbf;
            background: rgba(255, 0, 94, 0.18);
        }

        .sentiment-neutral {
            border: 1px solid rgba(144, 189, 255, 0.9);
            color: #d3e5ff;
            background: rgba(24, 46, 98, 0.7);
        }

        .analysis-body {
            font-size: 0.8rem;
            line-height: 1.4;
        }

        .analysis-body pre {
            white-space: pre-wrap;
            font-family: inherit;
        }

        .form-panel {
            margin-top: 8px;
            border-radius: 14px;
            padding: 10px 12px 12px;
            background: radial-gradient(circle at bottom, rgba(255, 0, 153, 0.18), rgba(2, 8, 30, 0.98));
            border: 1px solid rgba(255, 0, 180, 0.8);
        }

        .form-panel label {
            font-size: 0.73rem;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: #ffcfff;
        }

        .form-panel textarea {
            margin-top: 6px;
            width: 100%;
            min-height: 110px;
            max-height: 210px;
            resize: vertical;
            border-radius: 10px;
            border: 1px solid rgba(138, 198, 255, 0.7);
            background: rgba(0, 5, 18, 0.95);
            color: #e6f1ff;
            padding: 8px 10px;
            font-size: 0.8rem;
            outline: none;
            box-shadow: 0 0 10px rgba(2, 217, 255, 0.2);
        }

        .form-panel textarea:focus {
            border-color: #00f5ff;
            box-shadow: 0 0 15px rgba(0, 245, 255, 0.5);
        }

        .form-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 8px;
            gap: 10px;
            flex-wrap: wrap;
        }

        .hint-text {
            font-size: 0.7rem;
            color: #93b7ff;
            opacity: 0.85;
            flex: 1 1 160px;
        }

        .error-banner {
            margin-bottom: 8px;
            padding: 8px 10px;
            border-radius: 8px;
            background: rgba(255, 45, 90, 0.16);
            border: 1px solid rgba(255, 99, 132, 0.8);
            font-size: 0.8rem;
            color: #ffc8d4;
        }

        ::-webkit-scrollbar {
            width: 6px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(4, 8, 26, 0.9);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(0, 255, 255, 0.6);
            border-radius: 999px;
        }
    </style>
</head>
<body>
    <div class="scanline"></div>
    <div class="grid-overlay"></div>
    <div class="neon-orb"></div>
    <div class="neon-orb-2"></div>

    <div class="wrapper">
        <div class="hud-frame">
            <header class="hud-header">
                <div class="logo">
                    <div class="logo-orb"></div>
                    <div>
                        <div class="logo-text-main">NEERAJ'S PORTFOLIO</div>
                        <div class="logo-text-sub">CUSTOMER FEEDBACK • AI • WEB</div>
                    </div>
                </div>
                <div class="hud-pill">
                    LIVE • SENTIMENT GRID ONLINE
                </div>
            </header>

            <main>
                <!-- LEFT: Portfolio + CTA -->
                <section class="hero-copy">
                    <div class="hero-eyebrow">CYBERPUNK DEVELOPER PROFILE</div>
                    <h1 class="hero-title">
                        <span class="neon">NEERAJ'S PORTFOLIO</span>
                    </h1>
                    <p class="hero-subtitle">
                        Building futuristic customer feedback systems with AI-driven sentiment analysis,
                        real-time dashboards, and immersive neon UI. This project showcases a live
                        transcript analyzer powered by Groq and Flask.
                    </p>

                    <div class="cta-row">
                        <button type="submit" form="feedback-form" class="btn-primary">
                            Share Feedback
                        </button>
                        <button type="button" class="btn-secondary">
                            View Sample Insights
                        </button>
                    </div>

                    <div class="glow-text">
                        → Paste any call transcript or customer review on the right to see how Neeraj's AI tooling summarizes and scores sentiment in real-time.
                    </div>

                    <div class="hud-metrics">
                        <div class="metric-pill">
                            <div class="metric-dot"></div>
                            Flask &amp; Python backend
                        </div>
                        <div class="metric-pill">
                            <div class="metric-dot"></div>
                            Groq LLM-powered analysis
                        </div>
                        <div class="metric-pill">
                            <div class="metric-dot"></div>
                            Responsive mobile-first design
                        </div>
                    </div>
                </section>

                <!-- RIGHT: Holographic Dashboard -->
                <section class="dashboard-shell">
                    <div class="floating-icons">
                        <div class="floating-icon">💬</div>
                        <div class="floating-icon">⭐</div>
                        <div class="floating-icon">👍</div>
                        <div class="floating-icon">📊</div>
                    </div>

                    <div class="dashboard-inner">
                        <div class="hud-topbar">
                            <span class="code">NODE ▸ CITY-01 / REVIEW-MATRIX</span>
                            <div class="star-strip">
                                <span class="star">⭐</span>
                                <span class="star">⭐</span>
                                <span class="star">⭐</span>
                                <span class="star">⭐</span>
                                <span class="star" style="opacity:0.45;">⭐</span>
                                <span>4.2 avg • Live</span>
                            </div>
                        </div>

                        <div class="mini-panels">
                            <div class="mini-panel">
                                <div class="mini-label">Sentiment Mix</div>
                                <div class="mini-value">68% Positive • 21% Neutral • 11% Negative</div>
                            </div>
                            <div class="mini-panel">
                                <div class="mini-label">Live Streams</div>
                                <div class="mini-value">32 active calls • 6 queues</div>
                            </div>
                            <div class="mini-panel">
                                <div class="mini-label">Feedback Velocity</div>
                                <div class="mini-value">+412 reviews / hr</div>
                            </div>
                        </div>

                        <!-- Cyberpunk cityline + silhouettes -->
                        <div class="cityline">
                            <div class="city-building"></div>
                            <div class="city-building magenta"></div>
                            <div class="city-building"></div>
                            <div class="city-building magenta"></div>
                            <div class="city-building"></div>
                            <div class="city-building magenta"></div>
                            <div class="city-building"></div>
                            <div class="city-building magenta"></div>

                            <div class="silhouettes-row">
                                <div class="silhouette"></div>
                                <div class="silhouette magenta"></div>
                                <div class="silhouette"></div>
                                <div class="silhouette magenta"></div>
                            </div>
                        </div>

                        <div class="review-flow">
                            <div class="review-chip">“Agent was extremely helpful!”</div>
                            <div class="review-chip">“Wait time was too long.”</div>
                            <div class="review-chip">“Loved the resolution speed.”</div>
                        </div>

                        <!-- Analysis panel (shows summary + sentiment when available) -->
                        {% if summary %}
                        <div class="analysis-panel">
                            <div class="analysis-header">
                                <span class="label">Latest Transcript Analysis</span>
                                {% set sentiment_lower = sentiment|lower %}
                                {% if "pos" in sentiment_lower %}
                                    <span class="sentiment-tag sentiment-positive">{{ sentiment }}</span>
                                {% elif "neg" in sentiment_lower %}
                                    <span class="sentiment-tag sentiment-negative">{{ sentiment }}</span>
                                {% else %}
                                    <span class="sentiment-tag sentiment-neutral">{{ sentiment }}</span>
                                {% endif %}
                            </div>
                            <div class="analysis-body">
                                <strong>Summary:</strong>
                                <pre>{{ summary }}</pre>
                            </div>
                        </div>
                        {% endif %}

                        <!-- Transcript input form -->
                        <div class="form-panel">
                            {% if api_error %}
                            <div class="error-banner">
                                ⚠ {{ api_error }}
                            </div>
                            {% endif %}

                            <form id="feedback-form" method="post">
                                <label for="transcript">Transcript • Neon City Call Log</label>
                                <textarea id="transcript" name="transcript" required>{{ transcript }}</textarea>
                                <div class="form-actions">
                                    <div class="hint-text">
                                        Paste a full call transcript or customer review to generate
                                        a holographic summary + sentiment.
                                    </div>
                                    <button type="submit" class="btn-primary">
                                        Share Feedback
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                </section>
            </main>
        </div>
    </div>
    <script>
    const textarea = document.getElementById("transcript");
    const form = document.getElementById("feedback-form");

    textarea.addEventListener("keydown", function (event) {
        // ENTER → submit form
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault(); // stop new line
            form.submit();          // submit transcript
        }
        // SHIFT + ENTER → new line (default behavior, do nothing)
    });
</script>

</body>
</html>
"""

# =========================================================
# FLASK ROUTE
# =========================================================

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    summary = None
    sentiment = None
    api_error = None

    if request.method == "POST":
        transcript = request.form.get("transcript", "").strip()

        if not GROQ_API_KEY:
            api_error = "GROQ_API_KEY is not set. Please set it as an environment variable and restart the app."
        elif not transcript:
            api_error = "Transcript cannot be empty."
        else:
            summary, sentiment = analyze_transcript(transcript, GROQ_API_KEY)
            analysis_data = {
                "Transcript": transcript,
                "Summary": summary,
                "Sentiment": sentiment
            }
            save_analysis_to_csv(analysis_data)

    return render_template_string(
        PAGE_TEMPLATE,
        transcript=transcript,
        summary=summary,
        sentiment=sentiment,
        api_error=api_error
    )


# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    # host="0.0.0.0" lets mobile on same Wi-Fi open it using your PC's IP
    app.run(host="0.0.0.0", port=5000, debug=True)
